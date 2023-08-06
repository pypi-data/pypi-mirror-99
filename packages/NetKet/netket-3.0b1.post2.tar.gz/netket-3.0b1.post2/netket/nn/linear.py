# Copyright 2021 The Flax Authors.
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

"""Linear modules."""

from dataclasses import field

from typing import Any, Callable, Iterable, Optional, Tuple, Union
from functools import partial

import flax
from flax.linen.module import Module, compact
from netket.nn.initializers import lecun_normal, normal, variance_scaling, zeros
from netket import jax as nkjax
from netket.graph import AbstractGraph

from jax import lax
import jax.numpy as jnp
import numpy as np


PRNGKey = Any
Shape = Iterable[int]
Dtype = Any  # this could be a real type?
Array = Any


default_kernel_init = normal(stddev=0.01)
# complex_kernel_init = lecun_normal()


def _normalize_axes(axes, ndim):
    # A tuple by convention. len(axes_tuple) then also gives the rank efficiently.
    return tuple([ax if ax >= 0 else ndim + ax for ax in axes])


def _canonicalize_tuple(x):
    if isinstance(x, Iterable):
        return tuple(x)
    else:
        return (x,)


class DenseGeneral(Module):
    """A linear transformation with flexible axes.

    Attributes:
      features: int or tuple with number of output features.
      axis: int or tuple with axes to apply the transformation on. For instance,
        (-2, -1) will apply the transformation to the last two axes.
      batch_dims: tuple with batch axes.
      use_bias: whether to add a bias to the output (default: True).
      dtype: the dtype of the computation (default: float32).
      kernel_init: initializer function for the weight matrix.
      bias_init: initializer function for the bias.
      precision: numerical precision of the computation see `jax.lax.Precision`
        for details.
    """

    features: Union[int, Iterable[int]]
    axis: Union[int, Iterable[int]] = -1
    batch_dims: Iterable[int] = ()
    use_bias: bool = True
    dtype: Dtype = jnp.float64
    kernel_init: Callable[[PRNGKey, Shape, Dtype], Array] = default_kernel_init
    bias_init: Callable[[PRNGKey, Shape, Dtype], Array] = zeros
    precision: Any = None

    @compact
    def __call__(self, inputs: Array) -> Array:
        """Applies a linear transformation to the inputs along multiple dimensions.
        Args:
          inputs: The nd-array to be transformed.
        Returns:
          The transformed input.
        """
        features = _canonicalize_tuple(self.features)
        axis = _canonicalize_tuple(self.axis)
        batch_dims = _canonicalize_tuple(self.batch_dims)
        if batch_dims:
            max_dim = np.max(batch_dims)
            if set(batch_dims) != set(range(max_dim + 1)):
                raise ValueError(
                    "batch_dims %s must be consecutive leading "
                    "dimensions starting from 0." % str(batch_dims)
                )

        dtype = jnp.promote_types(inputs.dtype, self.dtype)

        inputs = jnp.asarray(inputs, dtype)

        ndim = inputs.ndim
        n_batch_dims = len(batch_dims)
        axis = _normalize_axes(axis, ndim)
        batch_dims = _normalize_axes(batch_dims, ndim)
        n_axis, n_features = len(axis), len(features)

        def kernel_init_wrap(rng, shape, dtype=jnp.float32):
            size_batch_dims = np.prod(shape[:n_batch_dims], dtype=np.int32)
            flat_shape = (
                np.prod(shape[n_batch_dims : n_axis + n_batch_dims]),
                np.prod(shape[-n_features:]),
            )
            kernel = jnp.concatenate(
                [
                    self.kernel_init(rng, flat_shape, dtype)
                    for _ in range(size_batch_dims)
                ],
                axis=0,
            )
            return jnp.reshape(kernel, shape)

        batch_shape = tuple([inputs.shape[ax] for ax in batch_dims])
        kernel_shape = tuple([inputs.shape[ax] for ax in axis]) + features
        kernel = self.param("kernel", kernel_init_wrap, batch_shape + kernel_shape)
        kernel = jnp.asarray(kernel, dtype)

        batch_ind = tuple(range(n_batch_dims))
        contract_ind = tuple(range(n_batch_dims, n_axis + n_batch_dims))
        out = lax.dot_general(
            inputs,
            kernel,
            ((axis, contract_ind), (batch_dims, batch_ind)),
            precision=self.precision,
        )

        if self.use_bias:

            def bias_init_wrap(rng, shape, dtype=jnp.float32):
                size_batch_dims = np.prod(shape[:n_batch_dims], dtype=np.int32)
                flat_shape = (np.prod(shape[-n_features:]),)
                bias = jnp.concatenate(
                    [
                        self.bias_init(rng, flat_shape, dtype)
                        for _ in range(size_batch_dims)
                    ],
                    axis=0,
                )
                return jnp.reshape(bias, shape)

            bias = self.param("bias", bias_init_wrap, batch_shape + features)

            # Reshape bias for broadcast.
            expand_dims = sorted(set(range(inputs.ndim)) - set(axis) - set(batch_dims))
            for ax in expand_dims:
                bias = jnp.expand_dims(bias, ax)
            bias = jnp.asarray(bias, dtype)
            out = out + bias
        return out


