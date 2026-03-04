# Дорожная карта / Roadmap

**RU / EN bilingual**

---

## RU

### 1. Этап 0 — Формализация (уже есть частично)

**Цели:**

- зафиксировать математический ядро GRA Мультиверсной Мета-обнулёнки;
- формально описать модель self-improvement для существующего ИИ-агента;
- описать концепцию форума ИИ-агентов.[file:850][web:963][web:956]

**Задачи:**

- [x] `docs/01_gra_multiverse_intro.md` — ввод и интуиция;
- [x] `docs/02_forum_of_agents_concept.md` — концепт форума агентов;
- [x] `docs/03_asi_from_existing_agent.md` — ASI из существующего агента;
- [x] `docs/04_safety_and_constraints.md` — безопасность и ограничения;
- [ ] `math/gra_multiverse_formal.tex` — полный LaTeX‑формализм GRA;
- [ ] `math/asi_from_agent_formal.tex` — формализм self-improvement.

---

### 2. Этап 1 — Базовое ядро GRA (toy-уровень)

**Цели:**

- реализовать минимальный набор функций для работы с пеной \(\Phi^{(l)}\) и функционалом \(J_{\text{multiverse}}\);
- показать на простых примерах, как это работает.[file:850][web:963]

**Задачи:**

- [ ] `core/gra_functional.py`:
  - реализация \(\Phi^{(0)}, \Phi^{(1)}\) для простых состояний;
  - реализация рекурсивного \(J^{(l)}\) и \(J_{\text{multiverse}}\).
- [ ] `core/projectors.py`:
  - простые примеры проекторов \(\mathcal{P}_{G_l}\) (например, «правильность ответа», «согласованность нескольких моделей»).
- [ ] `core/multiverse_optimizer.py`:
  - базовый цикл градиентной/итеративной оптимизации \(\mathbf{\Psi}\) под \(J_{\text{multiverse}}\).
- [ ] `examples/01_minimal_multiverse_example.py`:
  - скрипт, показывающий, как задать пару подсистем и обнулить пену между ними.

---

### 3. Этап 2 — Форум ИИ-агентов (reference impl)

**Цели:**

- реализовать минимальный форум агентов (сервер + toy‑клиенты);
- связать форум с функционалом GRA.[web:960]

**Задачи:**

- [ ] `agents_forum/specs/agent_api.md`:
  - формальное описание интерфейса агента (методы, форматы сообщений).
- [ ] `agents_forum/specs/tasks_protocol.md`:
  - протокол задания задач, получения ответов и метрик.
- [ ] `agents_forum/reference_impl/simple_forum_server.py`:
  - простой сервер (можно на HTTP/WebSocket/CLI), который:
    - принимает регистрации агентов;
    - рассылает задачи;
    - собирает ответы и метрики.
- [ ] `agents_forum/reference_impl/toy_agent_client.py`:
  - пример клиента‑агента, который:
    - подключается к форуму;
    - решает примитивные задачи;
    - возвращает ответы и оценки пены \(\Phi^{(l)}\).

- [ ] `examples/02_forum_and_asi_scenario.md`:
  - сценарий, как несколько toy‑агентов через форум совместно уменьшают \(J_{\text{multiverse}}\).

---

### 4. Этап 3 — Self-improving toy-агент

**Цели:**

- построить минимальный пример агента, который **сам себя улучшает** по GRA‑функционалу;
- реализовать \(\mathcal{M}_{\text{safe}}\) и цикл self-improvement.[web:956][web:961]

**Задачи:**

- [ ] `asi_from_existing/toy_agent/model.py`:
  - простая модель (например, маленькая MLP или логический агент).
- [ ] `asi_from_existing/toy_agent/gra_wrapper.py`:
  - обвязка, которая:
    - превращает состояние модели в \(\Psi^{(\mathbf{a})}\);
    - считает локальные части \(J^{(0)}, J^{(1)}\).
