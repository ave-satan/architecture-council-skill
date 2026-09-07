---
architecture_revision: "{{REVISION}}"
feature: "{{FEATURE_NAME}}"
artifact: migration_rehearsal
status: "{{PLANNED|COMPLETE|FAILED|INCONCLUSIVE|NOT_REQUIRED}}"
owner: "{{OWNER}}"
execution_authorization: "{{NOT_REQUESTED|AUTHORIZED_WITH_LINK}}"
artifact_language: "{{USER_LANGUAGE}}"
executed_at: "{{YYYY-MM-DD}}"
---

# Репетиция миграции

`PLANNED` не означает, что rehearsal разрешена. Изменяющий проект или данные
прогон требует отдельной явной команды пользователя и disposable scope.

## Scope и среда

- Migration version: {{VERSION}}
- Dataset shape/size: {{DESCRIPTION}}
- Environment differences: {{DESCRIPTION}}

## Предварительные условия

- {{CHECK}}

## Процедура и наблюдения

| Шаг | Ожидание | Наблюдение | Длительность | Результат |
|---|---|---|---:|---|
| {{STEP}} | {{EXPECTED}} | {{OBSERVED}} | {{DURATION}} | {{PASS/FAIL}} |

## Валидация и reconciliation

- Record counts/checksums: {{RESULT}}
- Business invariants: {{RESULT}}
- Compatibility during transition: {{RESULT}}

## Репетиция rollback

- Performed: {{yes/no}}
- Result: {{RESULT}}
- Data consequences: {{DESCRIPTION}}

## Findings и влияние на решение

- {{FINDING_OR_NONE}}

При `NOT_REQUIRED` зафиксируй, почему изменение не содержит миграции или
опасного переходного состояния, и приложи ссылку на Evolution Plan.