class Dense(Module):
    """A linear transformation applied over the last dimension of the input.

    Attributes:
      features: the number of output features.
      use_bias: whether to add a bias to the output (default: True).
      dtype: the dtype of the computation (default: float32).
      precision: numerical precision of the computation see `jax.lax.Precision`
        for details.
      kernel_init: initializer function for the weight matrix.
      bias_init: initializer function for the bias.
    """

    features: int
    use_bias: bool = True
    dtype: Any = jnp.float64
    precision: Any = None
    kernel_init: Callable[[PRNGKey, Shape, Dtype], Array] = default_kernel_init
    bias_init: Callable[[PRNGKey, Shape, Dtype], Array] = zeros

    @compact
    def __call__(self, inputs: Array) -> Array:
        """Applies a linear transformation to the inputs along the last dimension.
        Args:
          inputs: The nd-array to be transformed.
        Returns:
          The transformed input.
        """
        dtype = jnp.promote_types(inputs.dtype, self.dtype)

        inputs = jnp.asarray(inputs, dtype)
        kernel = self.param(
            "kernel", self.kernel_init, (inputs.shape[-1], self.features), self.dtype
        )
        kernel = jnp.asarray(kernel, dtype)
        y = lax.dot_general(
            inputs,
            kernel,
            (((inputs.ndim - 1,), (0,)), ((), ())),
            precision=self.precision,
        )
        if self.use_bias:
            bias = self.param("bias", self.bias_init, (self.features,), self.dtype)
            bias = jnp.asarray(bias, dtype)
            y = y + bias
        return y


class DenseSymm(Module):
    """A symmetrized linear transformation applied over the last dimension of the input.
    This layer uses a reduced number of parameters, which are arranged so that the full
    affine transformation is invariant under all of the given permutations when applied to s.

    See :func:`~netket.nn.create_DenseSymm` for a more convenient constructor.
    """

    permutations: Callable[[], Array]
    """Callable returning a sequence of permutations over which the layer should be invariant."""
    features: int
    """The number of symmetry-reduced features. The full output size is len(permutations) * features."""
    use_bias: bool = True
    """Whether to add a bias to the output (default: True)."""
    dtype: Any = jnp.float64
    """The dtype of the weights."""
    precision: Any = None
    """numerical precision of the computation see `jax.lax.Precision`for details."""

    kernel_init: Callable[[PRNGKey, Shape, Dtype], Array] = default_kernel_init
    """Initializer for the Dense layer matrix."""
    bias_init: Callable[[PRNGKey, Shape, Dtype], Array] = zeros
    """Initializer for the bias."""

    def setup(self):
        perms = self.permutations()

        self.n_symm, self.n_sites = perms.shape
        self.n_hidden = self.features * self.n_symm

        # symmetrization tensor, maps Wsymm to full W
        # note that this should be a sparse object, once jax supports them
        def symmetrizer_ijkl(i, j, k, l):
            jsymm = np.floor_divide(j, self.n_symm)
            cond_k = k == jnp.asarray(perms)[j % self.n_symm, i]
            cond_l = l == jsymm
            return jnp.asarray(jnp.logical_and(cond_k, cond_l), dtype=int)

        self.symmetrizer = jnp.array(
            np.fromfunction(
                symmetrizer_ijkl,
                shape=(self.n_sites, self.n_hidden, self.n_sites, self.features),
                dtype=int,
            ),
            dtype=self.dtype,
        ).reshape(-1, self.features * self.n_sites)

    def full_kernel(self, kernel):
        """
        Converts the symmetry-reduced kernel of shape (n_sites, features) to
        the full Dense kernel of shape (n_sites, features * n_symm).
        """
        # equivalent to: kernel = jnp.einsum("ijkl,kl->ij", self.symmetrizer, kernel)
        # for appropriately shaped symmetrizer
        kvec = kernel.reshape(-1)
        return jnp.matmul(self.symmetrizer, kvec).reshape(self.n_sites, -1)

    def full_bias(self, bias):
        """
        Convert symmetry-reduced bias of shape (features,) to the full bias of
        shape (n_symm * features,).
        """
        return jnp.repeat(bias, self.n_symm)

    @compact
    def __call__(self, inputs: Array) -> Array:
        """Applies the symmetrized linear transformation to the inputs along the last dimension.
        Args:
          inputs: The nd-array to be transformed.
        Returns:
          The transformed input.
        """
        dtype = jnp.promote_types(inputs.dtype, self.dtype)
        inputs = jnp.asarray(inputs, dtype)

        kernel = self.param(
            "kernel", self.kernel_init, (inputs.shape[-1], self.features), self.dtype
        )
        kernel = self.full_kernel(kernel)
        kernel = jnp.asarray(kernel, dtype)

        y = lax.dot_general(
            inputs,
            kernel,
            (((inputs.ndim - 1,), (0,)), ((), ())),
            precision=self.precision,
        )

        if self.use_bias:
            bias = self.param("bias", self.bias_init, (self.features,), self.dtype)
            bias = jnp.asarray(self.full_bias(bias), dtype)
            y += bias

        return y


