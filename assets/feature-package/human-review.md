---
feature: "{{FEATURE_NAME}}"
artifact: human_review
architecture_revision: "{{REVISION}}"
status: "{{AWAITING_HUMAN_REVIEW|CHANGES_REQUESTED|APPROVED|REJECTED|ON_HOLD}}"
reviewer: "{{PERSON_OR_EXTERNAL_OWNER}}"
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# Запись решения человека

Предмет ответа: [краткое решение](decision-brief.md), ревизия **{{REVISION}}**.
Агент заполняет запись по фактическому ответу; человеку не нужно редактировать файл.

| Дата / кто | Решение и условия | Источник ответа |
|---|---|---|
| {{DATE_AND_OWNER_OR_PENDING}} | {{ACTUAL_DECISION_OR_PENDING}} | {{MESSAGE_REFERENCE_OR_EXTERNAL_LINK_OR_PENDING}} |

{{ONLY_ACTUAL_COMMENTS_RESPONSES_AND_REVIEW_HISTORY_OR_REMOVE_IF_NONE}}

Approval относится к указанной ревизии. Существенные изменения возвращаются на
review; реализация требует отдельной команды.
