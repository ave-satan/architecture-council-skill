---
feature: "{{FEATURE_NAME}}"
artifact: verbose_review
architecture_revision: "{{REVISION}}"
diagnostics_mode: "{{DIAGNOSTICS_MODE}}"
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# Ретроспектива verbose-прогона

Этот evidence описывает наблюдаемое поведение процесса. Он не содержит
chain-of-thought, сырых prompts, секретов, исходного кода или полных tool outputs
и не переопределяет нормативную архитектуру.

## Краткий итог

{{OBSERVED_RUN_SUMMARY}}

## Метрики прогона

| Метрика | Значение | Источник |
|---|---:|---|
| События | {{COUNT}} | [журнал событий](process-log.md) |
| Запуски ролей | {{COUNT}} | [Process Ledger](../process-ledger.md) |
| Возвраты между стадиями | {{COUNT}} | [журнал событий](process-log.md) |
| Уточнения пользователя | {{COUNT}} | [журнал событий](process-log.md) |
| Ошибки и восстановления | {{COUNT}} | [журнал событий](process-log.md) |

## Временные и процессные узкие места

| ID | Наблюдение | Evidence | Влияние |
|---|---|---|---|
| VR-001 | {{OBSERVATION}} | {{EVENT_IDS_OR_LINK}} | {{IMPACT}} |

## Сработавшие защиты

| Gate/правило | Событие | Что предотвратило или обнаружило |
|---|---|---|
| {{GATE_OR_RULE}} | {{EVENT_IDS_OR_LINK}} | {{RESULT}} |

## Предполагаемые пробелы скилла или протокола

| ID | Пробел | Evidence | Предлагаемое изменение | Приоритет |
|---|---|---|---|---|
| VR-GAP-001 | {{GAP}} | {{EVENT_IDS_OR_LINK}} | {{CHANGE}} | {{HIGH_MEDIUM_LOW}} |

## Что сохранить без изменений

- {{PRACTICE}}

## Ограничения ретроспективы

- {{MISSING_OR_UNRELIABLE_OBSERVATION}}
