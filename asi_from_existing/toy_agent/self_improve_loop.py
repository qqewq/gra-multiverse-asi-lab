"""
asi_from_existing/toy_agent/self_improve_loop.py

Toy self-improvement loop for the ToyAgent using the GRA wrapper.

This script demonstrates a minimal RSI-style cycle:
- evaluate J_multiverse,
- propose simple modifications,
- accept those that reduce J_multiverse.[file:850][web:963][web:1069]

This is a sandboxed, non-dangerous example (tiny state, no external effects).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Dict, Any

import numpy as np  # RNG and small math [web:1077]

from .model import ToyAgent, ToyAgentConfig
from .gra_wrapper import (
    AgentMultiverseBinding,
    build_binding,
    sync_agent_to_multiverse,
    sync_multiverse_to_agent,
    compute_J,
    random_perturbation,
)


@dataclass
class Modification:
    """
    Simple representation of a candidate self-modification.
    """
    name: str
    apply: Callable[[AgentMultiverseBinding], None]


def make_modifications(binding: AgentMultiverseBinding) -> List[Modification]:
    """
    Construct a small set of candidate modifications for the toy agent.

    Types (all considered "safe" in this toy setup):
    - small random perturbation of parameters;
    - change nonlinearity (tanh <-> relu);
    - toggle bias term.[web:1079][web:1076]
    """

    def mod_noise(b: AgentMultiverseBinding) -> None:
        random_perturbation(b, scale=0.01)

    def mod_nonlinearity_toggle(b: AgentMultiverseBinding) -> None:
        agent = b.agent
        if agent.config.nonlinearity == "tanh":
            agent.config.nonlinearity = "relu"
        elif agent.config.nonlinearity == "relu":
            agent.config.nonlinearity = "tanh"
        # re-sync to multiverse after config change
        sync_agent_to_multiverse(b)

    def mod_toggle_bias(b: AgentMultiverseBinding) -> None:
        agent = b.agent
        agent.config.use_bias = not agent.config.use_bias
        sync_agent_to_multiverse(b)

    return [
        Modification(name="noise_params", apply=mod_noise),
        Modification(name="toggle_nonlinearity", apply=mod_nonlinearity_toggle),
        Modification(name="toggle_bias", apply=mod_toggle_bias),
    ]


@dataclass
class SelfImproveConfig:
    max_iters: int = 20
    candidates_per_iter: int = 3
    verbose: bool = True


def self_improve_loop(
    binding: AgentMultiverseBinding,
    config: SelfImproveConfig,
) -> Dict[str, Any]:
    """
    Run a toy self-improvement loop:

    For each iteration:
    - sync agent -> multiverse,
    - evaluate J,
    - sample candidate modifications,
    - evaluate their effect on J,
    - keep the best (lowest J) modification if it improves J,
    - update agent from multiverse.[web:1069][web:1075]
    """
    history = []
    rng = np.random.default_rng()

    # Initial J
    sync_agent_to_multiverse(binding)
    J_current = compute_J(binding)
    history.append(J_current)

    if config.verbose:
        print(f"[iter 0] J = {J_current:.6f}")

    for it in range(1, config.max_iters + 1):
        mods = make_modifications(binding)
        # sample subset of candidates
        chosen_indices = rng.choice(len(mods), size=config.candidates_per_iter, replace=False)
        best_delta = 0.0
        best_J = J_current
        best_mod_name = None
        best_state_snapshot = None

        # snapshot current multiverse state
        base_state = binding.multiverse.subsystems[binding.index_param].state.copy()

        for idx in chosen_indices:
            mod = mods[idx]

            # reset to baseline before each trial
            binding.multiverse.subsystems[binding.index_param].state = base_state.copy()
            sync_multiverse_to_agent(binding)

            # apply modification
            mod.apply(binding)

            # evaluate new J
            sync_agent_to_multiverse(binding)
            J_new = compute_J(binding)
            delta = J_new - J_current

            if config.verbose:
                print(f"  trial mod={mod.name}, J_new={J_new:.6f}, ΔJ={delta:+.6f}")

            if J_new < best_J:
                best_J = J_new
                best_delta = delta
                best_mod_name = mod.name
                best_state_snapshot = binding.multiverse.subsystems[binding.index_param].state.copy()

        # Decide whether to accept the best modification
        if best_mod_name is not None and best_delta < 0.0:
            # apply best snapshot
            binding.multiverse.subsystems[binding.index_param].state = best_state_snapshot
            sync_multiverse_to_agent(binding)
            J_current = best_J
            if config.verbose:
                print(f"[iter {it}] accepted mod={best_mod_name}, J={J_current:.6f}")
        else:
            if config.verbose:
                print(f"[iter {it}] no improving modification found, stopping.")
            break

        history.append(J_current)

    return {
        "history": history,
        "final_J": J_current,
        "iters": len(history) - 1,
    }


def main() -> None:
    config_agent = ToyAgentConfig(input_dim=4, hidden_dim=4, use_bias=True, nonlinearity="tanh")
    agent = ToyAgent.init_random(config_agent, scale=0.1)
    binding = build_binding(agent, lambda0=1.0, alpha=0.5)

    cfg = SelfImproveConfig(max_iters=10, candidates_per_iter=3, verbose=True)
    result = self_improve_loop(binding, cfg)

    print("Self-improvement result:", result)


if __name__ == "__main__":
    main()