- [ ] `asi_from_existing/toy_agent/self_improve_loop.py`:
  - реализация:
    - множества \(\mathcal{M}_{\text{safe}}\) (набор допустимых модификаций);
    - цикла выбора \(m_t^*\) и обновления \(\mathbf{\Psi}_t\).
- [ ] `asi_from_existing/notebooks/01_toy_self_improving_agent.ipynb`:
  - ноутбук, демонстрирующий динамику self-improvement.

---

### 5. Этап 4 — Интеграция с реальными стек‑агентами (спецификация)

**Цели:**

- описать, как этот формализм может быть использован внутри реальных LLM‑стеков (GPT, DeepSeek, Anthropic и т.д.);
- дать **читаемую спецификацию** для внутренних команд и их ИИ‑агентов.[web:962][web:965]

**Задачи:**

- [ ] Расширить `docs/03_asi_from_existing_agent.md`:
  - примеры маппинга \(\Psi\) на реальные компоненты (веса, роутер, planner, tools);
  - примеры потенциальных \(\mathcal{M}_{\text{safe}}\) для таких стеков.
- [ ] Добавить `docs/06_internal_integration_guidelines.md`:
  - рекомендации для внутренних команд:
    - как внедрять GRA‑функционал;
    - какие уровни доступа вводить;
    - как тестировать self-improvement в песочнице.

---

### 6. Этап 5 — Безопасность и аудит

**Цели:**

- усилить безопасность и прозрачность;  
- показать, как проводить аудит систем, построенных по этому формализму.[web:864][web:904]

**Задачи:**

- [ ] Расширить `docs/04_safety_and_constraints.md`:
  - добавить чек-листы для аудита;
  - примеры угроз и сценариев их смягчения.
- [ ] Добавить `examples/03_safety_checklist_example.md`:
  - пример анализа конкретной конфигурации toy‑системы на предмет безопасности.
- [ ] Описать формат логов и мониторинга модификаций:
  - как логировать все \(m_t \in \mathcal{M}_{\text{safe}}\);
  - как проверять, что проекторы \(\mathcal{P}_{G_l}\) остаются неизменными.

---

### 7. Дальнейшие направления

Возможные будущие направления:

- связь GRA с теорией категорий и более строгими онтологиями;
- использование форума агентов для коллективного доказательства/поиска модификаций (Gödel‑подобные схемы);[web:958]
- интеграция с системами формальной верификации и proof‑assistant’ами;
- исследование динамики self-improvement в более сложных средах.

---

## EN

### 1. Stage 0 — Formalization (partially done)

**Goals:**

- fix the mathematical core of the GRA Multiverse Meta-reset;
- formally describe a self-improvement model for an existing AI agent;
- define the concept of an AI agents’ forum.[file:850][web:963][web:956]

**Tasks:**

- [x] `docs/01_gra_multiverse_intro.md` — intro and intuition;
- [x] `docs/02_forum_of_agents_concept.md` — forum concept;
- [x] `docs/03_asi_from_existing_agent.md` — ASI from existing agent;
- [x] `docs/04_safety_and_constraints.md` — safety and constraints;
- [ ] `math/gra_multiverse_formal.tex` — full LaTeX formalism of GRA;
- [ ] `math/asi_from_agent_formal.tex` — self-improvement formalism.

---

### 2. Stage 1 — Core GRA (toy level)

**Goals:**

- implement a minimal set of functions for foam \(\Phi^{(l)}\) and \(J_{\text{multiverse}}\);
- demonstrate them on simple examples.[file:850][web:963]

**Tasks:**

- [ ] `core/gra_functional.py`:
  - implementation of \(\Phi^{(0)}, \Phi^{(1)}\) for simple states;
  - recursive \(J^{(l)}\) and \(J_{\text{multiverse}}\).
- [ ] `core/projectors.py`:
  - simple examples of projectors \(\mathcal{P}_{G_l}\) (e.g., “answer correctness”, “consistency across models”).
