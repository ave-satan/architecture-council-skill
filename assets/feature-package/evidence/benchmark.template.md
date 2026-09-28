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

- Требования: {{QA_IDS}}
- Уточняемое решение: {{OPTION_ADR_OR_CONFLICT}}

## Среда

- Оборудование/среда исполнения: {{DESCRIPTION}}
- Версии/конфигурация: {{DESCRIPTION}}
- Отличия от рабочей среды: {{DESCRIPTION}}

## Нагрузка и данные

- Модель нагрузки: {{RPS_CONCURRENCY_DURATION}}
- Набор данных: {{SIZE_SHAPE_DISTRIBUTION}}
- Прогрев/повторы: {{DESCRIPTION}}

## Метрики и критерии прохождения

| Метрика | Цель | Метод измерения |
|---|---:|---|
| {{METRIC}} | {{TARGET}} | {{METHOD}} |

## Результаты

| Метрика | Наблюдение | Разброс/интервал | Проход |
|---|---:|---:|---|
| {{METRIC}} | {{VALUE}} | {{VALUE}} | {{yes/no}} |

## Артефакты

- Команды/конфигурация: {{LINK}}
- Сырые результаты: {{LINK}}
- Графики/логи: {{LINK}}

## Ограничения

- {{LIMITATION}}

## Влияние на решение

{{WHAT_IS_CONFIRMED_REFUTED_OR_STILL_UNKNOWN}}
