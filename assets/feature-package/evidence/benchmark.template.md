---
architecture_revision: "{{REVISION}}"
benchmark_id: "BENCH-{{NNN}}"
status: "{{PLANNED|RUNNING|COMPLETE|INVALID}}"
owner: "{{OWNER}}"
execution_authorization: "{{NOT_REQUESTED|AUTHORIZED_WITH_LINK}}"
artifact_language: "{{USER_LANGUAGE}}"
executed_at: "{{YYYY-MM-DD}}"
---

# BENCH-{{NNN}}: {{QUESTION}}

Планирование benchmark не разрешает его запуск. Если benchmark меняет проект,
данные или внешнее состояние, приложи явную команду пользователя.

## Требование/решение

- Requirements: {{QA_IDS}}
- Informs: {{OPTION_ADR_OR_CONFLICT}}

## Среда

- Hardware/runtime: {{DESCRIPTION}}
- Versions/configuration: {{DESCRIPTION}}
- Differences from production: {{DESCRIPTION}}

## Нагрузка и данные

- Traffic model: {{RPS_CONCURRENCY_DURATION}}
- Dataset: {{SIZE_SHAPE_DISTRIBUTION}}
- Warm-up/repetitions: {{DESCRIPTION}}

## Метрики и критерии прохождения

| Метрика | Цель | Метод измерения |
|---|---:|---|
| {{METRIC}} | {{TARGET}} | {{METHOD}} |

## Результаты

| Метрика | Наблюдение | Разброс/интервал | Проход |
|---|---:|---:|---|
| {{METRIC}} | {{VALUE}} | {{VALUE}} | {{yes/no}} |

## Артефакты

- Commands/configuration: {{LINK}}
- Raw results: {{LINK}}
- Charts/logs: {{LINK}}

## Ограничения

- {{LIMITATION}}

## Влияние на решение

{{WHAT_IS_CONFIRMED_REFUTED_OR_STILL_UNKNOWN}}
