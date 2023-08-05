# Lint as: python3
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Vector of correlated Hull-White models with time-dependent parameters."""

import tensorflow.compat.v2 as tf

from tf_quant_finance.math import gradient
from tf_quant_finance.math import piecewise
from tf_quant_finance.math import random_ops as random
from tf_quant_finance.models import euler_sampling
from tf_quant_finance.models import generic_ito_process
from tf_quant_finance.models import utils


class VectorHullWhiteModel(generic_ito_process.GenericItoProcess):
  r"""Ensemble of correlated Hull-White Models.

  Represents the Ito process:

  ```None
    dr_i(t) = (theta_i(t) - a_i(t) * r_i(t)) dt + sigma_i(t) * dW_{r_i}(t),
    1 <= i <= n,
  ```
  where `W_{r_i}` are 1D Brownian motions with a correlation matrix `Rho(t)`.
  For each `i`, `r_i` is the Hull-White process.
  `theta_i`, `a_i`, `sigma_i`, `Rho` are positive functions of time.
  `a_i` correspond to the mean-reversion rate, `sigma_i` is the volatility of
  the process, `theta_i(t)` is the function that determines long run behaviour
  of the process `r(t) = (r_1(t), ..., r_n(t))`
  and is computed to match the initial (at t=0) discount curve:

  ```None
  \theta_i = df_i(t) / dt + a_i * f_i(t) + 0.5 * sigma_i**2 / a_i
             * (1 - exp(-2 * a_i *t)), 1 <= i <= n
  ```
  where `f_i(t)` is the instantaneous forward rate at time `0` for a maturity
  `t` and `df_i(t)/dt` is the gradient of `f_i` with respect to the maturity.
  See Section 3.3.1 of [1] for details.

  The price at time `t` of a zero-coupon bond maturing at `T` is given by
  (Ref. [2]):

  ```None
  P(t,T) = P(0,T) / P(0,t) *
           exp(-(r(t) - f(0,t)) * G(t,T) - 0.5 * y(t) * G(t,T)^2)

  y(t) = int_0^t [exp(-2 int_u^t (a(s) ds)) sigma(u)^2 du]

  G(t,T) = int_t^T [exp(-int_t^u a(s) ds) du]
  ```

  If mean-reversion, `a_i`, is constant and the volatility (`sigma_i`), and
  correlation (`Rho`) are piecewise constant functions, the process is sampled
  exactly. Otherwise, Euler sampling is used.

  For `n=1` this class represents Hull-White Model (see
  tff.models.hull_white.HullWhiteModel1F).

  #### Example. Two correlated Hull-White processes.

  ```python
  import numpy as np
  import tensorflow as tf
  import tf_quant_finance as tff

  dtype = tf.float64
  # Mean-reversion is constant for the two processes. `mean_reversion(t)`
  # has shape `[dim] + t.shape`.
  mean_reversion = [0.03, 0.02]
  # Volatility is a piecewise constant function with jumps at the same locations
  # for both Hull-White processes. `volatility(t)` has shape `[dim] + t.shape`.
  volatility = tff.math.piecewise.PiecewiseConstantFunc(
      jump_locations=[[0.1, 2.], [0.1, 2.]],
      values=[[0.01, 0.02, 0.01], [0.01, 0.015, 0.01]],
      dtype=dtype)
  # Correlation matrix is constant
  corr_matrix = [[1., 0.1], [0.1, 1.]]
  initial_discount_rate_fn = lambda *args: [0.01, 0.015]
  process = tff.models.hull_white.VectorHullWhiteModel(
      dim=2, mean_reversion=mean_reversion,
      volatility=volatility,
      initial_discount_rate_fn=initial_discount_rate_fn,
      corr_matrix=corr_matrix,
      dtype=dtype)
  # Sample 10000 paths using Sobol numbers as a random type.
  times = np.linspace(0., 1.0, 10)
  num_samples = 10000  # number of trajectories
  paths = process.sample_paths(
      times,
      num_samples=num_samples,
      random_type=tff.math.random.RandomType.SOBOL,
      seed=[4, 2])
  # Compute mean for each Hull-White process at the terminal value
  tf.math.reduce_mean(paths[:, -1, :], axis=0)
  # Expected: [0.01070005, 0.01540942]

  # User can supply time discretization grid along with the underlying
  # normal draws directly to the sampler.
  times_grid = tf.sort(tf.concat([np.linspace(0., 1.0, 10), [0.1]], axis=-1))
  normal_draws = tf.random.stateless_normal(
      [num_samples // 2, 10, 2], seed=[4, 2], dtype=dtype)
  normal_draws = tf.concat([normal_draws, -normal_draws], axis=0)
  paths = process.sample_paths(
      times,
      num_samples=num_samples,
      times_grid = times_grid,
      normal_draws=normal_draws)
  # Compute mean for each Hull-White process at the terminal value
  tf.math.reduce_mean(paths[:, -1, :], axis=0)
  # Expected: [0.0101668 , 0.01509873]
  ```

  #### References:
    [1]: D. Brigo, F. Mercurio. Interest Rate Models. 2007.
    [2]: Leif B. G. Andersen and Vladimir V. Piterbarg. Interest Rate Modeling.
    Volume II: Term Structure Models.
  """

  def __init__(self,
               dim,
               mean_reversion,
               volatility,
               initial_discount_rate_fn,
               corr_matrix=None,
               dtype=None,
               name=None):
    """Initializes the Correlated Hull-White Model.

    Args:
      dim: A Python scalar which corresponds to the number of correlated
        Hull-White Models.
      mean_reversion: A real positive `Tensor` of shape `[dim]` or a Python
        callable. The callable can be one of the following:
          (a) A left-continuous piecewise constant object (e.g.,
          `tff.math.piecewise.PiecewiseConstantFunc`) that has a property
          `is_piecewise_constant` set to `True`. In this case the object
          should have a method `jump_locations(self)` that returns a
          `Tensor` of shape `[dim, num_jumps]` or `[num_jumps]`
          In the first case, `mean_reversion(t)` should return a `Tensor`
          of shape `[dim] + t.shape`, and in the second, `t.shape + [dim]`,
          where `t` is a rank 1 `Tensor` of the same `dtype` as the output.
          See example in the class docstring.
         (b) A callable that accepts scalars (stands for time `t`) and returns a
         `Tensor` of shape `[dim]`.
        Corresponds to the mean reversion rate.
      volatility: A real positive `Tensor` of the same `dtype` as
        `mean_reversion` or a callable with the same specs as above.
        Corresponds to the lond run price variance.
      initial_discount_rate_fn: A Python callable that accepts expiry time as
        a real `Tensor` of the same `dtype` as `mean_reversion` and returns a
        `Tensor` of shape `input_shape + dim`.
        Corresponds to the zero coupon bond yield at the present time for the
        input expiry time.
      corr_matrix: A `Tensor` of shape `[dim, dim]` and the same `dtype` as
        `mean_reversion` or a Python callable. The callable can be one of
        the following:
          (a) A left-continuous piecewise constant object (e.g.,
          `tff.math.piecewise.PiecewiseConstantFunc`) that has a property
          `is_piecewise_constant` set to `True`. In this case the object
          should have a method `jump_locations(self)` that returns a
          `Tensor` of shape `[num_jumps]`. `corr_matrix(t)` should return a
          `Tensor` of shape `t.shape + [dim]`, where `t` is a rank 1 `Tensor`
          of the same `dtype` as the output.
         (b) A callable that accepts scalars (stands for time `t`) and returns a
         `Tensor` of shape `[dim, dim]`.
        Corresponds to the correlation matrix `Rho`.
      dtype: The default dtype to use when converting values to `Tensor`s.
        Default value: `None` which means that default dtypes inferred by
          TensorFlow are used.
      name: Python string. The name to give to the ops created by this class.
        Default value: `None` which maps to the default name `hull_white_model`.

    Raises:
      ValueError:
        (a) If either `mean_reversion`, `volatility`, or `corr_matrix` is
          a piecewise constant function where `jump_locations` have batch shape
          of rank > 1.
        (b): If batch rank of the `jump_locations` is `[n]` with `n` different
          from `dim`.
    """
    self._name = name or 'hull_white_model'
    with tf.name_scope(self._name):
      self._dtype = dtype or None
      # If the parameter is callable but not a piecewise constant use
      # generic sampling method (e.g., Euler).
      self._sample_with_generic = False
      def _instant_forward_rate_fn(t):
        t = tf.convert_to_tensor(t, dtype=self._dtype)
        def _log_zero_coupon_bond(x):
          r = tf.convert_to_tensor(
              initial_discount_rate_fn(x), dtype=self._dtype)
          return -r * x

        rate = -gradient.fwd_gradient(
            _log_zero_coupon_bond, t, use_gradient_tape=True,
            unconnected_gradients=tf.UnconnectedGradients.ZERO)
        return rate

      def _initial_discount_rate_fn(t):
        return tf.convert_to_tensor(
            initial_discount_rate_fn(t), dtype=self._dtype)

      self._instant_forward_rate_fn = _instant_forward_rate_fn
      self._initial_discount_rate_fn = _initial_discount_rate_fn
      self._mean_reversion, sample_with_generic = _input_type(
          mean_reversion, dim=dim, dtype=dtype, name='mean_reversion')

      # Update flag to whether to sample with a generic sampler.
      self._sample_with_generic |= sample_with_generic
      # Get the volatility type
      self._volatility, sample_with_generic = _input_type(
          volatility, dim=dim, dtype=dtype, name='volatility')

      # Update flag to whether to sample with a generic sampler.
      self._sample_with_generic |= sample_with_generic
      if corr_matrix is not None:
        # Get correlation matrix type
        self._corr_matrix, sample_with_generic = _input_type(
            corr_matrix, dim=dim, dtype=dtype, name='corr_matrix')
        # Update flag to whether to sample with a generic sampler.
        self._sample_with_generic |= sample_with_generic
      else:
        self._corr_matrix = None

      if not self._sample_with_generic:
        self._exact_discretization_setup(dim)

    # Volatility function
    def _vol_fn(t, x):
      """Volatility function of correlated Hull-White."""
      # Get parameter values at time `t`
      volatility = _get_parameters(tf.expand_dims(t, -1), self._volatility)[0]
      volatility = tf.transpose(volatility)
      if self._corr_matrix is not None:
        corr_matrix = _get_parameters(tf.expand_dims(t, -1), self._corr_matrix)
        corr_matrix = corr_matrix[0]
        corr_matrix = tf.linalg.cholesky(corr_matrix)
      else:
        corr_matrix = tf.eye(self._dim, dtype=volatility.dtype)

      return volatility * corr_matrix + tf.zeros(
          x.shape.as_list()[:-1] + [self._dim, self._dim],
          dtype=volatility.dtype)

    # Drift function
    def _drift_fn(t, x):
      """Drift function of correlated Hull-White."""
      # Get parameter values at time `t`
      mean_reversion, volatility = _get_parameters(  # pylint: disable=unbalanced-tuple-unpacking
          tf.expand_dims(t, -1), self._mean_reversion, self._volatility)
      fwd_rates = self._instant_forward_rate_fn(t)
      fwd_rates_grad = gradient.fwd_gradient(
          self._instant_forward_rate_fn, t, use_gradient_tape=True,
          unconnected_gradients=tf.UnconnectedGradients.ZERO)
      drift = fwd_rates_grad + mean_reversion * fwd_rates
      drift += (volatility**2 / 2 / mean_reversion
                * (1 - tf.math.exp(-2 * mean_reversion * t))
                - mean_reversion * x)
      return drift
    super(VectorHullWhiteModel, self).__init__(dim, _drift_fn, _vol_fn,
                                               dtype, name)

  @property
  def mean_reversion(self):
    return self._mean_reversion

  @property
  def volatility(self):
    return self._volatility

  def sample_paths(self,
                   times,
                   num_samples=1,
                   random_type=None,
                   seed=None,
                   skip=0,
                   time_step=None,
                   times_grid=None,
                   normal_draws=None,
                   validate_args=False,
                   name=None):
    """Returns a sample of paths from the correlated Hull-White process.

    Uses exact sampling if `self.mean_reversion` is constant and
    `self.volatility` and `self.corr_matrix` are all `Tensor`s or piecewise
    constant functions, and Euler scheme sampling otherwise.

    The exact sampling implements the algorithm and notations in [1], section
    10.1.6.1.

    Args:
      times: Rank 1 `Tensor` of positive real values. The times at which the
        path points are to be evaluated.
      num_samples: Positive scalar `int32` `Tensor`. The number of paths to
        draw.
      random_type: Enum value of `RandomType`. The type of (quasi)-random
        number generator to use to generate the paths.
        Default value: `None` which maps to the standard pseudo-random numbers.
      seed: Seed for the random number generator. The seed is
        only relevant if `random_type` is one of
        `[STATELESS, PSEUDO, HALTON_RANDOMIZED, PSEUDO_ANTITHETIC,
          STATELESS_ANTITHETIC]`. For `PSEUDO`, `PSEUDO_ANTITHETIC` and
        `HALTON_RANDOMIZED` the seed should be an Python integer. For
        `STATELESS` and  `STATELESS_ANTITHETIC `must be supplied as an integer
        `Tensor` of shape `[2]`.
        Default value: `None` which means no seed is set.
      skip: `int32` 0-d `Tensor`. The number of initial points of the Sobol or
        Halton sequence to skip. Used only when `random_type` is 'SOBOL',
        'HALTON', or 'HALTON_RANDOMIZED', otherwise ignored.
        Default value: `0`.
      time_step: Scalar real `Tensor`. Maximal distance between time grid points
        in Euler scheme. Used only when Euler scheme is applied.
      Default value: `None`.
      times_grid: An optional rank 1 `Tensor` representing time discretization
        grid. If `times` are not on the grid, then the nearest points from the
        grid are used. When supplied, `time_step` and jumps of the piecewise
        constant arguments are ignored.
        Default value: `None`, which means that the times grid is computed using
        `time_step`.  When exact sampling is used, the shape should be equal to
        `[num_time_points + 1]` where `num_time_points` is `tf.shape(times)[0]`
        plus the number of jumps of the Hull-White piecewise constant
        parameters. The grid should include the initial time point which is
        usually set to `0.0`.
      normal_draws: A `Tensor` of shape `[num_samples, num_time_points, dim]`
        and the same `dtype` as `times`. Represents random normal draws to
        compute increments `N(0, t_{n+1}) - N(0, t_n)`. When supplied,
        `num_samples` argument is ignored and the first dimensions of
        `normal_draws` is used instead. When exact sampling is used,
        `num_time_points` should be equal to `tf.shape(times)[0]` plus the
        number of jumps of the Hull-White piecewise constant  parameters.
        Default value: `None` which means that the draws are generated by the
        algorithm.
      validate_args: Python `bool`. When `True` and `normal_draws` are supplied,
        checks that `tf.shape(normal_draws)[1]` is equal to the total number of
        time steps performed by the sampler.
        When `False` invalid dimension may silently render incorrect outputs.
        Default value: `False`.
      name: Python string. The name to give this op.
        Default value: `sample_paths`.

    Returns:
      A `Tensor` of shape [num_samples, k, dim] where `k` is the size
      of the `times` and `dim` is the dimension of the process.

    Raises:
      ValueError:
        (a) If `times` has rank different from `1`.
        (b) If Euler scheme is used by times is not supplied.
        (c) When neither `times_grid` nor `time_step` are supplied and Euler
          scheme is used.
        (d) If `normal_draws` is supplied and `dim` is mismatched.
      tf.errors.InvalidArgumentError: If `normal_draws` is supplied and the
        number of time steps implied by `times_grid` or `times_step` is
        mismatched.
    """
    # Note: all the notations below are the same as in [2].
    name = name or self._name + '_sample_path'
    with tf.name_scope(name):
      times = tf.convert_to_tensor(times, self._dtype, name='times')
      if times_grid is not None:
        times_grid = tf.convert_to_tensor(times_grid, self._dtype,
                                          name='times_grid')
      if len(times.shape) != 1:
        raise ValueError('`times` should be a rank 1 Tensor. '
                         'Rank is {} instead.'.format(len(times.shape)))
      if self._sample_with_generic:
        if time_step is None and times_grid is None:
          raise ValueError(
              'Either `time_step` or `times_grid` has to be specified when '
              'at least one of the parameters is a generic callable.')
        initial_state = self._instant_forward_rate_fn(0.0)
        return euler_sampling.sample(dim=self._dim,
                                     drift_fn=self._drift_fn,
                                     volatility_fn=self._volatility_fn,
                                     times=times,
                                     time_step=time_step,
                                     num_samples=num_samples,
                                     initial_state=initial_state,
                                     random_type=random_type,
                                     seed=seed,
                                     skip=skip,
                                     times_grid=times_grid,
                                     normal_draws=normal_draws,
                                     dtype=self._dtype)
      if normal_draws is not None:
        normal_draws = tf.convert_to_tensor(normal_draws, dtype=self._dtype,
                                            name='normal_draws')
        # Shape [num_time_points, num_samples, dim]
        normal_draws = tf.transpose(normal_draws, [1, 0, 2])
        num_samples = tf.shape(normal_draws)[1]
        draws_dim = normal_draws.shape[2]
        if self._dim != draws_dim:
          raise ValueError(
              '`dim` should be equal to `normal_draws.shape[2]` but are '
              '{0} and {1} respectively'.format(self._dim, draws_dim))
      return self._sample_paths(
          times=times, num_samples=num_samples, random_type=random_type,
          normal_draws=normal_draws,
          skip=skip, seed=seed, validate_args=validate_args,
          times_grid=times_grid)

  def sample_discount_curve_paths(
      self,
      times,
      curve_times,
      num_samples=1,
      random_type=None,
      seed=None,
      skip=0,
      time_step=None,
      times_grid=None,
      normal_draws=None,
      validate_args=False,
      name=None):
    """Returns a sample of simulated discount curves for the Hull-white model.

    ### References:
      [1]: Leif B.G. Andersen and Vladimir V. Piterbarg. Interest Rate Modeling,
      Volume II: Term Structure Models. 2010.

    Args:
      times: Rank 1 `Tensor` of positive real values. The times at which the
        discount curves are to be evaluated.
      curve_times: Rank 1 `Tensor` of positive real values. The maturities
        at which discount curve is computed at each simulation time.
      num_samples: Positive scalar `int`. The number of paths to draw.
      random_type: Enum value of `RandomType`. The type of (quasi)-random
        number generator to use to generate the paths.
        Default value: None which maps to the standard pseudo-random numbers.
      seed: Seed for the random number generator. The seed is
        only relevant if `random_type` is one of
        `[STATELESS, PSEUDO, HALTON_RANDOMIZED, PSEUDO_ANTITHETIC,
          STATELESS_ANTITHETIC]`. For `PSEUDO`, `PSEUDO_ANTITHETIC` and
        `HALTON_RANDOMIZED` the seed should be an Python integer. For
        `STATELESS` and  `STATELESS_ANTITHETIC` must be supplied as an integer
        `Tensor` of shape `[2]`.
        Default value: `None` which means no seed is set.
      skip: `int32` 0-d `Tensor`. The number of initial points of the Sobol or
        Halton sequence to skip. Used only when `random_type` is 'SOBOL',
        'HALTON', or 'HALTON_RANDOMIZED', otherwise ignored.
        Default value: `0`.
      time_step: Scalar real `Tensor`. Maximal distance between time grid points
        in Euler scheme. Used only when Euler scheme is applied.
      Default value: `None`.
      times_grid: An optional rank 1 `Tensor` representing time discretization
        grid. If `times` are not on the grid, then the nearest points from the
        grid are used. When supplied, `time_step` and jumps of the piecewise
        constant arguments are ignored.
        Default value: `None`, which means that the times grid is computed using
        `time_step`.  When exact sampling is used, the shape should be equal to
        `[num_time_points + 1]` where `num_time_points` is `tf.shape(times)[0]`
        plus the number of jumps of the Hull-White piecewise constant
        parameters. The grid should include the initial time point which is
        usually set to `0.0`.
      normal_draws: A `Tensor` of shape `[num_samples, num_time_points, dim]`
        and the same `dtype` as `times`. Represents random normal draws to
        compute increments `N(0, t_{n+1}) - N(0, t_n)`. When supplied,
        `num_samples` argument is ignored and the first dimensions of
        `normal_draws` is used instead. When exact sampling is used,
        `num_time_points` should be equal to `tf.shape(times)[0]` plus the
        number of jumps of the Hull-White piecewise constant parameters.
        Default value: `None` which means that the draws are generated by the
        algorithm.
      validate_args: Python `bool`. When `True` and `normal_draws` are supplied,
        checks that `tf.shape(normal_draws)[1]` is equal to the total number of
        time steps performed by the sampler.
        When `False` invalid dimension may silently render incorrect outputs.
        Default value: `False`.
      name: Str. The name to give this op.
        Default value: `sample_discount_curve_paths`.

    Returns:
      A tuple containing two `Tensor`s. The first element is a `Tensor` of
      shape [num_samples, m, k, dim] and contains the simulated bond curves
      where `m` is the size of `curve_times`, `k` is the size of `times` and
      `dim` is the dimension of the process. The second element is a `Tensor`
      of shape [num_samples, k, dim] and contains the simulated short rate
      paths.

    Raises:
      ValueError:
        (a) If `times` has rank different from `1`.
        (b) If Euler scheme is used by times is not supplied.
        (c) When neither `times_grid` nor `time_step` are supplied and Euler
          scheme is used.
        (d) If `normal_draws` is supplied and `dim` is mismatched.
      tf.errors.InvalidArgumentError: If `normal_draws` is supplied and the
        number of time steps implied by `times_grid` or `times_step` is
        mismatched.
    """
    name = name or self._name + '_sample_discount_curve_paths'
    with tf.name_scope(name):
      times = tf.convert_to_tensor(times, self._dtype, name='times')
      curve_times = tf.convert_to_tensor(curve_times, self._dtype,
                                         name='curve_times')
      if times_grid is not None:
        times_grid = tf.convert_to_tensor(times_grid, self._dtype,
                                          name='times_grid')
      mean_reversion = self._mean_reversion(times)
      volatility = self._volatility(times)
      y_t = self._compute_yt(times, mean_reversion, volatility)
      rate_paths = self.sample_paths(
          times=times,
          num_samples=num_samples,
          random_type=random_type,
          skip=skip,
          time_step=time_step,
          times_grid=times_grid,
          normal_draws=normal_draws,
          validate_args=validate_args,
          seed=seed)
      short_rate = tf.expand_dims(rate_paths, axis=1)

      # Reshape all `Tensor`s so that they have the dimensions same as (or
      # broadcastable to) the output shape
      # ([num_smaples,num_curve_times,num_sim_times,dim]).
      num_curve_nodes = curve_times.shape.as_list()[0]  # m
      num_sim_steps = times.shape.as_list()[0]  # k
      times = tf.reshape(
          tf.repeat(tf.expand_dims(times, axis=-1), self._dim, axis=-1),
          (1, 1, num_sim_steps, self._dim))
      curve_times = tf.reshape(curve_times, (1, num_curve_nodes, 1, 1))
      curve_times = tf.repeat(curve_times, self._dim, axis=-1)

      mean_reversion = tf.reshape(
          mean_reversion, (1, 1, self._dim, num_sim_steps))
      # Transpose so the `dim` is the trailing dimension.
      mean_reversion = tf.transpose(mean_reversion, [0, 1, 3, 2])

      # Calculate the variable `y(t)` (described in [1], section 10.1.6.1)
      # so that we have the full Markovian state to compute the P(t,T).
      y_t = tf.reshape(tf.transpose(y_t), (1, 1, num_sim_steps, self._dim))

      return self._bond_reconstitution(times, times + curve_times,
                                       mean_reversion, short_rate,
                                       y_t), rate_paths

  def discount_bond_price(self, short_rate, times, maturities, name=None):
    """Returns zero-coupon bond prices `P(t,T)` conditional on `r(t)`.

    Args:
      short_rate: A `Tensor` of real dtype and shape `batch_shape + [dim]`
        specifying the short rate `r(t)`.
      times: A `Tensor` of real dtype and shape `batch_shape`. The time `t`
        at which discount bond prices are computed.
      maturities: A `Tensor` of real dtype and shape `batch_shape`. The time
        to maturity of the discount bonds.
      name: Str. The name to give this op.
        Default value: `discount_bond_prices`.

    Returns:
      A `Tensor` of real dtype and the same shape as `batch_shape + [dim]`
      containing the price of zero-coupon bonds.
    """
    name = name or self._name + '_discount_bond_prices'
    with tf.name_scope(name):
      short_rate = tf.convert_to_tensor(short_rate, self._dtype)
      times = tf.convert_to_tensor(times, self._dtype)
      maturities = tf.convert_to_tensor(maturities, self._dtype)
      # Flatten it because `PiecewiseConstantFunction` expects the first
      # dimension to be broadcastable to [dim]
      input_shape_times = times.shape.as_list()
      times = tf.reshape(times, shape=[-1])
      # The shape of `mean_reversion` will be (dim,n) where `n` is the number
      # of elements in `times`.
      mean_reversion = self._mean_reversion(times)
      volatility = self._volatility(times)
      y_t = self._compute_yt(times, mean_reversion, volatility)
      times = tf.reshape(times, input_shape_times + [1])
      maturities = tf.reshape(maturities, input_shape_times + [1])
      mean_reversion = tf.reshape(tf.transpose(mean_reversion),
                                  input_shape_times + [self._dim])
      y_t = tf.reshape(tf.transpose(y_t), input_shape_times + [self._dim])
      values = self._bond_reconstitution(
          times, maturities, mean_reversion, short_rate, y_t)
      return values

  def instant_forward_rate(self, t):
    """Returns the instantaneous forward rate."""
    return self._instant_forward_rate_fn(t)

  def _sample_paths(self,
                    times,
                    num_samples,
                    random_type,
                    skip,
                    seed,
                    normal_draws=None,
                    times_grid=None,
                    validate_args=False):
    """Returns a sample of paths from the process."""
    # Note: all the notations below are the same as in [1].
    num_requested_times = times.shape[0]
    params = [self._mean_reversion, self._volatility]
    if self._corr_matrix is not None:
      params = params + [self._corr_matrix]
    times, keep_mask = _prepare_grid(
        times, times_grid, *params)
    # Add zeros as a starting location
    dt = times[1:] - times[:-1]
    if dt.shape.is_fully_defined():
      steps_num = dt.shape.as_list()[-1]
    else:
      steps_num = tf.shape(dt)[-1]
      # TODO(b/148133811): Re-enable Sobol test when TF 2.2 is released.
      if random_type == random.RandomType.SOBOL:
        raise ValueError('Sobol sequence for Euler sampling is temporarily '
                         'unsupported when `time_step` or `times` have a '
                         'non-constant value')
    if normal_draws is None:
      # In order to use low-discrepancy random_type we need to generate the
      # sequence of independent random normals upfront. We also precompute
      # random numbers for stateless random type in order to ensure independent
      # samples for multiple function calls whith different seeds.
      if random_type in (random.RandomType.SOBOL,
                         random.RandomType.HALTON,
                         random.RandomType.HALTON_RANDOMIZED,
                         random.RandomType.STATELESS,
                         random.RandomType.STATELESS_ANTITHETIC):
        normal_draws = utils.generate_mc_normal_draws(
            num_normal_draws=self._dim, num_time_steps=steps_num,
            num_sample_paths=num_samples, random_type=random_type,
            seed=seed,
            dtype=self._dtype, skip=skip)
      else:
        normal_draws = None
    else:
      if validate_args:
        draws_times = tf.shape(normal_draws)[0]
        asserts = tf.assert_equal(
            draws_times, tf.shape(times)[0] - 1,  # We have added `0` to `times`
            message='`tf.shape(normal_draws)[1]` should be equal to the '
                    'number of all `times` plus the number of all jumps of '
                    'the piecewise constant parameters.')
        with tf.compat.v1.control_dependencies([asserts]):
          normal_draws = tf.identity(normal_draws)
    # The below is OK because we support exact discretization with piecewise
    # constant mr and vol.
    mean_reversion = self._mean_reversion(times)
    volatility = self._volatility(times)
    if self._corr_matrix is not None:
      corr_matrix = _get_parameters(
          times + tf.math.reduce_min(dt) / 2, self._corr_matrix)[0]
      corr_matrix_root = tf.linalg.cholesky(corr_matrix)
    else:
      corr_matrix_root = None

    exp_x_t = self._conditional_mean_x(times, mean_reversion, volatility)
    var_x_t = self._conditional_variance_x(times, mean_reversion, volatility)
    if self._dim == 1:
      mean_reversion = tf.expand_dims(mean_reversion, axis=0)

    cond_fn = lambda i, *args: i < tf.size(dt)
    def body_fn(i, written_count,
                current_x,
                rate_paths):
      """Simulate hull-white process to the next time point."""
      if normal_draws is None:
        normals = random.mv_normal_sample(
            (num_samples,),
            mean=tf.zeros((self._dim,), dtype=mean_reversion.dtype),
            random_type=random_type, seed=seed)
      else:
        normals = normal_draws[i]

      if corr_matrix_root is not None:
        normals = tf.linalg.matvec(corr_matrix_root[i], normals)

      next_x = (tf.math.exp(-tf.transpose(mean_reversion)[i + 1] * dt[i])
                * current_x
                + tf.transpose(exp_x_t)[i]
                + tf.math.sqrt(tf.transpose(var_x_t)[i]) * normals)
      f_0_t = self._instant_forward_rate_fn(times[i + 1])

      # Update `rate_paths`
      rate_paths = utils.maybe_update_along_axis(
          tensor=rate_paths,
          do_update=keep_mask[i + 1],
          ind=written_count,
          axis=1,
          new_tensor=tf.expand_dims(next_x, axis=1) + f_0_t)
      written_count += tf.cast(keep_mask[i + 1], dtype=tf.int32)
      return (i + 1, written_count, next_x, rate_paths)

    rate_paths = tf.zeros((num_samples, num_requested_times, self._dim),
                          dtype=self._dtype)
    # Include initial state, if necessary
    f0_t = self._instant_forward_rate_fn(times[0])
    rate_paths = utils.maybe_update_along_axis(
        tensor=rate_paths,
        do_update=keep_mask[0],
        ind=0,
        axis=1,
        new_tensor=f0_t)
    written_count = tf.cast(keep_mask[0], dtype=tf.int32)
    initial_x = tf.zeros((num_samples, self._dim), dtype=self._dtype)
    # TODO(b/157232803): Use tf.cumsum instead?
    _, _, _, rate_paths = tf.while_loop(
        cond_fn, body_fn, (0, written_count, initial_x, rate_paths))

    return rate_paths

  def _bond_reconstitution(self,
                           times,
                           maturities,
                           mean_reversion,
                           short_rate,
                           y_t):
    """Compute discount bond prices using Eq. 10.18 in Ref [2]."""
    f_0_t = self._instant_forward_rate_fn(times)
    x_t = short_rate - f_0_t
    p_0_t = tf.math.exp(-self._initial_discount_rate_fn(times) * times)
    p_0_t_tau = tf.math.exp(
        -self._initial_discount_rate_fn(maturities) *
        (maturities)) / p_0_t
    g_t_tau = (1. - tf.math.exp(
        -mean_reversion * (maturities - times))) / mean_reversion
    term1 = x_t * g_t_tau
    term2 = y_t * g_t_tau**2
    p_t_tau = p_0_t_tau * tf.math.exp(-term1 - 0.5 * term2)
    return p_t_tau

  def _exact_discretization_setup(self, dim):
    """Initial setup for efficient computations."""
    self._zero_padding = tf.zeros((dim, 1), dtype=self._dtype)
    self._jump_locations = tf.concat(
        [self._volatility.jump_locations(),
         self._mean_reversion.jump_locations()], axis=-1)
    self._jump_values_vol = self._volatility(self._jump_locations)
    self._jump_values_mr = self._mean_reversion(self._jump_locations)
    if dim == 1:
      self._padded_knots = tf.concat([
          self._zero_padding,
          tf.expand_dims(self._jump_locations[:-1], axis=0)
      ], axis=1)
      self._jump_values_vol = tf.expand_dims(self._jump_values_vol, axis=0)
      self._jump_values_mr = tf.expand_dims(self._jump_values_mr, axis=0)
      self._jump_locations = tf.expand_dims(self._jump_locations, axis=0)

    else:
      self._padded_knots = tf.concat(
          [self._zero_padding, self._jump_locations[:, :-1]], axis=1)

  def _compute_yt(self, t, mr_t, sigma_t):
    """Computes y(t) as described in [1], section 10.1.6.1."""
    # Shape [dim, num_times]
    t = tf.broadcast_to(t, tf.concat([[self._dim], tf.shape(t)], axis=-1))
    time_index = tf.searchsorted(self._jump_locations, t)
    y_between_vol_knots = self._y_integral(
        self._padded_knots, self._jump_locations, self._jump_values_vol,
        self._jump_values_mr)
    y_at_vol_knots = tf.concat(
        [self._zero_padding,
         utils.cumsum_using_matvec(y_between_vol_knots)], axis=1)

    vn = tf.concat(
        [self._zero_padding, self._jump_locations], axis=1)
    y_t = self._y_integral(
        tf.gather(vn, time_index, batch_dims=1), t, sigma_t, mr_t)
    y_t = y_t + tf.gather(y_at_vol_knots, time_index, batch_dims=1)
    return tf.math.exp(-2 * mr_t * t) * y_t

  def _conditional_mean_x(self, t, mr_t, sigma_t):
    """Computes the drift term in [1], Eq. 10.39."""
    # Shape [dim, num_times]
    t = tf.broadcast_to(t, tf.concat([[self._dim], tf.shape(t)], axis=-1))
    time_index = tf.searchsorted(self._jump_locations, t)
    vn = tf.concat([self._zero_padding, self._jump_locations], axis=1)
    y_between_vol_knots = self._y_integral(self._padded_knots,
                                           self._jump_locations,
                                           self._jump_values_vol,
                                           self._jump_values_mr)

    y_at_vol_knots = tf.concat(
        [self._zero_padding,
         utils.cumsum_using_matvec(y_between_vol_knots)], axis=1)

    ex_between_vol_knots = self._ex_integral(self._padded_knots,
                                             self._jump_locations,
                                             self._jump_values_vol,
                                             self._jump_values_mr,
                                             y_at_vol_knots[:, :-1])

    ex_at_vol_knots = tf.concat(
        [self._zero_padding,
         utils.cumsum_using_matvec(ex_between_vol_knots)], axis=1)

    c = tf.gather(y_at_vol_knots, time_index, batch_dims=1)
    exp_x_t = self._ex_integral(
        tf.gather(vn, time_index, batch_dims=1), t, sigma_t, mr_t, c)
    exp_x_t = exp_x_t + tf.gather(ex_at_vol_knots, time_index, batch_dims=1)
    exp_x_t = (exp_x_t[:, 1:] - exp_x_t[:, :-1]) * tf.math.exp(
        -tf.broadcast_to(mr_t, t.shape)[:, 1:] * t[:, 1:])
    return exp_x_t

  def _y_integral(self, t0, t, vol, k):
    """Computes int_t0^t sigma(u)^2 exp(2*k*u) du."""
    return (vol * vol) / (2 * k) * (
        tf.math.exp(2 * k * t) - tf.math.exp(2 * k * t0))

  def _ex_integral(self, t0, t, vol, k, y_t0):
    """Function computes the integral for the drift calculation."""
    # Computes int_t0^t (exp(k*s)*y(s)) ds,
    # where y(s)=y(t0) + int_t0^s exp(-2*(s-u)) vol(u)^2 du."""
    value = (
        tf.math.exp(k * t) - tf.math.exp(k * t0) + tf.math.exp(2 * k * t0) *
        (tf.math.exp(-k * t) - tf.math.exp(-k * t0)))
    value = value * vol**2 / (2 * k * k) + y_t0 * (tf.math.exp(-k * t0) -
                                                   tf.math.exp(-k * t)) / k
    return value

  def _conditional_variance_x(self, t, mr_t, sigma_t):
    """Computes the variance of x(t), see [1], Eq. 10.41."""
    # Shape [dim, num_times]
    t = tf.broadcast_to(t, tf.concat([[self._dim], tf.shape(t)], axis=-1))
    var_x_between_vol_knots = self._variance_int(self._padded_knots,
                                                 self._jump_locations,
                                                 self._jump_values_vol,
                                                 self._jump_values_mr)
    varx_at_vol_knots = tf.concat(
        [self._zero_padding,
         utils.cumsum_using_matvec(var_x_between_vol_knots)],
        axis=1)

    time_index = tf.searchsorted(self._jump_locations, t)
    vn = tf.concat(
        [self._zero_padding,
         self._jump_locations], axis=1)

    var_x_t = self._variance_int(
        tf.gather(vn, time_index, batch_dims=1), t, sigma_t, mr_t)
    var_x_t = var_x_t + tf.gather(varx_at_vol_knots, time_index, batch_dims=1)

    var_x_t = (var_x_t[:, 1:] - var_x_t[:, :-1]) * tf.math.exp(
        -2 * tf.broadcast_to(mr_t, t.shape)[:, 1:] * t[:, 1:])
    return var_x_t

  def _variance_int(self, t0, t, vol, k):
    """Computes int_t0^t exp(2*k*s) vol(s)^2 ds."""
    return vol * vol / (2 * k) * (
        tf.math.exp(2 * k * t) - tf.math.exp(2 * k * t0))


