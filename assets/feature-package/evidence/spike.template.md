---
architecture_revision: "{{REVISION}}"
spike_id: "SPIKE-{{NNN}}"
status: "{{PLANNED|RUNNING|COMPLETE|INCONCLUSIVE}}"
owner: "{{OWNER}}"
timebox: "{{DURATION}}"
execution_authorization: "{{NOT_REQUESTED|AUTHORIZED_WITH_LINK}}"
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# SPIKE-{{NNN}}: {{QUESTION}}

Описание spike не разрешает его запуск. Любые записи в проект, данные,
инфраструктуру или внешние системы требуют отдельной явной команды пользователя.

## Какое решение уточняет

{{OPTION_CONFLICT_ADR_OR_REQUIREMENT}}

## Бюджет ветки и остановка

{{BRANCH_LINK_OR_LOCAL_SCOPE_AND_TOTAL_BUDGET_INCLUDING_PREPARATION_REVIEW_AND_REPAIRS}}

- Достаточное evidence для решения: {{MINIMUM_DECISION_CHANGING_OBSERVATION}}
- Остановиться или сменить семейство: {{STOP_OR_SWITCH_CRITERION}}
- Почему следующий опыт изменит решение: {{EXPECTED_INFORMATION_GAIN}}

## Гипотеза

{{TESTABLE_HYPOTHESIS}}

## Scope и исключения

- Included: {{SCOPE}}
- Excluded: {{SCOPE}}

## Метод

1. {{STEP}}
2. {{STEP}}

## Критерии успеха и неопределённости

- Supports hypothesis if: {{CRITERION}}
- Refutes hypothesis if: {{CRITERION}}
- Inconclusive if: {{CRITERION}}

## Результат

- Outcome: `{{SUPPORTED|REFUTED|INCONCLUSIVE}}`
- Evidence: {{LINKS_OUTPUTS}}
- Limitations: {{LIMITATIONS}}

## Влияние на решение

{{WHAT_MUST_CHANGE_OR_WHAT_IS_NOW_CONFIRMED}}
