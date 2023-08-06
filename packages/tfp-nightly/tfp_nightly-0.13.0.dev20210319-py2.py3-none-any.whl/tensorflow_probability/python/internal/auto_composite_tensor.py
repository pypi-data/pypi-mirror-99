# Copyright 2020 The TensorFlow Probability Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Turns arbitrary objects into tf.CompositeTensor."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools

import numpy as np
import tensorflow.compat.v2 as tf

from tensorflow.python.framework import composite_tensor  # pylint: disable=g-direct-tensorflow-import
from tensorflow.python.saved_model import nested_structure_coder  # pylint: disable=g-direct-tensorflow-import
from tensorflow.python.util import tf_inspect  # pylint: disable=g-direct-tensorflow-import

__all__ = [
    'auto_composite_tensor',
    'AutoCompositeTensor',
]


_registry = {}  # Mapping from (python pkg, class name) -> class.

_SENTINEL = object()

_AUTO_COMPOSITE_TENSOR_VERSION = 2


def _extract_init_kwargs(obj, omit_kwargs=(), limit_to=None,
                         prefer_static_value=()):
  """Extract constructor kwargs to reconstruct `obj`."""
  sig = tf_inspect.signature(obj.__init__)
  if any(v.kind in (tf_inspect.Parameter.VAR_KEYWORD,
                    tf_inspect.Parameter.VAR_POSITIONAL)
         for v in sig.parameters.values()):
    raise ValueError(
        '*args and **kwargs are not supported. Found `{}`'.format(sig))

  keys = [p for p in sig.parameters if p != 'self' and p not in omit_kwargs]
  if limit_to is not None:
    keys = [k for k in keys if k in limit_to]

  kwargs = {}
  not_found = object()
  for k in keys:

    if k in prefer_static_value:
      srcs = [
          getattr(obj, 'parameters', {}).get(k, not_found),
          getattr(obj, k, not_found), getattr(obj, '_' + k, not_found),
      ]
    else:
      srcs = [
          getattr(obj, k, not_found), getattr(obj, '_' + k, not_found),
          getattr(obj, 'parameters', {}).get(k, not_found),
      ]
    if any(v is not not_found for v in srcs):
      kwargs[k] = [v for v in srcs if v is not not_found][0]
    else:
      raise ValueError(
          f'Could not determine an appropriate value for field `{k}` in object '
          ' `{obj}`. Looked for \n'
          ' 1. an attr called `{k}`,\n'
          ' 2. an attr called `_{k}`,\n'
          ' 3. an entry in `obj.parameters` with key "{k}".')
    if k in prefer_static_value and kwargs[k] is not None:
      if tf.is_tensor(kwargs[k]):
        static_val = tf.get_static_value(kwargs[k])
        if static_val is not None:
          kwargs[k] = static_val
      if isinstance(kwargs[k], (np.ndarray, np.generic)):
        # Generally, these are shapes or int.
        kwargs[k] = kwargs[k].tolist()
  return kwargs


def _extract_type_spec_recursively(value):
  """Return (collection of) TypeSpec(s) for `value` if it includes `Tensor`s.

  If `value` is a `Tensor` or `CompositeTensor`, return its `TypeSpec`. If
  `value` is a collection containing `Tensor` values, recursively supplant them
  with their respective `TypeSpec`s in a collection of parallel stucture.

  If `value` is nont of the above, return it unchanged.

  Args:
    value: a Python `object` to (possibly) turn into a (collection of)
    `tf.TypeSpec`(s).

  Returns:
    spec: the `TypeSpec` or collection of `TypeSpec`s corresponding to `value`
    or `value`, if no `Tensor`s are found.
  """
  if isinstance(value, composite_tensor.CompositeTensor):
    return value._type_spec  # pylint: disable=protected-access
  if tf.is_tensor(value):
    return tf.TensorSpec(value.shape, value.dtype)
  if isinstance(value, (list, tuple)):
    specs = [_extract_type_spec_recursively(v) for v in value]
    has_tensors = any(a is not b for a, b in zip(value, specs))
    has_only_tensors = all(a is not b for a, b in zip(value, specs))
    if has_tensors:
      if has_tensors != has_only_tensors:
        raise NotImplementedError(
            'Found `{}` with both Tensor and non-Tensor parts: {}'
            .format(type(value), value))
      return type(value)(specs)
  return value


