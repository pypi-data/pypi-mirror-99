# Copyright 2021 The NetKet Authors - All rights reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Optional, Callable

import jax
from jax import numpy as jnp
from jax.experimental import loops

from flax import struct

from netket.hilbert import AbstractHilbert

from .base import Sampler, SamplerState

PyTree = Any
PRNGKey = jnp.ndarray


@struct.dataclass
class MetropolisRule:
    """
    Base class for Transition rules of Metropolis, such as Local, Exchange, Hamiltonian
    and several others.
    """

    def init_state(
        rule,
        sampler: Sampler,
        machine: Callable,
        params: PyTree,
        key: PRNGKey,
    ) -> Optional[Any]:
        """
        Initialises the optional internal state of the Metropolis Sampler Transition
        Rule.

        The provided key is unique and does not need to be splitted.
        It should return an immutable datastructure.

        Arguments:
            sampler: The Metropolis sampler
            machine: The forward evaluation function of the model, accepting PyTrees of parameters and inputs.
            params: The dict of variables needed to evaluate the model.
            key: A Jax PRNGKey rng state.

        Returns:
            An Optional State.
        """
        return None

    def reset(
        rule,
        sampler: Sampler,
        machine: Callable,
        params: PyTree,
        sampler_state: SamplerState,
    ) -> Optional[Any]:
        """
        Resets the internal state of the Metropolis Sampler Transition Rule.

        Arguments:
            sampler: The Metropolis sampler
            machine: The forward evaluation function of the model, accepting PyTrees of parameters and inputs.
            params: The dict of variables needed to evaluate the model.
            sampler_state: The current state of the sampler. Should not modify it.

        Returns:
            An Optional State. Must return the same type of `sampler_state.rule_state`.
        """
        return sampler_state.rule_state

    def transition(
        rule,
        sampler: Sampler,
        machine: Callable,
        parameters: PyTree,
        state: SamplerState,
        key: PRNGKey,
        σ: jnp.ndarray,
    ) -> jnp.ndarray:

        raise NotImplementedError("error")

    def random_state(
        rule,
        sampler: Sampler,
        machine: Callable,
        parameters: PyTree,
        state: SamplerState,
        key: PRNGKey,
    ):
        """
        Generates a random state compatible with this rule.

        By default this calls :func:`netket.hilbert.random.random_state`.

        Arguments:
            sampler: the sampler
            machine: the function to evaluate the model
            parameters: the parameters of the model
            state: the current sampler state
            key: the PRNGKey to use to generate the random state
        """
        return sampler.hilbert.random_state(
            key, size=sampler.n_batches, dtype=sampler.dtype
        )


@struct.dataclass
class MetropolisSamplerState(SamplerState):
    """
    State for a metropolis sampler.
    Contains the current configuration, the rng state and the (optional)
    state of the transition rule.
    """

    σ: jnp.ndarray
    """Current batch of configurations in the markov chain."""
    rng: jnp.ndarray
    """State of the random number generator (key, in jax terms)."""
    rule_state: Optional[Any]
    """Optional state of a transition rule."""
    n_samples: int = 0
    """Number of moves performed along the chains since the last reset."""
    n_accepted: int = 0
    """Number of accepted transitions along the chains since the last reset."""

    def __repr__(self):
        if self.n_samples > 0:
            acceptance_rate = self.n_accepted / self.n_samples * 100
            acc_string = "# accepted = {}/{} ({}%), ".format(
                self.n_accepted, self.n_samples, acceptance_rate
            )
        else:
            acc_string = ""

        text = "MetropolisSamplerState(" + acc_string + "rng state={})".format(self.rng)
        return text


