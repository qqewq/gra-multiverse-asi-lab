"""
asi_from_existing/toy_agent/model.py

Simple toy agent model used to demonstrate GRA-based self-improvement.

- State = small vector (parameters) + a couple of discrete "architecture flags".
- Forward = trivial linear transform.
- Train / update = basic gradient step on MSE loss.[web:1053][web:1054]

This is intentionally minimal and not meant for real tasks.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any, Tuple

import numpy as np  # basic numerical backend [web:1053][web:1060]


@dataclass
class ToyAgentConfig:
    """
    Configuration / "architecture flags" for the toy agent.
    """
    input_dim: int = 4
    hidden_dim: int = 4
    use_bias: bool = True
    nonlinearity: str = "tanh"  # or "relu" or "linear"


@dataclass
class ToyAgentState:
    """
    Continuous parameters of the toy agent.
    """
    W: np.ndarray  # shape (hidden_dim, input_dim)
    b: np.ndarray  # shape (hidden_dim,)


@dataclass
class ToyAgent:
    """
    Toy agent:

    - maintains parameters W, b and config;
    - can perform a "forward" pass on a vector;
    - can update its parameters via a simple gradient step.[web:1053][web:1054]
    """
    config: ToyAgentConfig
    state: ToyAgentState

    @staticmethod
    def init_random(config: ToyAgentConfig, scale: float = 0.1) -> "ToyAgent":
        rng = np.random.default_rng()
        W = rng.normal(0.0, scale, size=(config.hidden_dim, config.input_dim))
        b = rng.normal(0.0, scale, size=(config.hidden_dim,))
        return ToyAgent(
            config=config,
            state=ToyAgentState(W=W, b=b),
        )

    # ----- Forward -----

    def _apply_nonlinearity(self, x: np.ndarray) -> np.ndarray:
        if self.config.nonlinearity == "tanh":
            return np.tanh(x)
        elif self.config.nonlinearity == "relu":
            return np.maximum(x, 0.0)
        elif self.config.nonlinearity == "linear":
            return x
        else:
            # default to linear if unknown
            return x

    def forward(self, x: np.ndarray) -> np.ndarray:
        """
        Compute y = f_W(x) for a single input vector x of shape (input_dim,).[web:1054]
        """
        W = self.state.W
        b = self.state.b
        x = np.asarray(x, dtype=float)

        z = W @ x  # (hidden_dim,)
        if self.config.use_bias:
            z = z + b
        y = self._apply_nonlinearity(z)
        return y

    # ----- Loss and gradient -----

    def loss_mse(self, x: np.ndarray, target: np.ndarray) -> float:
        """
        Mean squared error between forward(x) and target.[web:1053]
        """
        y = self.forward(x)
        target = np.asarray(target, dtype=float)
        return float(np.mean((y - target) ** 2))

    def grad_step_mse(
        self,
        x: np.ndarray,
        target: np.ndarray,
        lr: float = 0.1,
    ) -> float:
        """
        Perform one gradient descent step on MSE loss
        with respect to W, b (backprop implemented manually).[web:1053][web:1059]

        Returns:
            loss_before_step
        """
        x = np.asarray(x, dtype=float)
        target = np.asarray(target, dtype=float)

        # Forward
        W = self.state.W
        b = self.state.b

        z = W @ x
        if self.config.use_bias:
            z = z + b

        if self.config.nonlinearity == "tanh":
            y = np.tanh(z)
            dy_dz = 1.0 - y**2
        elif self.config.nonlinearity == "relu":
            y = np.maximum(z, 0.0)
            dy_dz = (z > 0.0).astype(float)
        else:  # linear
            y = z
            dy_dz = np.ones_like(z)

        loss = float(np.mean((y - target) ** 2))

        # dL/dy = 2 (y - target) / N
        N = y.size
        dL_dy = 2.0 * (y - target) / N

        # dL/dz = dL/dy * dy/dz (elementwise)
        dL_dz = dL_dy * dy_dz  # shape (hidden_dim,)

        # Gradients
        dL_dW = np.outer(dL_dz, x)  # (hidden_dim, input_dim)
        dL_db = dL_dz               # (hidden_dim,)

        # Update
        self.state.W = W - lr * dL_dW
        if self.config.use_bias:
            self.state.b = b - lr * dL_db

        return loss

    # ----- Introspection helpers (for GRA wrappers) -----

    def get_vector_state(self) -> np.ndarray:
        """
        Flatten W and b into a single vector for use as Psi^(a). [web:1053]
        """
        W_flat = self.state.W.flatten()
        b_flat = self.state.b.flatten()
        return np.concatenate([W_flat, b_flat], axis=0)

    def set_vector_state(self, vec: np.ndarray) -> None:
        """
        Set W and b from a flattened vector.[web:1054]
        """
        vec = np.asarray(vec, dtype=float)
        d_W = self.config.hidden_dim * self.config.input_dim
        W_flat = vec[:d_W]
        b_flat = vec[d_W:d_W + self.config.hidden_dim]

        self.state.W = W_flat.reshape(self.config.hidden_dim, self.config.input_dim)
        self.state.b = b_flat