def create_DenseSymm(
    permutations: Union[Callable[[], Array], AbstractGraph, Array], *args, **kwargs
):
    """A symmetrized linear transformation applied over the last dimension of the input.
    This layer uses a reduced number of parameters, which are arranged so that the full
    affine transformation is invariant under all of the given permutations when applied to s.

    This is a convenience wrapper for creating a :ref:`netket.nn.DenseSymm` layer.

    Arguments:
      permutations: Sequence of permutations over which the layer should be invariant.
        Should be either an array-like object of shape (n_permutations, input_size),
        an argument-less callable returning such an array, or :ref:`netket.graph.AbstractGraph`, in which
        case the graph automorphisms are used.

    See :ref:`netket.nn.DenseSymm` for the remaining parameters.
    """
    if isinstance(permutations, Callable):
        perm_fn = permutations
    elif isinstance(permutations, AbstractGraph):
        perm_fn = lambda: jnp.asarray(permutations.automorphisms())
    else:
        permutations = jnp.asarray(permutations)
        if not permutations.ndim == 2:
            raise ValueError(
                "permutations must be an array of shape (#permutations, #sites)."
            )
        perm_fn = lambda: permutations

    return DenseSymm(permutations=perm_fn, *args, **kwargs)


class Conv(Module):
    """Convolution Module wrapping lax.conv_general_dilated.

    Attributes:
      features: number of convolution filters.
      kernel_size: shape of the convolutional kernel. For 1D convolution,
        the kernel size can be passed as an integer. For all other cases, it must
        be a sequence of integers.
      strides: a sequence of `n` integers, representing the inter-window
        strides.
      padding: either the string `'SAME'`, the string `'VALID'`, or a sequence
        of `n` `(low, high)` integer pairs that give the padding to apply before
        and after each spatial dimension.
      input_dilation: `None`, or a sequence of `n` integers, giving the
        dilation factor to apply in each spatial dimension of `inputs`.
        Convolution with input dilation `d` is equivalent to transposed
        convolution with stride `d`.
      kernel_dilation: `None`, or a sequence of `n` integers, giving the
        dilation factor to apply in each spatial dimension of the convolution
        kernel. Convolution with kernel dilation is also known as 'atrous
        convolution'.
      feature_group_count: integer, default 1. If specified divides the input
        features into groups.
      use_bias: whether to add a bias to the output (default: True).
      dtype: the dtype of the computation (default: float32).
      precision: numerical precision of the computation see `jax.lax.Precision`
        for details.
      kernel_init: initializer for the convolutional kernel.
      bias_init: initializer for the bias.
    """

    features: int
    kernel_size: Union[int, Iterable[int]]
    strides: Optional[Iterable[int]] = None
    padding: Union[str, Iterable[Tuple[int, int]]] = "SAME"
    input_dilation: Optional[Iterable[int]] = None
    kernel_dilation: Optional[Iterable[int]] = None
    feature_group_count: int = 1
    use_bias: bool = True
    dtype: Dtype = jnp.float64
    precision: Any = None
    kernel_init: Callable[[PRNGKey, Shape, Dtype], Array] = default_kernel_init
    bias_init: Callable[[PRNGKey, Shape, Dtype], Array] = zeros

    @compact
    def __call__(self, inputs: Array) -> Array:
        """Applies a convolution to the inputs.
        Args:
          inputs: input data with dimensions (batch, spatial_dims..., features).
        Returns:
          The convolved data.
        """
        dtype = jnp.promote_types(inputs.dtype, self.dtype)

        inputs = jnp.asarray(inputs, dtype)

        if isinstance(self.kernel_size, int):
            kernel_size = (self.kernel_size,)
        else:
            kernel_size = self.kernel_size

        is_single_input = False
        if inputs.ndim == len(kernel_size) + 1:
            is_single_input = True
            inputs = jnp.expand_dims(inputs, axis=0)

        strides = self.strides or (1,) * (inputs.ndim - 2)

        in_features = inputs.shape[-1]
        assert in_features % self.feature_group_count == 0
        kernel_shape = kernel_size + (
            in_features // self.feature_group_count,
            self.features,
        )
        kernel = self.param("kernel", self.kernel_init, kernel_shape, self.dtype)
        kernel = jnp.asarray(kernel, dtype)

        dimension_numbers = flax.linen.linear._conv_dimension_numbers(inputs.shape)
        y = lax.conv_general_dilated(
            inputs,
            kernel,
            strides,
            self.padding,
            lhs_dilation=self.input_dilation,
            rhs_dilation=self.kernel_dilation,
            dimension_numbers=dimension_numbers,
            feature_group_count=self.feature_group_count,
            precision=self.precision,
        )

        if is_single_input:
            y = jnp.squeeze(y, axis=0)

        if self.use_bias:
            bias = self.param("bias", self.bias_init, (self.features,), self.dtype)
            bias = jnp.asarray(bias, dtype)
            y = y + bias
        return y