@struct.dataclass
class MetropolisSampler(Sampler):
    """
    Metropolis-Hastings sampler for an Hilbert space according to a specific transition rule.

    The transition rule is used to generate a proposed state :math:`s^\prime`, starting from the
    current state :math:`s`. The move is accepted with probability

    .. math::

        A(s \\rightarrow s^\\prime) = \\mathrm{min} \\left( 1,\\frac{P(s^\\prime)}{P(s)} F(e^{L(s,s^\\prime)}) \\right) ,

    where the probability being sampled from is :math:`P(s)=|M(s)|^p. Here ::math::`M(s)` is a
    user-provided function (the machine), :math:`p` is also user-provided with default value :math:`p=2`,
    and :math:`L(s,s^\prime)` is a suitable correcting factor computed by the transition kernel.

    The dtype of the sampled states can be chosen.
    """

    rule: MetropolisRule = None
    """The metropolis transition rule."""
    n_sweeps: int = struct.field(pytree_node=False, default=0)
    """Number of sweeps for each step along the chain. Defaults to number of sites in hilbert space."""
    reset_chain: bool = False
    """If True resets the chain state when reset is called (every new sampling)."""

    def __init__(
        self,
        hilbert: AbstractHilbert,
        rule: MetropolisRule,
        *,
        n_sweeps: Optional[int] = None,
        reset_chain: bool = False,
        **kwargs,
    ):
        """
        Constructs a Metropolis Sampler.

        Args:
            hilbert: The hilbert space to sample
            rule: A `MetropolisRule` to generate random transitions from a given state as
                    well as uniform random states.
            n_sweeps: The number of exchanges that compose a single sweep.
                    If None, sweep_size is equal to the number of degrees of freedom being sampled
                    (the size of the input vector s to the machine).
            reset_chain: If False the state configuration is not resetted when reset() is called.
            n_chains: The number of Markov Chain to be run in parallel on a single process.
            n_chains: The number of batches of the states to sample (default = 8)
            machine_pow: The power to which the machine should be exponentiated to generate the pdf (default = 2).
            dtype: The dtype of the statees sampled (default = np.float32).
        """
        if n_sweeps is None:
            n_sweeps = hilbert.size

        object.__setattr__(self, "rule", rule)
        object.__setattr__(self, "n_sweeps", n_sweeps)
        object.__setattr__(self, "reset_chain", reset_chain)

        super().__init__(hilbert, **kwargs)

    def __post_init__(self):
        super().__post_init__()
        # Validate the inputs
        if not isinstance(self.rule, MetropolisRule):
            raise TypeError("rule must be a MetropolisRule.")

        #  Default value of n_sweeps
        if self.n_sweeps == 0:
            object.__setattr__(self, "n_sweeps", self.hilbert.size)

    def _init_state(sampler, machine, params, key):
        key_state, key_rule = jax.random.split(key, 2)
        rule_state = sampler.rule.init_state(sampler, machine, params, key_rule)
        σ = jnp.zeros((sampler.n_chains, sampler.hilbert.size), dtype=sampler.dtype)

        state = MetropolisSamplerState(
            σ=σ, rng=key_state, rule_state=rule_state, n_samples=0, n_accepted=0
        )

        # If we don't reset the chain at every sampling iteration, then reset it
        # now.
        if not sampler.reset_chain:
            key_state, rng = jax.random.split(key_state)
            σ = sampler.rule.random_state(sampler, machine, params, state, rng)
            state = state.replace(σ=σ, rng=key_state)

        return state

    def _reset(sampler, machine, parameters, state):
        new_rng, rng = jax.random.split(state.rng)

        if sampler.reset_chain:
            σ = sampler.rule.random_state(sampler, machine, parameters, state, rng)
        else:
            σ = state.σ

        rule_state = sampler.rule.reset(sampler, machine, parameters, state)

        return state.replace(
            σ=σ, rng=new_rng, rule_state=rule_state, n_samples=0, n_accepted=0
        )

    def _sample_next(sampler, machine, parameters, state):
        new_rng, rng = jax.random.split(state.rng)

        with loops.Scope() as s:
            s.key = rng
            s.σ = state.σ
            s.log_prob = sampler.machine_pow * machine(parameters, state.σ).real

            # for logging
            s.accepted = state.n_accepted

            for i in s.range(sampler.n_sweeps):
                # 1 to propagate for next iteration, 1 for uniform rng and n_chains for transition kernel
                s.key, key1, key2 = jax.random.split(s.key, 3)

                σp, log_prob_correction = sampler.rule.transition(
                    sampler, machine, parameters, state, key1, s.σ
                )
                proposal_log_prob = sampler.machine_pow * machine(parameters, σp).real

                uniform = jax.random.uniform(key2, shape=(sampler.n_chains,))
                if log_prob_correction is not None:
                    do_accept = uniform < jnp.exp(
                        proposal_log_prob - s.log_prob + log_prob_correction
                    )
                else:
                    do_accept = uniform < jnp.exp(proposal_log_prob - s.log_prob)

                # do_accept must match ndim of proposal and state (which is 2)
                s.σ = jnp.where(do_accept.reshape(-1, 1), σp, s.σ)
                s.accepted += do_accept.sum()

                s.log_prob = jax.numpy.where(
                    do_accept.reshape(-1), proposal_log_prob, s.log_prob
                )

            new_state = state.replace(
                rng=new_rng,
                σ=s.σ,
                n_accepted=s.accepted,
                n_samples=state.n_samples + sampler.n_sweeps * sampler.n_chains,
            )

        return new_state, new_state.σ

    def __repr__(sampler):
        return (
            "MetropolisSampler("
            + "\n  hilbert = {},".format(sampler.hilbert)
            + "\n  rule = {},".format(sampler.rule)
            + "\n  n_chains = {},".format(sampler.n_chains)
            + "\n  machine_power = {},".format(sampler.machine_pow)
            + "\n  reset_chain = {},".format(sampler.reset_chain)
            + "\n  n_sweeps = {},".format(sampler.n_sweeps)
            + "\n  dtype = {}".format(sampler.dtype)
            + ")"
        )

    def __str__(sampler):
        return (
            "MetropolisSampler("
            + "rule = {}, ".format(sampler.rule)
            + "n_chains = {}, ".format(sampler.n_chains)
            + "machine_power = {}, ".format(sampler.machine_pow)
            + "n_sweeps = {}, ".format(sampler.n_sweeps)
            + "dtype = {})".format(sampler.dtype)
        )