class _AutoCompositeTensorTypeSpec(tf.TypeSpec):
  """A tf.TypeSpec for `AutoCompositeTensor` objects."""

  __slots__ = ('_param_specs', '_non_tensor_params', '_omit_kwargs',
               '_prefer_static_value')

  def __init__(self, param_specs, non_tensor_params, omit_kwargs,
               prefer_static_value):
    self._param_specs = param_specs
    self._non_tensor_params = non_tensor_params
    self._omit_kwargs = omit_kwargs
    self._prefer_static_value = prefer_static_value

  @classmethod
  def from_instance(cls, instance, omit_kwargs=()):
    prefer_static_value = tuple(
        getattr(instance, '_composite_tensor_shape_params', ()))
    kwargs = _extract_init_kwargs(instance, omit_kwargs=omit_kwargs,
                                  prefer_static_value=prefer_static_value)

    non_tensor_params = {}
    param_specs = {}
    for k, v in list(kwargs.items()):
      # If v contains no Tensors, this will just be v
      type_spec_or_v = _extract_type_spec_recursively(v)
      if type_spec_or_v is not v:
        param_specs[k] = type_spec_or_v
      else:
        non_tensor_params[k] = v

    # Construct the spec.
    return cls(param_specs=param_specs,
               non_tensor_params=non_tensor_params,
               omit_kwargs=omit_kwargs,
               prefer_static_value=prefer_static_value)

  def _to_components(self, obj):
    return _extract_init_kwargs(obj, limit_to=list(self._param_specs))

  def _from_components(self, components):
    kwargs = dict(self._non_tensor_params, **components)
    return self.value_type(**kwargs)

  @property
  def _component_specs(self):
    return self._param_specs

  def _serialize(self):
    result = (_AUTO_COMPOSITE_TENSOR_VERSION,
              self._param_specs,
              self._non_tensor_params,
              self._omit_kwargs,
              self._prefer_static_value)
    return result

  @classmethod
  def _deserialize(cls, encoded):
    version = encoded[0]
    if version == 1:
      encoded = encoded + ((),)
      version = 2
    if version != _AUTO_COMPOSITE_TENSOR_VERSION:
      raise ValueError('Expected version {}, but got {}'
                       .format(_AUTO_COMPOSITE_TENSOR_VERSION, version))
    return cls(*encoded[1:])


_TypeSpecCodec = nested_structure_coder._TypeSpecCodec  # pylint: disable=protected-access
_TypeSpecCodec.TYPE_SPEC_CLASS_FROM_PROTO[321584790] = (
    _AutoCompositeTensorTypeSpec)
_TypeSpecCodec.TYPE_SPEC_CLASS_TO_PROTO[_AutoCompositeTensorTypeSpec] = (
    321584790)
del _TypeSpecCodec


class AutoCompositeTensor(composite_tensor.CompositeTensor):
  """Recommended base class for `@auto_composite_tensor`-ified classes.

  See details in `tfp.experimental.auto_composite_tensor` description.
  """

  @property
  def _type_spec(self):
    # This property will be overwritten by the `@auto_composite_tensor`
    # decorator. However, we need it so that a valid subclass of the `ABCMeta`
    # class `CompositeTensor` can be constructed and passed to the
    # `@auto_composite_tensor` decorator
    pass