def _get_parameters(times, *params):
  """Gets parameter values at at specified `times`."""
  res = []
  for param in params:
    if isinstance(param, piecewise.PiecewiseConstantFunc):
      jump_locations = param.jump_locations()
      if len(jump_locations.shape) > 1:
        # If `jump_locations` has batch dimension, transpose the result
        # Shape [num_times, dim]
        res.append(tf.transpose(param(times)))
      else:
        # Shape [num_times, dim]
        res.append(param(times))
    elif callable(param):
      # Used only in drift and volatility computation.
      # Here `times` is of shape [1]
      t = tf.squeeze(times)
      # The result has to have shape [1] + param.shape
      res.append(tf.expand_dims(param(t), 0))
    else:
      res.append(param + tf.zeros(times.shape + param.shape, dtype=times.dtype))
  return res


def _prepare_grid(times, times_grid, *params):
  """Prepares grid of times for path generation.

  Args:
    times:  Rank 1 `Tensor` of increasing positive real values. The times at
      which the path points are to be evaluated.
    times_grid: An optional rank 1 `Tensor` representing time discretization
      grid. If `times` are not on the grid, then the nearest points from the
      grid are used.
    *params: Parameters of the Heston model. Either scalar `Tensor`s of the
      same `dtype` or instances of `PiecewiseConstantFunc`.

  Returns:
    Tuple `(all_times, mask)`.
    `all_times` is a 1-D real `Tensor` containing all points from 'times`, the
    uniform grid of points between `[0, times[-1]]` with grid size equal to
    `time_step`, and jump locations of piecewise constant parameters The
    `Tensor` is sorted in ascending order and may contain duplicates.
    `mask` is a boolean 1-D `Tensor` of the same shape as 'all_times', showing
    which elements of 'all_times' correspond to THE values from `times`.
    Guarantees that times[0]=0 and mask[0]=False.
  """
  if times_grid is None:
    additional_times = []
    for param in params:
      if hasattr(param, 'is_piecewise_constant'):
        if param.is_piecewise_constant:
          # Flatten all jump locations
          additional_times.append(tf.reshape(param.jump_locations(), [-1]))
    zeros = tf.constant([0], dtype=times.dtype)
    all_times = tf.concat([zeros] + [times] + additional_times, axis=0)
    all_times = tf.sort(all_times)
    time_indices = tf.searchsorted(all_times, times, out_type=tf.int32)
  else:
    all_times = times_grid
    time_indices = tf.searchsorted(times_grid, times, out_type=tf.int32)
    # Adjust indices to bring `times` closer to `times_grid`.
    times_diff_1 = tf.gather(times_grid, time_indices) - times
    times_diff_2 = tf.gather(times_grid, tf.nn.relu(time_indices-1)) - times
    time_indices = tf.where(
        tf.math.abs(times_diff_2) > tf.math.abs(times_diff_1),
        time_indices,
        tf.nn.relu(time_indices - 1))
  # Create a boolean mask to identify the iterations that have to be recorded.
  mask_sparse = tf.sparse.SparseTensor(
      indices=tf.expand_dims(
          tf.cast(time_indices, dtype=tf.int64), axis=1),
      values=tf.fill(tf.shape(times), True),
      dense_shape=tf.shape(all_times, out_type=tf.int64))
  mask = tf.sparse.to_dense(mask_sparse)
  return all_times, mask


