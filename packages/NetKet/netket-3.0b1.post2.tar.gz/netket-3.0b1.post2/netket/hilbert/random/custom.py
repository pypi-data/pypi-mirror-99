# Copyright 2021 The NetKet Authors - All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional, List

import jax
import numpy as np
from jax import numpy as jnp

# from numba import jit

from ..custom_hilbert import CustomHilbert

from .base import register_flip_state_impl, register_random_state_impl


def random_state_batch_spin_impl(hilb: CustomHilbert, key, batches, dtype):
    if not hilb.is_discrete or not hilb.is_finite or hilb._has_constraint:
        raise NotImplementedError()

    # Default version for discrete hilbert spaces without constraints.
    # More specialized initializations can be defined in the derived classes.

    σ = jax.random.choice(
        key,
        jnp.asarray(hilb.local_states, dtype=dtype),
        shape=(batches, hilb.size),
        replace=True,
    )
    return jnp.asarray(σ, dtype=dtype)


## flips
def flip_state_scalar_spin_impl(hilb: CustomHilbert, key, σ, indx):
    local_states = jnp.asarray(hilb.local_states)

    rs = jax.random.randint(key, shape=(), minval=0, maxval=len(hilb.local_states) - 1)

    new_val = local_states[rs + (local_states[rs] >= σ[indx])]
    return jax.ops.index_update(σ, indx, new_val), σ[indx]


def flip_state_batch_spin_impl(hilb: CustomHilbert, key, σ, indxs):
    n_batches = σ.shape[0]

    local_states = jnp.asarray(hilb.local_states)

    rs = jax.random.randint(
        key, shape=(n_batches,), minval=0, maxval=len(hilb.local_states) - 1
    )

    def scalar_update_fun(σ, indx, rs):
        new_val = local_states[rs + (local_states[rs] >= σ[indx])]
        return jax.ops.index_update(σ, indx, new_val), σ[indx]

    return jax.vmap(scalar_update_fun, in_axes=(0, 0, 0), out_axes=0)(σ, indxs, rs)


register_random_state_impl(CustomHilbert, batch=random_state_batch_spin_impl)
register_flip_state_impl(
    CustomHilbert, scalar=flip_state_scalar_spin_impl, batch=flip_state_batch_spin_impl
)