def auto_composite_tensor(cls=None, omit_kwargs=()):
  """Automagically generate `CompositeTensor` behavior for `cls`.

  `CompositeTensor` objects are able to pass in and out of `tf.function` and
  `tf.while_loop`, or serve as part of the signature of a TF saved model.

  The contract of `auto_composite_tensor` is that all __init__ args and kwargs
  must have corresponding public or private attributes (or properties). Each of
  these attributes is inspected (recursively) to determine whether it is (or
  contains) `Tensor`s or non-`Tensor` metadata. `list` and `tuple` attributes
  are supported, but must either contain *only* `Tensor`s (or lists, etc,
  thereof), or *no* `Tensor`s. E.g.,
    - object.attribute = [1., 2., 'abc']                        # valid
    - object.attribute = [tf.constant(1.), [tf.constant(2.)]]   # valid
    - object.attribute = ['abc', tf.constant(1.)]               # invalid

  If the object has a `_composite_tensor_shape_parameters` field (presumed to
  have `tuple` of `str` value), the flattening code will use
  `tf.get_static_value` to attempt to preserve shapes as static metadata, for
  fields whose name matches a name specified in that field. Preserving static
  values can be important to correctly propagating shapes through a loop.

  If the decorated class `A` does not subclass `CompositeTensor`, a *new class*
  will be generated, which mixes in `A` and `CompositeTensor`.

  To avoid this extra class in the class hierarchy, we suggest inheriting from
  `auto_composite_tensor.AutoCompositeTensor`, which inherits from
  `CompositeTensor` and implants a trivial `_type_spec` @property. The
  `@auto_composite_tensor` decorator will then overwrite this trivial
  `_type_spec` @property. The trivial one is necessary because `_type_spec` is
  an abstract property of `CompositeTensor`, and a valid class instance must be
  created before the decorator can execute -- without the trivial `_type_spec`
  property present, `ABCMeta` will throw an error! The user may thus do any of
  the following:

  #### `AutoCompositeTensor` base class (recommended)
  ```python
  @tfp.experimental.auto_composite_tensor
  class MyClass(tfp.experimental.AutoCompositeTensor):
    ...

  mc = MyClass()
  type(mc)
  # ==> MyClass
  ```

  #### No `CompositeTensor` base class (ok, but changes expected types)
  ```python
  @tfp.experimental.auto_composite_tensor
  class MyClass(object):
    ...

  mc = MyClass()
  type(mc)
  # ==> MyClass_AutoCompositeTensor
  ```

  #### `CompositeTensor` base class, requiring trivial `_type_spec`
  ```python
  from tensorflow.python.framework import composite_tensor
  @tfp.experimental.auto_composite_tensor
  class MyClass(composite_tensor.CompositeTensor):
    @property
    def _type_spec(self):  # will be overwritten by @auto_composite_tensor
      pass
    ...

  mc = MyClass()
  type(mc)
  # ==> MyClass
  ```

  ## Full usage example

  ```python
  @tfp.experimental.auto_composite_tensor(omit_kwargs=('name',))
  class Adder(tfp.experimental.AutoCompositeTensor):
    def __init__(self, x, y, name=None):
      with tf.name_scope(name or 'Adder') as name:
        self._x = tf.convert_to_tensor(x)
        self._y = tf.convert_to_tensor(y)
        self._name = name

    def xpy(self):
      return self._x + self._y

  def body(obj):
    return Adder(obj.xpy(), 1.),

  result, = tf.while_loop(
      cond=lambda _: True,
      body=body,
      loop_vars=(Adder(1., 1.),),
      maximum_iterations=3)

  result.xpy()  # => 5.
  ```

  Args:
    cls: The class for which to create a CompositeTensor subclass.
    omit_kwargs: Optional sequence of kwarg names to be omitted from the spec.

  Returns:
    composite_tensor_subclass: A subclass of `cls` and TF CompositeTensor.
  """
  if cls is None:
    return functools.partial(auto_composite_tensor,
                             omit_kwargs=omit_kwargs)

  # If the declared class is already a CompositeTensor subclass, we can avoid
  # affecting the actual type of the returned class. Otherwise, we need to
  # explicitly mix in the CT type, and hence create and return a newly
  # synthesized type.
  if issubclass(cls, composite_tensor.CompositeTensor):
    class _AlreadyCTTypeSpec(_AutoCompositeTensorTypeSpec):

      @property
      def value_type(self):
        return cls

    _AlreadyCTTypeSpec.__name__ = f'{cls.__name__}_ACTTypeSpec'

    cls._type_spec = property(  # pylint: disable=protected-access
        lambda self: _AlreadyCTTypeSpec.from_instance(self, omit_kwargs))
    return cls

  clsid = (cls.__module__, cls.__name__, omit_kwargs)

  # Check for subclass if retrieving from the _registry, in case the user
  # has redefined the class (e.g. in a REPL/notebook).
  if clsid in _registry and issubclass(_registry[clsid], cls):
    return _registry[clsid]

  class _GeneratedCTTypeSpec(_AutoCompositeTensorTypeSpec):

    @property
    def value_type(self):
      return _registry[clsid]

  _GeneratedCTTypeSpec.__name__ = f'{cls.__name__}_GCTTypeSpec'

  class _AutoCompositeTensor(cls, composite_tensor.CompositeTensor):
    """A per-`cls` subclass of `CompositeTensor`."""

    @property
    def _type_spec(self):
      return _GeneratedCTTypeSpec.from_instance(self, omit_kwargs)

  _AutoCompositeTensor.__name__ = '{}_AutoCompositeTensor'.format(cls.__name__)
  _registry[clsid] = _AutoCompositeTensor
  return _AutoCompositeTensor
