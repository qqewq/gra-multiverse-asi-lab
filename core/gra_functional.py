"""
core/gra_functional.py

Implementation of multilevel GRA Multiverse Meta-Reset:
- foam Phi^(l)
- level functionals J^(l)
- global functional J_multiverse

This is a toy / reference implementation for small, discrete state spaces.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Hashable, Iterable, Mapping, Tuple, Callable, Any, Optional
import numpy as np  # used as a generic linear space backend [web:970]


LevelIndex = int
MultiIndex = Tuple[Hashable, ...]  # generic multi-index a = (a0, a1, ..., ak)

# State vector for a subsystem; in full theory this lives in a Hilbert space.
StateVector = np.ndarray

# Projector: maps a state to its goal-aligned component (P_G |psi>).
Projector = Callable[[StateVector], StateVector]

# Local loss J_loc at level 0.
LocalLoss = Callable[[StateVector, Any], float]


@dataclass
class Subsystem:
    """
    Subsystem of the multiverse at some level l = dim(a).

    Attributes:
        index: multi-index a = (a0, ..., ak)
        level: l = dim(a)
        state: state vector Psi^(a)
        goal_data: arbitrary goal metadata G_l^(a), passed to projectors / losses
    """
    index: MultiIndex
    level: LevelIndex
    state: StateVector
    goal_data: Any = None


@dataclass
class Multiverse:
    """
    Discrete multiverse container.

    Attributes:
        subsystems: mapping from multi-index -> Subsystem
        parents: mapping child_index -> parent_index (for b ≺ a); optional.
    """
    subsystems: Dict[MultiIndex, Subsystem]
    parents: Dict[MultiIndex, MultiIndex]

    def by_level(self) -> Dict[LevelIndex, Dict[MultiIndex, Subsystem]]:
        levels: Dict[LevelIndex, Dict[MultiIndex, Subsystem]] = {}
        for a, sub in self.subsystems.items():
            levels.setdefault(sub.level, {})[a] = sub
        return levels


@dataclass
class GRAFunctional:
    """
    Container for GRA multiverse functionals.

    Attributes:
        projectors: mapping level -> projector P_{G_l}.
                    In more detailed setups this can be per-subsystem.
        local_loss: local loss J_loc for level 0.
        lambda0: base weight λ0 for level weights Λ_l = λ0 α^l.
        alpha: decay factor α in (0,1).
    """
    projectors: Mapping[LevelIndex, Projector]
    local_loss: LocalLoss
    lambda0: float = 1.0
    alpha: float = 0.5

    # --------- Foams Φ^(l) ---------

    def foam_level(
        self,
        subs_at_level: Mapping[MultiIndex, Subsystem],
        level: LevelIndex,
    ) -> float:
        """
        Compute foam Φ^(l)(Psi^(l), G_l) as a sum over pairs (a != b) of
        | <Psi^a | P_G_l | Psi^b> |^2.

        Assumes all states are np.ndarray with compatible shapes.[web:970]
        """
        projector = self.projectors[level]
        indices = list(subs_at_level.keys())
        n = len(indices)
        if n <= 1:
            return 0.0

        phi = 0.0
        # naive O(n^2) pairwise computation; fine for toy examples
        for i in range(n):
            a = indices[i]
            psi_a = subs_at_level[a].state
            for j in range(n):
                if i == j:
                    continue
                b = indices[j]
                psi_b = subs_at_level[b].state
                projected_b = projector(psi_b)
                inner = float(np.vdot(psi_a, projected_b))  # <a|P|b>
                phi += inner * inner.conjugate()
        return float(phi.real)

    # --------- Level functionals J^(l) ---------

    def level_functionals(
        self,
        multiverse: Multiverse,
        max_level: Optional[int] = None,
    ) -> Dict[MultiIndex, float]:
        """
        Compute J^(l)(Psi^(a)) for all subsystems via the recursive definition.

        Returns:
            mapping from subsystem index a -> J^(level(a))(Psi^(a)).
        """
        levels = multiverse.by_level()
        if not levels:
            return {}

        if max_level is None:
            max_level = max(levels.keys())

        J_values: Dict[MultiIndex, float] = {}

        # Level 0: purely local losses.
        if 0 in levels:
            for a, sub in levels[0].items():
                J_values[a] = float(self.local_loss(sub.state, sub.goal_data))

        # Higher levels: recursive accumulation + foam.
        for l in range(1, max_level + 1):
            if l not in levels:
                continue
            # Precompute foam for this level (one shared value used inside J^(l)).
            phi_l = self.foam_level(levels[l], level=l)
            for a, sub in levels[l].items():
                # Sum of J^(l-1) over children b ≺ a.
                children_sum = 0.0
                for b, parent in multiverse.parents.items():
                    if parent == a:
                        children_sum += J_values.get(b, 0.0)
                # For simplicity, use same foam value for all subsystems at level l.
                J_values[a] = children_sum + phi_l

        return J_values

    # --------- Global functional J_multiverse ---------

    def level_weight(self, level: LevelIndex) -> float:
        """Λ_l = λ0 α^l."""
        return self.lambda0 * (self.alpha ** level)

    def J_multiverse(
        self,
        multiverse: Multiverse,
        max_level: Optional[int] = None,
    ) -> float:
        """
        Compute J_multiverse(Psi) = sum_l Λ_l sum_{dim(a)=l} J^(l)(Psi^(a)).
        """
        levels = multiverse.by_level()
        if not levels:
            return 0.0
        if max_level is None:
            max_level = max(levels.keys())

        J_vals = self.level_functionals(multiverse, max_level=max_level)
        total = 0.0
        for l in range(0, max_level + 1):
            if l not in levels:
                continue
            w_l = self.level_weight(l)
            for a, sub in levels[l].items():
                total += w_l * J_vals.get(a, 0.0)
        return float(total)


# ---------- Minimal helpers / defaults ----------

def projector_identity(state: StateVector) -> StateVector:
    """
    Trivial projector P = I (no change).
    Useful as a default when no goal-structure is yet defined.[web:970]
    """
    return state


def local_loss_mse(state: StateVector, target: Optional[StateVector]) -> float:
    """
    Simple mean squared error local loss for level 0.
    If target is None, loss is taken as 0.0 (no supervision).[web:970]
    """
    if target is None:
        return 0.0
    state = np.asarray(state)
    target = np.asarray(target)
    return float(np.mean((state - target) ** 2))


def make_default_functional() -> GRAFunctional:
    """
    Create a default toy GRAFunctional with:
    - identity projector on all levels,
    - MSE as level-0 local loss,
    - λ0 = 1.0, α = 0.5.[web:970]
    """
    # For toy use we assume levels 0..2 exist; higher levels can reuse the same projector.
    projectors: Dict[LevelIndex, Projector] = {
        0: projector_identity,
        1: projector_identity,
        2: projector_identity,
    }
    return GRAFunctional(
        projectors=projectors,
        local_loss=local_loss_mse,
        lambda0=1.0,
        alpha=0.5,
    )
