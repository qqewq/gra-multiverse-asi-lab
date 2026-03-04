"""
01_minimal_multiverse_example.py

Простой пример использования core/:

- создаём маленький мультиверс из трёх подсистем на уровнях 0 и 1;
- задаём GRAFunctional с простыми проекторами;
- считаем J^(l) и J_multiverse.[file:850]
"""

from __future__ import annotations

from typing import Dict, Tuple, Any

import numpy as np

from core.gra_functional import (
    Multiverse,
    Subsystem,
    GRAFunctional,
    local_loss_mse,
)
from core.projectors import make_level_projectors_example


def main() -> None:
    # --- 1. Определяем подсистемы ---

    # Две подсистемы уровня 0
    psi_a0 = np.array([0.1, 0.2, 0.3, 0.4], dtype=float)
    psi_b0 = np.array([0.9, 0.8, 0.7, 0.6], dtype=float)

    sub_a0 = Subsystem(index=("a",), level=0, state=psi_a0, goal_data=None)
    sub_b0 = Subsystem(index=("b",), level=0, state=psi_b0, goal_data=None)

    # Одна подсистема уровня 1, которая «содержит» обе 0‑уровневые
    psi_c1 = np.array([0.5, 0.5, 0.5, 0.5], dtype=float)
    sub_c1 = Subsystem(index=("c", 1), level=1, state=psi_c1, goal_data=None)

    subsystems: Dict[Tuple[Any, ...], Subsystem] = {
        sub_a0.index: sub_a0,
        sub_b0.index: sub_b0,
        sub_c1.index: sub_c1,
    }

    # Иерархия: a ≺ c, b ≺ c
    parents: Dict[Tuple[Any, ...], Tuple[Any, ...]] = {
        sub_a0.index: sub_c1.index,
        sub_b0.index: sub_c1.index,
    }

    multiverse = Multiverse(subsystems=subsystems, parents=parents)

    # --- 2. Задаём GRAFunctional ---

    dim = psi_a0.size  # размерность векторов
    projectors = make_level_projectors_example(dim=dim)

    functional = GRAFunctional(
        projectors=projectors,
        local_loss=local_loss_mse,
        lambda0=1.0,
        alpha=0.5,
    )

    # --- 3. Считаем J^(l) и J_multiverse ---

    J_levels = functional.level_functionals(multiverse)
    J_total = functional.J_multiverse(multiverse)

    print("Level-wise J^(l)(Psi^(a)):")
    for idx, val in J_levels.items():
        print(f"  index={idx}, J={val:.6f}")

    print(f"\nGlobal J_multiverse = {J_total:.6f}")


if __name__ == "__main__":
    main()