def _input_type(param, dim, dtype, name):
  """Checks if the input parameter is a callable or piecewise constant."""
  # If the parameter is callable but not a piecewise constant use
  # generic sampling method (e.g., Euler).
  sample_with_generic = False
  if hasattr(param, 'is_piecewise_constant'):
    if param.is_piecewise_constant:
      jumps_shape = param.jump_locations().shape
      if len(jumps_shape) > 2:
        raise ValueError(
            'Batch rank of `jump_locations` should be `1` for all piecewise '
            'constant arguments but {} instead'.format(len(jumps_shape[:-1])))
      if len(jumps_shape) == 2:
        if dim != jumps_shape[0]:
          raise ValueError(
              'Batch shape of `jump_locations` should be either empty or '
              '`[{0}]` but `[{1}]` instead'.format(dim, jumps_shape[0]))
      if name == 'mean_reversion' and jumps_shape[0] > 0:
        # Exact discretization currently not supported with time-dependent mr
        sample_with_generic = True
      return param, sample_with_generic
    else:
      sample_with_generic = True
  elif callable(param):
    sample_with_generic = True
  else:
    # Otherwise, input is a `Tensor`, return a `PiecewiseConstantFunc`.
    param = tf.convert_to_tensor(param, dtype=dtype, name=name)
    param_shape = param.shape.as_list()
    param_rank = param.shape.rank
    if param_shape[-1] != dim:
      # This is an error, we need as many parameters as the number of `dim`
      raise ValueError(
          'Length of {} ({}) should be the same as `dims`({}).'.format(
              name, param_shape[0], dim))
    if param_rank == 2:
      # This is when the parameter is a correlation matrix
      jump_locations = []
      values = tf.expand_dims(param, axis=0)
    else:
      jump_locations = [] if dim == 1 else [[]] * dim
      values = param if dim == 1 else tf.expand_dims(param, axis=-1)
    param = piecewise.PiecewiseConstantFunc(
        jump_locations=jump_locations, values=values,
        dtype=dtype)

  return param, sample_with_generic