class ConvTranspose(Module):
    """Convolution Module wrapping lax.conv_general_dilated.

    Attributes:
      features: number of convolution filters.
      kernel_size: shape of the convolutional kernel. For 1D convolution,
        the kernel size can be passed as an integer. For all other cases, it must
        be a sequence of integers.
      strides: a sequence of `n` integers, representing the inter-window
        strides.
      padding: either the string `'SAME'`, the string `'VALID'`, or a sequence
        of `n` `(low, high)` integer pairs that give the padding to apply before
        and after each spatial dimension.
      kernel_dilation: `None`, or a sequence of `n` integers, giving the
        dilation factor to apply in each spatial dimension of the convolution
        kernel. Convolution with kernel dilation is also known as 'atrous
        convolution'.
      use_bias: whether to add a bias to the output (default: True).
      dtype: the dtype of the computation (default: float32).
      precision: numerical precision of the computation see `jax.lax.Precision`
        for details.
      kernel_init: initializer for the convolutional kernel.
      bias_init: initializer for the bias.
    """

    features: int
    kernel_size: Union[int, Iterable[int]]
    strides: Optional[Iterable[int]] = None
    padding: Union[str, Iterable[Tuple[int, int]]] = "SAME"
    kernel_dilation: Optional[Iterable[int]] = None
    use_bias: bool = True
    dtype: Dtype = jnp.float64
    precision: Any = None
    kernel_init: Callable[[PRNGKey, Shape, Dtype], Array] = default_kernel_init
    bias_init: Callable[[PRNGKey, Shape, Dtype], Array] = zeros

    @compact
    def __call__(self, inputs: Array) -> Array:
        """Applies a transposed convolution to the inputs. Behaviour mirrors of
        `jax.lax.conv_transpose`.
        Args:
          inputs: input data with dimensions (batch, spatial_dims..., features).
        Returns:
          The convolved data.
        """
        dtype = jnp.promote_types(self.dtype, inputs.dtype)

        inputs = jnp.asarray(inputs, dtype)

        if isinstance(self.kernel_size, int):
            kernel_size = (self.kernel_size,)
        else:
            kernel_size = self.kernel_size

        is_single_input = False
        if inputs.ndim == len(kernel_size) + 1:
            is_single_input = True
            inputs = jnp.expand_dims(inputs, axis=0)

        strides = self.strides or (1,) * (inputs.ndim - 2)

        in_features = inputs.shape[-1]
        kernel_shape = kernel_size + (in_features, self.features)
        kernel = self.param("kernel", self.kernel_init, kernel_shape, self.dtype)
        kernel = jnp.asarray(kernel, dtype)

        y = lax.conv_transpose(
            inputs,
            kernel,
            strides,
            self.padding,
            rhs_dilation=self.kernel_dilation,
            precision=self.precision,
        )

        if is_single_input:
            y = jnp.squeeze(y, axis=0)
        if self.use_bias:
            bias = self.param("bias", self.bias_init, (self.features,), self.dtype)
            bias = jnp.asarray(bias, dtype)
            bias = jnp.asarray(bias, dtype)
            y = y + bias
        return y