from netket.utils import wraps_legacy
from netket.legacy.machine import AbstractMachine

from .rules import LocalRule
from netket.legacy.sampler import MetropolisLocal as LegacyMetropolisLocal


@wraps_legacy(LegacyMetropolisLocal, "machine", AbstractMachine)
def MetropolisLocal(hilbert, *args, **kwargs) -> MetropolisSampler:
    """
    Sampler acting on one local degree of freedom.

    This sampler acts locally only on one local degree of freedom :math:`s_i`,
    and proposes a new state: :math:`s_1 \dots s^\prime_i \dots s_N`,
    where :math:`s^\prime_i \\neq s_i`.

    The transition probability associated to this
    sampler can be decomposed into two steps:

    1. One of the site indices :math:`i = 1\dots N` is chosen with uniform probability.

    2. Among all the possible (:math:`m`) values that :math:`s_i` can take,
    one of them is chosen with uniform probability.

    For example, in the case of spin :math:`1/2` particles, :math:`m=2`
    and the possible local values are :math:`s_i = -1,+1`.
    In this case then :class:`MetropolisLocal` is equivalent to flipping a random spin.

    In the case of bosons, with occupation numbers
    :math:`s_i = 0, 1, \dots n_{\mathrm{max}}`, :class:`MetropolisLocal`
    would pick a random local occupation number uniformly between :math:`0`
    and :math:`n_{\mathrm{max}}`.

    Args:
        hilbert: The hilbert space to sample
        n_chains: The number of Markov Chain to be run in parallel on a single process.
        n_sweeps: The number of exchanges that compose a single sweep.
                If None, sweep_size is equal to the number of degrees of freedom being sampled
                (the size of the input vector s to the machine).
        n_chains: The number of batches of the states to sample (default = 8)
        machine_pow: The power to which the machine should be exponentiated to generate the pdf (default = 2).
        dtype: The dtype of the statees sampled (default = np.float32).
    """
    return MetropolisSampler(hilbert, LocalRule(), *args, **kwargs)


from .rules import ExchangeRule
from netket.legacy.sampler import MetropolisExchange as LegacyMetropolisExchange


