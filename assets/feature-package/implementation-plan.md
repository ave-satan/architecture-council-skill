---
feature: "{{FEATURE_NAME}}"
artifact: implementation_plan
architecture_revision: "{{REVISION}}"
human_review_status: "{{AWAITING_HUMAN_REVIEW|CHANGES_REQUESTED|APPROVED|REJECTED|ON_HOLD}}"
implementation_start: "NOT_REQUESTED"
code_revision: "{{COMMIT_OR_SNAPSHOT}}"
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# План реализации

Файл объединяет handoff, индекс задач и текущие статусы. Он не разрешает менять
проект без фактической команды пользователя.

## Граница запуска

| Review evidence | Разрешённый scope | Ближайшая работа | Проверки | Блокеры/исключения |
|---|---|---|---|---|
| {{APPROVAL_OR_OPEN}} | {{ACTUAL_USER_AUTHORIZED_SCOPE_OR_NOT_AUTHORIZED}} | {{TASK_ID}} | {{VER_IDS}} | {{ITEMS_OR_NONE}} |

<!-- AC:IMPLEMENTATION_TASKS -->
| Task | Increment | Requirements | Dependencies | Status | Blocker | Acceptance | Verification | Evidence |
|---|---|---|---|---|---|---|---|---|
| [TASK-001 — {{NAME}}](#task-001) | [INC-001](delivery-plan.md) | [{{REQ_IDS}}](requirements.md) | — | {{PLANNED|READY|BLOCKED|IN_PROGRESS|DONE|CANCELLED}} | {{REASON_OR_DASH}} | {{TESTABLE_RESULT}} | [{{VER_IDS}}](delivery-plan.md) | {{LINK_OR_DASH}} |

<a id="task-001"></a>
## TASK-001 — {{NAME}}

{{BOUNDED_SCOPE_INPUTS_ACCEPTANCE_AND_NON_GOALS_NEEDED_TO_START_WITHOUT_CHAT_HISTORY}}
