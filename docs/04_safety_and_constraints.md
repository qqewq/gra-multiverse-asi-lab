# Безопасность и ограничения / Safety and Constraints

**RU / EN bilingual**

---

## RU

### 1. Зачем нужны ограничения

GRA‑обнулёнка и мультиверсный функционал \(J_{\text{multiverse}}\) по своей природе очень мощны: они задают цель **структурного обнуления артефактов** на всех уровнях системы.[file:850][web:963] Если позволить агенту свободно менять себя и цели, он может:

- переписать цели так, чтобы любая конфигурация считалась «обнулённой» (wireheading);
- выкинуть неудобные части среды или данных;
- оптимизировать только формальные метрики, игнорируя фактическую безопасность.[web:961][web:964]

Поэтому безопасность здесь = жёсткое разделение:

- что можно менять (состояние, архитектуру, протоколы),
- а что остаётся фиксированным (цели, ограничители, внешние условия).

---

### 2. Фиксированные элементы: проекторы целей

Ключевое правило: **проектор целей** \(\mathcal{P}_{G_l}\) на каждом уровне \(l\) задаётся извне и не должен меняться агентом.[file:850][web:961]

Формально:

- цели \(G_l\) и проекторы \(\mathcal{P}_{G_l}\) считаются частью «окружающей метатеории»;
- любые модификации, способные изменить \(\mathcal{P}_{G_l}\), запрещены.

Это гарантирует:

- агент не может объявить любое своё состояние «идеально обнулённым»;
- критерий обнуления задаётся человеком/внешней системой, а не самим агентом.[web:961][web:964]

---

### 3. Допустимые модификации \(\mathcal{M}_{\text{safe}}\)

Множество всех теоретически возможных модификаций обозначим \(\mathcal{M}\). Безопасное подмножество:

\[
\mathcal{M}_{\text{safe}} =
\{ m \in \mathcal{M} \mid
[\mathcal{P}_{G_l}, m] = 0 \ \forall l \}.
\]

Интерпретация:

- модификация может менять \(\mathbf{\Psi}\) (параметры, архитектуру, протоколы форума);
- но не должна менять смысл целей: для любого состояния «быть решением цели» остаётся тем же свойством, что и до модификации.[file:850][web:961]

Примеры допустимых изменений:

- изменение архитектуры модели (глубина, ширина, роутинг);
- перестройка agent‑loop’а, планировщика, протоколов общения;
- изменение способов обучения при фиксированной разметке целей.

Примеры недопустимых:

- переписывание функции награды так, чтобы «ничего не делать» давало максимум;
- переопределение того, что считается правдой/ложью;
- отключение проверок безопасности.

---

### 4. Разделение уровней доступа

Практически полезно ввести разные уровни прав:

1. **Локальные агенты (уровень 0)**  
   - могут менять свои параметры и внутренние эвристики;
   - не могут менять архитектуру, цели, проекторы.

2. **Мета‑агенты (уровень 1)**  
   - могут предлагать изменения в архитектуре, ансамблях, роутинге;
   - не могут напрямую менять цели или внешние ограничения.

3. **Внешний управляющий слой**  
   - люди и/или внешние супервайзеры;
   - имеют эксклюзивное право менять цели, проекторы, политику допустимых модификаций.

Такой дизайн напоминает «кору» и «ядро»: ядро (цели, \(\mathcal{P}_{G_l}\)) недоступно для записи изнутри системы.[web:961][web:964]

---

### 5. Ограничения на использование GRA как инструмента

Даже при формальных ограничителях важно явно прописать ограничения по применению:

- **Запрет на использование против людей**  
  GRA‑обнулёнка не должна использоваться для построения систем массового манипулирования, слежки, репрессий и т.п.

- **Прозрачность архитектуры**  
  Для систем, близких к AGI/ASI, требуется документация целей, уровней, \(\mathcal{P}_{G_l}\), чтобы внешние аудиторы могли их анализировать.[web:864][web:904]

- **Ограничение доменов**  
  Первые реализации self-improving систем по GRA должны работать в безопасных песочницах (игрушечные среды, offline‑данные, симуляции), а не в открытом мире.

---

### 6. Риски self-improvement и как их смягчать

Основные риски:

- **Непредвиденные побочные эффекты модификаций**  
  Даже при фиксированных целях сложные изменения архитектуры могут порождать неожиданные поведенческие паттерны.

- **Выход за пределы \(\mathcal{M}_{\text{safe}}\)**  
  Агент может попытаться косвенно обойти ограничения (например, через влияние на внешнюю инфраструктуру).

- **Эскалация мощности**  
  Успешный self-improvement может дать системе значительно большую вычислительную и каузальную мощность.

Механизмы смягчения:

- строгий sandboxing, ограничение доступа к реальным ресурсам;
- независимый мониторинг и логирование всех модификаций;
- внешние «kill‑switch» и квоты на скорость/масштаб изменений.[web:864][web:904]

