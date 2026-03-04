https://doi.org/10.5281/zenodo.18859500
https://orcid.org/my-orcid?orcid=0009-0004-1872-1153
# GRA Multiverse ASI Lab

**RU / EN bilingual**

---

## RU: Описание проекта

**GRA Multiverse ASI Lab** — это экспериментальная и формальная архитектура для:

- мультиверсной GRA Мета-обнулёнки,
- форума ИИ-агентов,
- построения self-improving ASI из уже существующих ИИ-агентов (LLM-стеков и др.).[file:850][web:963]

Цель репозитория — не «ASI по кнопке», а:

- строгий математический формализм,
- toy-реализации,
- понятное техзадание, по которому внутренние команды и их ИИ-агенты могут строить реальные self-improving системы.[web:956][web:960]

---

### RU: Идея

1. **GRA Мета-обнулёнка** задаёт многоуровневый функционал
   \(J_{\text{multiverse}}\), который минимизирует «пену» \(\Phi^{(l)}\) на всех уровнях иерархии состояний (домен, мета-домен, мультиверс).[file:850][web:963]

2. **Форум ИИ-агентов** использует этот функционал как общую цель:
   разные агенты совместно ищут модификации кода/архитектуры/политики, которые уменьшают \(J_{\text{multiverse}}\), соблюдая ограничения безопасности.[web:956][web:961]

3. **Существующие ИИ-агенты** (LLM и др.) рассматриваются как исходные состояния \(\Psi_0\).
   Над ними запускается безопасный цикл самооптимизации с ограниченным множеством модификаций \(\mathcal{M}_{\text{safe}}\), которые не меняют сами цели (проектор \(\mathcal{P}_{G_l}\)).[web:961][web:964]

---

### RU: Структура репозитория
## EN: Idea

GRA Meta-Nullification defines a multi-level functional \(J_{\text{multiverse}}\) that minimizes the “foam” \(\Phi^{(l)}\) across all levels of the state hierarchy (domain, meta-domain, multiverse).

The AI agents forum uses this functional as a shared objective: different agents jointly search for code/architecture/policy modifications that decrease \(J_{\text{multiverse}}\) while respecting safety constraints.

Existing AI agents (LLMs and others) are treated as initial states \(\Psi_0\). A safe self-optimization loop runs on top of them with a restricted set of modifications \(\mathcal{M}_{\text{safe}}\) that do not change the goals themselves (the projector \(\mathcal{P}_{G_l}\)).
```text
gra-multiverse-asi-lab/
├─ README.md                # этот файл (RU/EN)
├─ LICENSE
│
├─ docs/
│  ├─ 01_gra_multiverse_intro.md
│  ├─ 02_forum_of_agents_concept.md
│  ├─ 03_asi_from_existing_agent.md
│  ├─ 04_safety_and_constraints.md
│  └─ 05_roadmap.md
│
├─ math/
│  ├─ gra_multiverse_formal.tex          # формализм мультиверсной GRA
│  └─ asi_from_agent_formal.tex          # формальная модель self-improvement
│
├─ core/
│  ├─ gra_functional.py                  # Φ^(l), J^(l), J_multiverse
│  ├─ projectors.py                      # задание P_{G_l}
│  └─ multiverse_optimizer.py            # общий цикл обнуления
│
├─ agents_forum/
│  ├─ README.md                          # концепция форума агентов
│  ├─ specs/
│  │  ├─ agent_api.md                    # интерфейс ИИ-агентов
│  │  └─ tasks_protocol.md               # протокол задач/общения
│  └─ reference_impl/
│     ├─ simple_forum_server.py          # минимальный "форум"
│     └─ toy_agent_client.py             # пример клиента-агента
│
├─ asi_from_existing/
│  ├─ README.md                          # как применять GRA к существующему ИИ
│  ├─ toy_agent/
│  │  ├─ model.py                        # простая модель-агент
│  │  ├─ gra_wrapper.py                  # обвязка GRA вокруг агента
│  │  └─ self_improve_loop.py            # цикл самосовершенствования
│  └─ notebooks/
│     └─ 01_toy_self_improving_agent.ipynb
│
└─ examples/
   ├─ 01_minimal_multiverse_example.py   # минимальное использование core/
   └─ 02_forum_and_asi_scenario.md       # сценарий "форум агентов строит ASI"



