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

`PLANNED` не означает, что репетиция разрешена. Изменяющий проект или данные
прогон требует отдельной явной команды пользователя и изолированной среды.

## Область проверки и среда

- Версия миграции: {{VERSION}}
- Структура/объём данных: {{DESCRIPTION}}
- Отличия среды: {{DESCRIPTION}}

## Предварительные условия

- {{CHECK}}

## Процедура и наблюдения

| Шаг | Ожидание | Наблюдение | Длительность | Результат |
|---|---|---|---:|---|
| {{STEP}} | {{EXPECTED}} | {{OBSERVED}} | {{DURATION}} | {{PASS/FAIL}} |

## Валидация и сверка данных

- Количество записей/контрольные суммы: {{RESULT}}
- Бизнес-инварианты: {{RESULT}}
- Совместимость во время перехода: {{RESULT}}

## Репетиция отката

- Выполнено: {{YES_OR_NO}}
- Результат: {{RESULT}}
- Последствия для данных: {{DESCRIPTION}}

## Замечания и влияние на решение

- {{FINDING_OR_NONE}}

При `NOT_REQUIRED` зафиксируй, почему изменение не содержит миграции или
опасного переходного состояния, и приложи ссылку на [план перехода](../delivery-plan.md).
