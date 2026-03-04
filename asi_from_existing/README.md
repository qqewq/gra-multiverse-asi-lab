# Applying GRA to Existing AI / Применение GRA к существующему ИИ

**RU / EN bilingual**

---

## RU: Обзор

Этот каталог описывает, как многоуровневая GRA Мета-обнулёнка может быть применена к **уже существующему ИИ‑агенту** (LLM‑стек, оркестратор агентов, продакшен‑бот и т.п.), чтобы задать для него формальную цель self-improvement и безопасный цикл самомодификации.[file:850][web:963][web:1044]

Каталог `asi_from_existing/` содержит:

- общую документацию (этот файл и `docs/03_asi_from_existing_agent.md`);
- игрушечный прототип (`toy_agent/`);
- ноутбуки с примерами динамики self-improvement.[web:1044][web:1045]

---

### RU: Структура каталога

```text
asi_from_existing/
├─ README.md                      # этот файл (RU/EN)
├─ toy_agent/
│  ├─ model.py                    # простая модель-агент
│  ├─ gra_wrapper.py              # обвязка GRA вокруг агента
│  └─ self_improve_loop.py        # цикл self-improvement
└─ notebooks/
   └─ 01_toy_self_improving_agent.ipynb
