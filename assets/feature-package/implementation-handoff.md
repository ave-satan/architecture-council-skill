---
feature: "{{FEATURE_NAME}}"
artifact: implementation_handoff
architecture_revision: "{{REVISION}}"
human_review_status: "{{AWAITING_HUMAN_REVIEW|CHANGES_REQUESTED|APPROVED|REJECTED|ON_HOLD}}"
implementation_start: "NOT_REQUESTED"
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# Передача решения в реализацию

## Текущий статус

- Architecture Package revision: `{{REVISION}}`
- Human review: `{{HUMAN_REVIEW_STATUS}}`
- Implementation start: `NOT_REQUESTED`
- **Этот документ не разрешает менять проект.**

## Условия до старта

- {{APPROVAL_EVIDENCE_OR_OPEN_CONDITION}}

## Разрешаемый начальный scope

- Рекомендуемый первый инкремент: {{INC_ID}}
- Включено: {{SCOPE}}
- Не включено: {{EXCLUSIONS}}
- Обязательные gates: {{VERIFICATION_AND_EVIDENCE}}

## Нормативные входы

1. [Final Decision](final-decision.md)
2. [Requirements](requirements.md)
3. [Target Architecture](target-architecture.md)
4. [ADR](adr/)
5. [Delivery Plan](delivery-plan.md)
6. [Verification Plan](verification-plan.md)

## Инструкция для новой сессии

Используй только после отдельной явной команды пользователя:

> Изучи Architecture Package по пути `{{ABSOLUTE_OR_PROJECT_RELATIVE_PATH}}`,
> revision `{{REVISION}}`. Человеческое review имеет статус
> `{{HUMAN_REVIEW_STATUS}}` и подтверждено `{{APPROVAL_EVIDENCE}}`. Начни только
> инкремент `{{INC_ID}}` в scope `{{SCOPE}}`. Перед изменениями проверь revisions
> пакета и кода. Не меняй утверждённые требования и ADR без отдельного
> согласования. Выполни проверки `{{VERIFICATION_IDS}}`.

## Явная команда, которой пока нет

Реализация начинается только после сообщения пользователя, эквивалентного:

> Утверждаю Architecture Package revision `{{REVISION}}`. Начинай реализацию
> инкремента `{{INC_ID}}` в указанном scope.

Approval, консенсус Council и наличие этого файла не заменяют такую команду.