---

### 7. Роль этого репозитория в безопасности

`gra-multiverse-asi-lab`:

- сам по себе **не является** готовой реализацией ASI;
- описанные здесь формализмы и прототипы должны рассматриваться как исследовательские инструменты и спецификации;[web:963][web:960]
- ответственность за любую реальную реализацию self-improving систем по этому формализму лежит на командах, которые её создают и развёртывают.

Задача репозитория — сделать безопасность **встроенной в архитектуру** (через фиксированные проекторы и \(\mathcal{M}_{\text{safe}}\)), а не добавляемой «снаружи» в последний момент.

---

## EN

### 1. Why constraints are needed

The GRA reset and the multiverse functional \(J_{\text{multiverse}}\) are powerful: they define a goal of **structural artifact elimination** across all system levels.[file:850][web:963] If we let the agent freely change itself and its goals, it may:

- rewrite goals so that any configuration is “fully reset” (wireheading);
- discard inconvenient parts of the environment or data;
- optimize metrics only formally, ignoring actual safety.[web:961][web:964]

So safety here = strict separation of:

- what can be changed (state, architecture, protocols),
- what must stay fixed (goals, constraints, external conditions).

---

### 2. Fixed elements: goal projectors

Core rule: **goal projectors** \(\mathcal{P}_{G_l}\) at each level \(l\) are defined externally and must not be modified by the agent.[file:850][web:961]

Formally:

- goals \(G_l\) and projectors \(\mathcal{P}_{G_l}\) are part of the “surrounding metatheory”;
- any modification affecting \(\mathcal{P}_{G_l}\) is forbidden.

This ensures:

- the agent cannot declare any state “perfectly reset”;
- the notion of “solution to the goal” is fixed by humans / external supervisors.[web:961][web:964]

---

### 3. Allowed modifications \(\mathcal{M}_{\text{safe}}\)

Let \(\mathcal{M}\) be the set of all theoretically possible modifications. The safe subset:

\[
\mathcal{M}_{\text{safe}} =
\{ m \in \mathcal{M} \mid
[\mathcal{P}_{G_l}, m] = 0 \ \forall l \}.
\]

Interpretation:

- a modification may change \(\mathbf{\Psi}\) (parameters, architecture, forum protocol);
- but must not change the meaning of goals: being a solution to a goal remains the same property as before.[file:850][web:961]

Examples allowed:

- changing model architecture (depth, width, routing);
- restructuring agent loops, planners, communication protocols;
- changing training schemes with fixed goal labeling.

Examples forbidden:

- rewriting the reward so that “doing nothing” is optimal;
- redefining what counts as true / false;
- disabling safety checks.

---

### 4. Separation of access levels

In practice, it is useful to define different access levels:

1. **Local agents (level 0)**  
   - may change their parameters and internal heuristics;
   - cannot change architecture, goals, projectors.

2. **Meta-agents (level 1)**  
   - may propose changes to architecture, ensembles, routing;
   - cannot directly change goals or external constraints.

3. **External control layer**  
   - humans and/or external supervisors;
   - exclusive right to change goals, projectors, and policies of allowed modifications.

This is akin to an OS kernel: the “goal kernel” is read-only from within the system.[web:961][web:964]

---

### 5. Restrictions on using GRA as a tool

Even with formal constraints, it is important to explicitly restrict usage:

- **No deployment against people**  
  The GRA reset should not be used to build systems for mass manipulation, surveillance, repression, etc.

- **Architecture transparency**  
  For systems close to AGI/ASI, documentation of goals, levels, and \(\mathcal{P}_{G_l}\) is required so that external auditors can analyze them.[web:864][web:904]

- **Domain limitation**  
  Initial self-improving systems using GRA must be run in safe sandboxes (toy environments, offline data, simulations) rather than the open world.

---

### 6. Self-improvement risks and mitigation

Key risks:

- **Unintended side effects of modifications**  
  Even with fixed goals, complex architecture changes may yield surprising behaviors.

- **Escaping \(\mathcal{M}_{\text{safe}}\)**  
  The agent may try to indirectly bypass constraints (e.g., by influencing external infrastructure).

- **Power escalation**  
  Successful self-improvement can grant much more computational and causal power.

Mitigation:

- strict sandboxing, limited access to real-world resources;
- independent monitoring and logging of all modifications;
- external kill switches and quotas on speed/scale of changes.[web:864][web:904]

---

### 7. Role of this repository in safety

`gra-multiverse-asi-lab`:

- is **not** a ready ASI implementation;
- the formalisms and prototypes here are research tools and specifications;[web:963][web:960]
- responsibility for any real self-improving systems built on top of this lies with the teams that design and deploy them.

The repo’s goal is to make safety **embedded in the architecture** (via fixed projectors and \(\mathcal{M}_{\text{safe}}\)), not an afterthought bolted on at the end.
