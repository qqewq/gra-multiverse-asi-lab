"""
agents_forum/reference_impl/simple_forum_server.py

Minimal toy "forum" server.

- Keeps tasks in memory.
- Communicates with agents via stdin/stdout JSON lines (for simplicity).
- Demonstrates how to route tasks and aggregate results in terms of GRA.[web:1024][web:1031]

This is NOT production code; it is only a reference skeleton for experiments.
"""

from __future__ import annotations

import json
import sys
import uuid
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional

from core.gra_functional import GRAFunctional, Multiverse, Subsystem
from core.projectors import make_level_projectors_example
from core.gra_functional import local_loss_mse


# ---------- Data models ----------

@dataclass
class Task:
    task_id: str
    session_id: str
    task_type: str
    goal_level: int
    payload: Dict[str, Any]
    constraints: Dict[str, Any]


@dataclass
class TaskState:
    task_id: str
    state: str  # created | running | completed | failed | cancelled
    output: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# ---------- Forum server core ----------

class SimpleForumServer:
    """
    Minimal in-process forum server using stdin/stdout JSON lines as the transport.

    Protocol (very simplified):

    - Input from agent: JSON objects with field "type":
        - "TaskResult"
        - "TaskFailure"
    - Output to agent: JSON objects with field "type":
        - "TaskAssignment"

    This allows to plug a toy_agent_client.py that reads/writes JSON lines.[web:1024][web:1031]
    """

    def __init__(self) -> None:
        self.tasks: Dict[str, Task] = {}
        self.task_states: Dict[str, TaskState] = {}

        # For simplicity, create a tiny multiverse with a single subsystem
        # that we interpret as "global state" affected by tasks.
        dim = 4
        projectors = make_level_projectors_example(dim=dim)
        self.functional = GRAFunctional(
            projectors=projectors,
            local_loss=local_loss_mse,
            lambda0=1.0,
            alpha=0.5,
        )

        # Single-subsystem multiverse (index = ("global",), level = 0).
        psi0 = [0.0] * dim
        sub = Subsystem(index=("global",), level=0, state=psi0, goal_data=None)
        self.multiverse = Multiverse(
            subsystems={sub.index: sub},
            parents={},
        )

    # ----- Task management -----

    def create_task(
        self,
        task_type: str,
        goal_level: int,
        payload: Dict[str, Any],
        constraints: Optional[Dict[str, Any]] = None,
    ) -> Task:
        task_id = str(uuid.uuid4())
        session_id = "session-0"
        if constraints is None:
            constraints = {}
        task = Task(
            task_id=task_id,
            session_id=session_id,
            task_type=task_type,
            goal_level=goal_level,
            payload=payload,
            constraints=constraints,
        )
        self.tasks[task_id] = task
        self.task_states[task_id] = TaskState(task_id=task_id, state="created")
        return task

    # ----- IO helpers -----

    def send(self, obj: Dict[str, Any]) -> None:
        """Send a JSON line to stdout."""
        sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
        sys.stdout.flush()

    def recv(self) -> Optional[Dict[str, Any]]:
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

    # ----- Main loop -----

    def run(self) -> None:
        """
        Main loop:

        1. Create a demo task.
        2. Send it as TaskAssignment to the agent.
        3. Wait for TaskResult / TaskFailure.
        4. Print updated J_multiverse.[web:1024]
        """
        # 1. Create demo task
        task = self.create_task(
            task_type="vector_task",
            goal_level=0,
            payload={"vector": [0.1, 0.2, 0.3, 0.4]},
        )

        # 2. Send TaskAssignment
        assignment = {
            "type": "TaskAssignment",
            "task": asdict(task),
            "context": {
                "session_id": task.session_id,
                "history": [],
                "extra": {},
            },
        }
        self.send(assignment)

        # 3. Wait for responses
        for incoming in iter(self.recv, None):
            msg_type = incoming.get("type")
            if msg_type == "TaskResult":
                self.handle_task_result(incoming)
                break
            elif msg_type == "TaskFailure":
                self.handle_task_failure(incoming)
                break
            else:
                # ignore unknown messages in this minimal example
                continue

        # 4. Print final J_multiverse
        j_val = self.functional.J_multiverse(self.multiverse)
        sys.stderr.write(f"Final J_multiverse = {j_val:.6f}\n")
        sys.stderr.flush()

    # ----- Handlers -----

    def handle_task_result(self, msg: Dict[str, Any]) -> None:
        task_id = msg.get("task_id")
        if task_id not in self.tasks:
            return
        state = self.task_states[task_id]
        state.state = "completed"
        state.output = msg.get("output", {})
        state.metrics = msg.get("metrics", {})

        # Optionally, update multiverse state from result (toy: copy vector).
        vec = state.output.get("vector")
        if isinstance(vec, list):
            sub = self.multiverse.subsystems[("global",)]
            sub.state = np.array(vec, dtype=float)  # type: ignore[name-defined]

    def handle_task_failure(self, msg: Dict[str, Any]) -> None:
        task_id = msg.get("task_id")
        if task_id not in self.tasks:
            return
        state = self.task_states[task_id]
        state.state = "failed"
        state.error = msg.get("error_message", "unknown")


if __name__ == "__main__":
    server = SimpleForumServer()
    server.run()
