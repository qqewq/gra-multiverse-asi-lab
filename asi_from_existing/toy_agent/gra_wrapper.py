"""
asi_from_existing/toy_agent/gra_wrapper.py

Wrapper that maps a ToyAgent into the GRA multiverse structures:

- builds a Multiverse with one or more subsystems from agent state;
- connects it to a GRAFunctional instance;
- provides helpers to compute J_multiverse and its toy gradients.[file:850][web:963]
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple, Any, Optional

import numpy as np  # flatten / reshape, basic linear algebra [web:1068][web:1071]

from core.gra_functional import (
    Multiverse,
    Subsystem,
    GRAFunctional,
    StateVector,
)
from core.projectors import make_level_projectors_example
from core.gra_functional import local_loss_mse

from .model import ToyAgent, ToyAgentConfig


@dataclass
class AgentMultiverseBinding:
    """
    Binding between a ToyAgent and its representation in the multiverse.

    For the toy case we use:
    - one level-0 subsystem representing the flattened parameters;
    - optional higher-level subsystems could be added later.
    """
    agent: ToyAgent
    multiverse: Multiverse
    functional: GRAFunctional
    index_param: Tuple[str, ...] = ("agent_params",)


def build_binding(
    agent: ToyAgent,
    lambda0: float = 1.0,
    alpha: float = 0.5,
) -> AgentMultiverseBinding:
    """
    Construct a minimal binding:

    - create a single subsystem at level 0 with index ("agent_params",);
    - state = flattened agent parameters (W, b);
    - GRAFunctional with simple projectors and MSE local loss.[file:850][web:963]
    """
    vec_state = agent.get_vector_state()
    dim = vec_state.size

    sub = Subsystem(
        index=("agent_params",),
        level=0,
        state=vec_state,
        goal_data=None,  # can be used later (e.g., target vectors)
    )

    multiverse = Multiverse(
        subsystems={sub.index: sub},
        parents={},
    )

    projectors = make_level_projectors_example(dim=dim)
    functional = GRAFunctional(
        projectors=projectors,
        local_loss=local_loss_mse,
        lambda0=lambda0,
        alpha=alpha,
    )

    return AgentMultiverseBinding(
        agent=agent,
        multiverse=multiverse,
        functional=functional,
        index_param=sub.index,
    )


def sync_agent_to_multiverse(binding: AgentMultiverseBinding) -> None:
    """
    Copy agent parameters into multiverse state.[web:1068]
    """
    vec = binding.agent.get_vector_state()
    sub = binding.multiverse.subsystems[binding.index_param]
    sub.state = np.asarray(vec, dtype=float)


def sync_multiverse_to_agent(binding: AgentMultiverseBinding) -> None:
    """
    Copy multiverse state back into agent parameters.[web:1068]
    """
    sub = binding.multiverse.subsystems[binding.index_param]
    vec = np.asarray(sub.state, dtype=float)
    binding.agent.set_vector_state(vec)


def compute_J(binding: AgentMultiverseBinding) -> float:
    """
    Compute J_multiverse for the current agent+multiverse state.[file:850][web:963]
    """
    sync_agent_to_multiverse(binding)
    return binding.functional.J_multiverse(binding.multiverse)


def random_perturbation(binding: AgentMultiverseBinding, scale: float = 0.01) -> None:
    """
    Apply a small random perturbation to the multiverse representation
    of the agent (toy modification).[web:1044]
    """
    sub = binding.multiverse.subsystems[binding.index_param]
    psi = np.asarray(sub.state, dtype=float)
    rng = np.random.default_rng()
    sub.state = psi + rng.normal(0.0, scale, size=psi.shape)


def print_binding_summary(binding: AgentMultiverseBinding) -> None:
    """
    Utility: print a short summary of the binding and current J value.
    """
    J_val = compute_J(binding)
    vec = binding.multiverse.subsystems[binding.index_param].state
    print(f"ToyAgent params dim = {vec.size}, J_multiverse = {J_val:.6f}")
