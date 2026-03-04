"""
core/multiverse_optimizer.py

Toy optimizer / reset loop for the GRA Multiverse Meta-Reset functional.
This module provides:
- a simple finite-difference gradient approximation w.r.t. subsystem states,
- an iterative optimization loop that reduces J_multiverse.[web:986][web:987]

Intended for small, low-dimensional toy examples only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple, Callable, Optional, Any

import numpy as np  # used for finite-difference gradient and updates [web:986]

from .gra_functional import (
    Multiverse,
    Subsystem,
    GRAFunctional,
    StateVector,
)


Gradient = Dict[Tuple[Any, ...], StateVector]  # mapping index -> grad wrt state


def finite_difference_gradient(
    functional: GRAFunctional,
    multiverse: Multiverse,
    eps: float = 1e-4,
    max_level: Optional[int] = None,
) -> Gradient:
    """
    Approximate gradient of J_multiverse w.r.t. each subsystem's state
    using coordinate-wise finite differences.[web:992][web:995]

    WARNING: O(N * d) where N = number of subsystems, d = dim of state vector.
             Use only for tiny toy systems.
    """
    grad: Gradient = {}

    # Baseline value
    base_value = functional.J_multiverse(multiverse, max_level=max_level)

    for a, sub in multiverse.subsystems.items():
        psi = np.asarray(sub.state, dtype=float)
        d = psi.size
        g = np.zeros_like(psi, dtype=float)

        # Perturb each coordinate independently
        for i in range(d):
            # +eps
            psi_plus = psi.copy()
            psi_plus.flat[i] += eps
            multiverse.subsystems[a].state = psi_plus
            j_plus = functional.J_multiverse(multiverse, max_level=max_level)

            # -eps
            psi_minus = psi.copy()
            psi_minus.flat[i] -= eps
            multiverse.subsystems[a].state = psi_minus
            j_minus = functional.J_multiverse(multiverse, max_level=max_level)

            # central difference
            g.flat[i] = (j_plus - j_minus) / (2.0 * eps)

        # restore original state
        multiverse.subsystems[a].state = psi
        grad[a] = g

    return grad


@dataclass
class OptimizationConfig:
    """
    Configuration for the multiverse optimization loop.
    """
    learning_rate: float = 0.1
    max_iters: int = 100
    tol: float = 1e-6
    finite_diff_eps: float = 1e-4
    max_level: Optional[int] = None
    verbose: bool = False


def gradient_descent_step(
    functional: GRAFunctional,
    multiverse: Multiverse,
    config: OptimizationConfig,
) -> float:
    """
    Perform one gradient descent step on J_multiverse with respect to all
    subsystem states.[web:986][web:987]

    Returns:
        new_value: updated J_multiverse after the step.
    """
    grad = finite_difference_gradient(
        functional, multiverse, eps=config.finite_diff_eps, max_level=config.max_level
    )
    # Update all subsystem states simultaneously (in-place).
    for a, g in grad.items():
        sub = multiverse.subsystems[a]
        psi = np.asarray(sub.state, dtype=float)
        psi_new = psi - config.learning_rate * g
        multiverse.subsystems[a].state = psi_new
    return functional.J_multiverse(multiverse, max_level=config.max_level)


def optimize_multiverse(
    functional: GRAFunctional,
    multiverse: Multiverse,
    config: Optional[OptimizationConfig] = None,
) -> Dict[str, Any]:
    """
    Run an iterative optimization / reset loop on the multiverse state.

    Args:
        functional: GRAFunctional (defines Φ^(l), J^(l), J_multiverse).
        multiverse: Multiverse (contains subsystem states and hierarchy).
        config: optimization hyperparameters.

    Returns:
        dict with:
            - "history": list of J_multiverse values per iteration,
            - "iters": number of iterations performed,
            - "converged": bool flag.
    """
    if config is None:
        config = OptimizationConfig()

    history = []
    value = functional.J_multiverse(multiverse, max_level=config.max_level)
    history.append(value)

    for it in range(config.max_iters):
        new_value = gradient_descent_step(functional, multiverse, config)
        history.append(new_value)

        if config.verbose:
            print(f"[iter {it+1}] J = {new_value:.6f}")

        # Check convergence by absolute change
        if abs(new_value - value) < config.tol:
            return {
                "history": history,
                "iters": it + 1,
                "converged": True,
            }
        value = new_value

    return {
        "history": history,
        "iters": config.max_iters,
        "converged": False,
    }