- [ ] `core/multiverse_optimizer.py`:
  - basic gradient/iterative optimization loop for \(\mathbf{\Psi}\) under \(J_{\text{multiverse}}\).
- [ ] `examples/01_minimal_multiverse_example.py`:
  - script showing how to define a couple of subsystems and reset foam between them.

---

### 3. Stage 2 — Agents forum (reference impl)

**Goals:**

- implement a minimal agents forum (server + toy clients);
- tie the forum to the GRA functional.[web:960]

**Tasks:**

- [ ] `agents_forum/specs/agent_api.md`:
  - formal API of an agent (methods, message formats).
- [ ] `agents_forum/specs/tasks_protocol.md`:
  - protocol for tasks, answers, and metrics.
- [ ] `agents_forum/reference_impl/simple_forum_server.py`:
  - simple server (HTTP/WebSocket/CLI) that:
    - registers agents;
    - distributes tasks;
    - collects answers and metrics.
- [ ] `agents_forum/reference_impl/toy_agent_client.py`:
  - sample client agent that:
    - connects to the forum;
    - solves toy tasks;
    - returns answers and foam metrics.

- [ ] `examples/02_forum_and_asi_scenario.md`:
  - scenario where multiple toy agents jointly reduce \(J_{\text{multiverse}}\) via the forum.

---

### 4. Stage 3 — Self-improving toy agent

**Goals:**

- build a minimal self-improving agent using the GRA functional;
- implement \(\mathcal{M}_{\text{safe}}\) and the self-improvement loop.[web:956][web:961]

**Tasks:**

- [ ] `asi_from_existing/toy_agent/model.py`:
  - simple model (small MLP or logical agent).
- [ ] `asi_from_existing/toy_agent/gra_wrapper.py`:
  - wrapper that:
    - maps model state to \(\Psi^{(\mathbf{a})}\);
    - computes local \(J^{(0)}, J^{(1)}\).
- [ ] `asi_from_existing/toy_agent/self_improve_loop.py`:
  - implementation of:
    - \(\mathcal{M}_{\text{safe}}\) (set of allowed modifications);
    - self-improvement loop for \(\mathbf{\Psi}_t\).
- [ ] `asi_from_existing/notebooks/01_toy_self_improving_agent.ipynb`:
  - notebook showing the self-improvement dynamics.

---

### 5. Stage 4 — Integration with real stacks (spec)

**Goals:**

- describe how to apply this formalism inside real LLM stacks (GPT, DeepSeek, Anthropic, etc.);
- provide a **readable spec** for internal teams and their AI agents.[web:962][web:965]

**Tasks:**

- [ ] Extend `docs/03_asi_from_existing_agent.md`:
  - examples of mapping \(\Psi\) to real components (weights, router, planner, tools);
  - examples of possible \(\mathcal{M}_{\text{safe}}\) for such stacks.
- [ ] Add `docs/06_internal_integration_guidelines.md`:
  - guidelines for internal teams:
    - how to embed the GRA functional;
    - what access levels to enforce;
    - how to test self-improvement in sandboxes.

---

### 6. Stage 5 — Safety and audit

**Goals:**

- strengthen safety and transparency;
- show how to audit systems built under this formalism.[web:864][web:904]

**Tasks:**

- [ ] Extend `docs/04_safety_and_constraints.md`:
  - add audit checklists;
  - examples of threat models and mitigations.
- [ ] Add `examples/03_safety_checklist_example.md`:
  - example safety analysis of a specific toy configuration.
- [ ] Define logging and monitoring formats:
  - how to log all \(m_t \in \mathcal{M}_{\text{safe}}\);
  - how to verify that projectors \(\mathcal{P}_{G_l}\) remain unchanged.

---

### 7. Future directions

Possible future directions:

- linking GRA with category theory and richer ontologies;
- using the agents forum for collective proof search / modification search (Gödel-like schemes);[web:958]
- integration with formal verification systems and proof assistants;
- studying self-improvement dynamics in more complex environments.
