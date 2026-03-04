"""
core/projectors.py

Example projectors P_{G_l} for different toy tasks / goals.

These are simple numerical projectors implemented with NumPy, intended
to be plugged into GRAFunctional from gra_functional.py.[web:976]
"""

from __future__ import annotations

from typing import Optional, Dict, Callable, Any
import numpy as np  # numerical backend for vector projections [web:976]

StateVector = np.ndarray

# A projector maps a state vector to its goal-aligned component.
Projector = Callable[[StateVector], StateVector]


# ---------- Basic helpers ----------

def _safe_norm(x: StateVector, eps: float = 1e-12) -> float:
    """Compute Euclidean norm with epsilon floor to avoid division by zero.[web:981]"""
    return float(np.linalg.norm(x) + eps)


# ---------- Simple projectors ----------

def projector_identity(state: StateVector) -> StateVector:
    """
    Trivial projector P = I (no change).

    Use this when no goal-structure is available yet, or as a baseline.[web:976]
    """
    return state


def projector_to_target_direction(target: StateVector) -> Projector:
    """
    Build a projector that projects any state onto the (normalized) direction
    of a given target vector.

    Mathematically:
        P |psi> = ( <t_hat | psi> ) |t_hat>,
    where t_hat is target / ||target||.[web:976][web:980]
    """
    target = np.asarray(target, dtype=float)
    norm = _safe_norm(target)
    t_hat = target / norm

    def projector(state: StateVector) -> StateVector:
        psi = np.asarray(state, dtype=float)
        coeff = float(np.vdot(t_hat, psi))  # <t_hat | psi>
        return coeff * t_hat

    return projector


def projector_to_affine_subspace(
    basis: StateVector,
    offset: StateVector,
) -> Projector:
    """
    Projector onto a 1D affine subspace offset + span{basis}.

    P(state) = offset + proj_basis(state - offset),
    where proj_basis is orthogonal projection onto basis.[web:976][web:977]
    """
    basis = np.asarray(basis, dtype=float)
    offset = np.asarray(offset, dtype=float)
    norm_sq = float(np.dot(basis, basis)) + 1e-12

    def projector(state: StateVector) -> StateVector:
        psi = np.asarray(state, dtype=float)
        delta = psi - offset
        coeff = float(np.dot(delta, basis)) / norm_sq
        return offset + coeff * basis

    return projector


def projector_to_boolean_hypercube() -> Projector:
    """
    Projector that snaps each component to {0,1} via threshold 0.5.

    Interprets the goal as being on a discrete hypercube.[web:980]
    """
    def projector(state: StateVector) -> StateVector:
        psi = np.asarray(state, dtype=float)
        return (psi >= 0.5).astype(float)

    return projector


# ---------- Higher-level goal projectors ----------

def make_level_projectors_example(
    dim: int,
    targets_level0: Optional[Dict[int, StateVector]] = None,
) -> Dict[int, Projector]:
    """
    Example constructor for projectors P_{G_l} across levels.

    Args:
        dim: base dimension of state vectors at level 0.
        targets_level0: optional mapping idx -> target vector for level-0 goals.

    Returns:
        dict: level -> projector
            - level 0: projector towards specific target directions (if given),
              or identity otherwise;
            - level 1: projector to mean direction (consensus) across subsystems;
            - level 2: identity (placeholder).[web:976][web:980]
    """
    # Level 0: if targets are provided, we project onto each target direction.
    # For GRAFunctional we usually provide a single projector per level, so here
    # we just use identity as a default. Targets can be handled in local_loss.

    def projector_level0(state: StateVector) -> StateVector:
        return state  # keep level-0 projector simple here

    # Level 1: consensus projector — project onto the all-ones direction
    # (interpreted as "agreement" across coordinates).
    ones = np.ones(dim, dtype=float)
    projector_level1 = projector_to_target_direction(ones)

    # Level 2: identity as placeholder.
    projector_level2 = projector_identity

    return {
        0: projector_level0,
        1: projector_level1,
        2: projector_level2,
    }