@wraps_legacy(LegacyMetropolisExchange, "machine", AbstractMachine)
def MetropolisExchange(
    hilbert, *args, clusters=None, graph=None, d_max=1, **kwargs
) -> MetropolisSampler:
    r"""
    This sampler acts locally only on two local degree of freedom :math:`s_i` and :math:`s_j`,
    and proposes a new state: :math:`s_1 \dots s^\prime_i \dots s^\prime_j \dots s_N`,
    where in general :math:`s^\prime_i \neq s_i` and :math:`s^\prime_j \neq s_j`.
    The sites :math:`i` and :math:`j` are also chosen to be within a maximum graph
    distance of :math:`d_{\mathrm{max}}`.

    The transition probability associated to this sampler can
    be decomposed into two steps:

    1. A pair of indices :math:`i,j = 1\dots N`, and such that
       :math:`\mathrm{dist}(i,j) \leq d_{\mathrm{max}}`,
       is chosen with uniform probability.

    2. The sites are exchanged, i.e. :math:`s^\prime_i = s_j` and :math:`s^\prime_j = s_i`.


    Notice that this sampling method generates random permutations of the quantum
    numbers, thus global quantities such as the sum of the local quantum numbers
    are conserved during the sampling.
    This scheme should be used then only when sampling in a
    region where :math:`\sum_i s_i = \mathrm{constant} ` is needed,
    otherwise the sampling would be strongly not ergodic.

    Args:
        hilbert: The hilbert space to sample
        d_max: The maximum graph distance allowed for exchanges.
        n_chains: The number of Markov Chain to be run in parallel on a single process.
        n_sweeps: The number of exchanges that compose a single sweep.
                If None, sweep_size is equal to the number of degrees of freedom being sampled
                (the size of the input vector s to the machine).
        n_batches: The number of batches of the states to sample (default = 8)
        machine_pow: The power to which the machine should be exponentiated to generate the pdf (default = 2).
        dtype: The dtype of the statees sampled (default = np.float32).


    Examples:
          Sampling from a RBM machine in a 1D lattice of spin 1/2, using
          nearest-neighbours exchanges.

          >>> import netket as nk
          >>>
          >>> g=nk.graph.Hypercube(length=10,n_dim=2,pbc=True)
          >>> hi=nk.hilbert.Spin(s=0.5,graph=g)
          >>>
          >>> # RBM Spin Machine
          >>> ma = nk.machine.RbmSpin(alpha=1, hilbert=hi)
          >>>
          >>> # Construct a MetropolisExchange Sampler
          >>> sa = nk.sampler.MetropolisExchange(machine=ma)
          >>> print(sa.machine.hilbert.size)
          100
    """
    rule = ExchangeRule(clusters=clusters, graph=graph, d_max=d_max)
    return MetropolisSampler(hilbert, rule, *args, **kwargs)


from .rules import HamiltonianRule
from netket.legacy.sampler import MetropolisHamiltonian as LegacyMetropolisHamiltonian


@wraps_legacy(LegacyMetropolisHamiltonian, "machine", AbstractMachine)
def MetropolisHamiltonian(hilbert, hamiltonian, *args, **kwargs) -> MetropolisSampler:
    r"""
    Sampling based on the off-diagonal elements of a Hamiltonian (or a generic Operator).
    In this case, the transition matrix is taken to be:

    .. math::
       T( \mathbf{s} \rightarrow \mathbf{s}^\prime) = \frac{1}{\mathcal{N}(\mathbf{s})}\theta(|H_{\mathbf{s},\mathbf{s}^\prime}|),

    where :math:`\theta(x)` is the Heaviside step function, and :math:`\mathcal{N}(\mathbf{s})`
    is a state-dependent normalization.
    The effect of this transition probability is then to connect (with uniform probability)
    a given state :math:`\mathbf{s}` to all those states :math:`\mathbf{s}^\prime` for which the Hamiltonian has
    finite matrix elements.
    Notice that this sampler preserves by construction all the symmetries
    of the Hamiltonian. This is in generally not true for the local samplers instead.

    This sampler only works on the CPU. To use the Hamiltonian smapler with GPUs,
    you should use :class:`netket.sampler.MetropolisHamiltonianNumpy`

    Args:
       machine: A machine :math:`\Psi(s)` used for the sampling.
                The probability distribution being sampled
                from is :math:`F(\Psi(s))`, where the function
                :math:`F(X)`, is arbitrary, by default :math:`F(X)=|X|^2`.
       hamiltonian: The operator used to perform off-diagonal transition.
       n_chains: The number of Markov Chain to be run in parallel on a single process.
       sweep_size: The number of exchanges that compose a single sweep.
                   If None, sweep_size is equal to the number of degrees of freedom (n_visible).


    Examples:
       Sampling from a RBM machine in a 1D lattice of spin 1/2

       >>> import netket as nk
       >>>
       >>> g=nk.graph.Hypercube(length=10,n_dim=2,pbc=True)
       >>> hi=nk.hilbert.Spin(s=0.5,graph=g)
       >>>
       >>> # RBM Spin Machine
       >>> ma = nk.machine.RbmSpin(alpha=1, hilbert=hi)
       >>>
       >>> # Transverse-field Ising Hamiltonian
       >>> ha = nk.operator.Ising(hilbert=hi, h=1.0)
       >>>
       >>> # Construct a MetropolisHamiltonian Sampler
       >>> sa = nk.sampler.MetropolisHamiltonian(machine=ma,hamiltonian=ha)
    """
    rule = HamiltonianRule(hamiltonian)
    return MetropolisSampler(hilbert, rule, *args, **kwargs)
