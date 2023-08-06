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
"""Contains sharding-aware versions of tfd.JointDistributions."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools

from tensorflow_probability.python.internal.backend.numpy.compat import v2 as tf
from tensorflow_probability.substrates.numpy import distributions as distribution_lib
from tensorflow_probability.substrates.numpy.distributions import log_prob_ratio as lp_ratio
from tensorflow_probability.substrates.numpy.experimental.distribute import distribute_lib
from tensorflow_probability.substrates.numpy.internal import samplers


class JointDistributionDistributedMixin(object):
  """A JDMixin that shards the log_prob calculation."""

  @property
  def shard_axis_name(self):
    return self._parameters['shard_axis_name']

  def _map_measure_over_dists(self, attr, value):
    """Override the default implementation to shard its log_prob calculation."""
    if any(x is None for x in tf.nest.flatten(value)):
      raise ValueError('No `value` part can be `None`; saw: {}.'.format(value))
    if attr == 'log_prob' and any(self.experimental_is_sharded):

      def inner_log_prob_parts(flat_value):
        unflat_value = self._model_unflatten(flat_value)
        ds, xs = self._call_flat_sample_distributions(
            value=unflat_value, seed=samplers.zeros_seed())
        # For sharded distributions, we need to make sure not to do an
        # all-reduce.
        flat_sharded = self._model_flatten(self.experimental_is_sharded)
        log_prob_fns = [
            functools.partial(d.log_prob, reduce_over_shards=False)
            if s else d.log_prob for d, s in zip(ds, flat_sharded)]
        # We need to flatten and unflatten here to ensure the output structure
        # matches `flat_sharded_distributions`.
        vals = self._model_unflatten(
            [log_prob_fn(x) for log_prob_fn, x in zip(log_prob_fns, xs)])
        return self._model_flatten(vals)

      flat_value = self._model_flatten(value)
      flat_sharded_distributions = self._model_flatten(
          self.experimental_is_sharded)
      flat_xs = distribute_lib.make_sharded_log_prob_parts(
          inner_log_prob_parts,
          flat_sharded_distributions,
          axis_name=self.shard_axis_name)(
              flat_value)
      return iter(flat_xs)
    ds, xs = self._call_flat_sample_distributions(
        value=value, seed=samplers.zeros_seed())
    return (getattr(d, attr)(x) for d, x in zip(ds, xs))


class JointDistributionSequential(JointDistributionDistributedMixin,
                                  distribution_lib.JointDistributionSequential):
  """A sharding-aware JointDistributionSequential."""

  def __init__(self,
               model,
               validate_args=False,
               shard_axis_name=None,
               name=None):
    """Construct the `JointDistributionSequential` distribution.

    Args:
      model: Python list of either tfd.Distribution instances and/or lambda
        functions which take the `k` previous distributions and returns a new
        tfd.Distribution instance.
      validate_args: Python `bool`.  Whether to validate input with asserts. If
        `validate_args` is `False`, and the inputs are invalid, correct behavior
        is not guaranteed.
        Default value: `False`.
      shard_axis_name: `str` for axis name for use in JAX backend.
      name: The name for ops managed by the distribution.
        Default value: `None` (i.e., `"JointDistributionSequential"`).
    """
    super(JointDistributionSequential, self).__init__(
        model, validate_args=validate_args, name=name)
    self._parameters['shard_axis_name'] = shard_axis_name

  _composite_tensor_nonshape_params = ('model',)


class JointDistributionNamed(JointDistributionDistributedMixin,
                             distribution_lib.JointDistributionNamed):
  """A sharding-aware JointDistributionNamed."""

  def __init__(self,
               model,
               validate_args=False,
               shard_axis_name=None,
               name=None):
    """Construct the `JointDistributionNamed` distribution.

    Args:
      model: Python `dict`, `collections.OrderedDict`, or `namedtuple` of
        distribution-making functions each with required args corresponding only
        to other keys.
      validate_args: Python `bool`.  Whether to validate input with asserts. If
        `validate_args` is `False`, and the inputs are invalid, correct behavior
        is not guaranteed.
        Default value: `False`.
      shard_axis_name: `str` for axis name for use in JAX backend.
      name: The name for ops managed by the distribution.
        Default value: `None` (i.e., `"JointDistributionNamed"`).
    """
    super(JointDistributionNamed,
          self).__init__(model, validate_args, name or 'JointDistributionNamed')
    self._parameters['shard_axis_name'] = shard_axis_name

  _composite_tensor_nonshape_params = ('model',)


class JointDistributionCoroutine(JointDistributionDistributedMixin,
                                 distribution_lib.JointDistributionCoroutine):
  """A sharding-aware JointDistributionCoroutine."""

  def __init__(
      self,
      model,
      sample_dtype=None,
      validate_args=False,
      shard_axis_name=None,
      name=None,
  ):
    """Construct the `JointDistributionCoroutine` distribution.

    Args:
      model: A generator that yields a sequence of `tfd.Distribution`-like
        instances.
      sample_dtype: Samples from this distribution will be structured like
        `tf.nest.pack_sequence_as(sample_dtype, list_)`. `sample_dtype` is only
        used for `tf.nest.pack_sequence_as` structuring of outputs, never
        casting (which is the responsibility of the component distributions).
        Default value: `None` (i.e. `namedtuple`).
      validate_args: Python `bool`.  Whether to validate input with asserts. If
        `validate_args` is `False`, and the inputs are invalid, correct behavior
        is not guaranteed.
        Default value: `False`.
      shard_axis_name: `str` for axis name for use in JAX backend.
      name: The name for ops managed by the distribution.
        Default value: `None` (i.e., `JointDistributionCoroutine`).
    """
    super(JointDistributionCoroutine, self).__init__(
        model,
        sample_dtype=sample_dtype,
        validate_args=validate_args,
        name=name)
    self._parameters['shard_axis_name'] = shard_axis_name


@lp_ratio.RegisterLogProbRatio(JointDistributionSequential)
@lp_ratio.RegisterLogProbRatio(JointDistributionNamed)
@lp_ratio.RegisterLogProbRatio(JointDistributionCoroutine)
def _dist_jd_log_prob_ratio(p, x, q, y, name=None):
  """Distributed log-prob ratio for JDs."""
  with tf.name_scope(name or 'dist_jd_log_prob_ratio'):
    tf.nest.assert_same_structure(x, y)
    if p.shard_axis_name != q.shard_axis_name:
      raise ValueError(
          'p and q must have the same shard_axis_name. '
          f'Saw: p: {p}, {p.shard_axis_name}, q: {q}, {q.shard_axis_name}')

    is_sharded = p.experimental_is_sharded
    q_sharded = q.experimental_is_sharded
    if is_sharded != q_sharded:
      raise ValueError(
          'p and q must use the same sharding. '
          f'Saw: p: {p}, {is_sharded}, q: {q}, {q_sharded}')

    def log_prob_ratio_parts_fn(x_y):
      x = tf.nest.map_structure(lambda part: part[0], x_y)
      y = tf.nest.map_structure(lambda part: part[1], x_y)
      p_dists = p.sample_distributions(value=x, seed=samplers.zeros_seed())[0]
      q_dists = q.sample_distributions(value=y, seed=samplers.zeros_seed())[0]
      # Ensure sharded distributions defer reductions.
      kwds = lambda s: {'reduce_over_shards': False} if s else {}
      return tf.nest.map_structure(
          lambda p, x, q, y, s: lp_ratio.log_prob_ratio(p, x, q, y, **kwds(s)),
          p_dists, x, q_dists, y, is_sharded)

    return tf.add_n(
        tf.nest.flatten(
            distribute_lib.make_sharded_log_prob_parts(
                log_prob_ratio_parts_fn,
                # Stack, because make_sharded_log_prob_parts expects
                # inputs/outputs to be 1 to 1. TODO(b/175084455): revisit this
                # after the distributed bijectors are done, as it is likely that
                # make_sharded_log_prob_parts will be adjusted then to not have
                # this limitation.
                is_sharded,
                axis_name=p.shard_axis_name)(tf.nest.map_structure(
                    lambda x, y: tf.stack([x, y], axis=0), x, y))))

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# This file is auto-generated by substrates/meta/rewrite.py
# It will be surfaced by the build system as a symlink at:
#   `tensorflow_probability/substrates/numpy/experimental/distribute/joint_distribution.py`
# For more info, see substrate_runfiles_symlinks in build_defs.bzl
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# (This notice adds 10 to line numbering.)


