# Tasks Protocol / Протокол задач и общения

**RU / EN bilingual**

---

## RU

Этот документ описывает минимальный протокол задач и сообщений между форумом и агентами.[file:850][web:1019] Он не привязан к конкретному транспорту (HTTP, WebSocket, gRPC и т.п.) и задаёт только структуру и семантику сообщений.

Основные сущности:

- `Task` — единица работы, которую форум назначает агенту.
- `TaskState` — состояние задачи (created, running, completed, failed, cancelled).
- `Message` — обмен контекстом, результатами и метриками.
- `Session` — логическая сессия / контекст, в котором живут задачи.[web:1015][web:1022]

---

### RU: Task

#### Структура `Task`

```json
{
  "task_id": "string",
  "session_id": "string",
  "created_at": "ISO-8601",
  "task_type": "qa | vector_task | planning | meta_eval | ...",
  "goal_level": 0,
  "payload": {},
  "constraints": {
    "max_steps": 32,
    "timeout_ms": 5000,
    "resource_limits": {
      "cpu_ms": 100,
      "tokens": 2048
    }
  }
}
