"""
agents_forum/reference_impl/toy_agent_client.py

Toy agent client for SimpleForumServer.

- Reads JSON lines from stdin (TaskAssignment messages).
- Solves a trivial "vector_task".
- Sends back TaskResult as JSON line to stdout.[web:1036][web:1040]

This is a minimal example for local experiments with the forum.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Dict, Optional, List

import numpy as np  # for simple vector operations [web:1034][web:1037]


def recv() -> Optional[Dict[str, Any]]:
    """Receive a JSON line from stdin."""
    line = sys.stdin.readline()
    if not line:
        return None
    line = line.strip()
    if not line:
        return None
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return None


def send(obj: Dict[str, Any]) -> None:
    """Send a JSON line to stdout."""
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def solve_vector_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Toy solver for task_type = 'vector_task'.

    Behavior:
    - read input vector from payload["vector"],
    - apply a simple transformation (e.g., scale towards ones),
    - compute a toy loss (distance to ones).[web:1034]
    """
    vec: List[float] = payload.get("vector", [])
    x = np.asarray(vec, dtype=float)
    target = np.ones_like(x)

    # Simple step towards target
    alpha = 0.5
    y = (1 - alpha) * x + alpha * target

    # Toy loss = mean squared error to target
    loss = float(np.mean((y - target) ** 2))

    output = {
        "vector": y.tolist(),
    }
    metrics = {
        "loss": loss,
        "accuracy": 1.0 - loss,  # nonsense metric, just for demo
        "foam_level": 0.0,       # this toy agent does not estimate foam
    }
    return {"output": output, "metrics": metrics}


def handle_task_assignment(msg: Dict[str, Any]) -> None:
    task = msg.get("task", {})
    task_id = task.get("task_id")
    task_type = task.get("task_type")
    payload = task.get("payload", {})

    if task_type == "vector_task":
        res = solve_vector_task(payload)
        result_msg = {
            "type": "TaskResult",
            "task_id": task_id,
            "state": "completed",
            "output": res["output"],
            "metrics": res["metrics"],
        }
        send(result_msg)
    else:
        failure_msg = {
            "type": "TaskFailure",
            "task_id": task_id,
            "state": "failed",
            "error_type": "unsupported_task_type",
            "error_message": f"Unsupported task_type: {task_type}",
        }
        send(failure_msg)


def main() -> None:
    """
    Main loop:

    - Wait for a single TaskAssignment from SimpleForumServer.
    - Handle it and exit.[web:1036][web:1040]
    """
    for incoming in iter(recv, None):
        msg_type = incoming.get("type")
        if msg_type == "TaskAssignment":
            handle_task_assignment(incoming)
            break
        else:
            # ignore other message types in this minimal client
            continue


if __name__ == "__main__":
    main()
