---
feature: "{{FEATURE_NAME}}"
artifact: final_architecture_decision
council_recommendation: "{{ACCEPTED|ACCEPTED_WITH_CONDITIONS|REWORK_REQUIRED|REJECTED|BLOCKED|ESCALATED}}"
design_maturity: "{{DESIGN_CANDIDATE|EVIDENCE_AUTHORIZED|IMPLEMENTATION_READY|NOT_READY}}"
human_review_status: "{{AWAITING_HUMAN_REVIEW|CHANGES_REQUESTED|APPROVED|REJECTED|ON_HOLD}}"
implementation_start: "NOT_REQUESTED"
architecture_revision: "{{REVISION}}"
decision_owner: "{{OWNER}}"
artifact_language: "{{USER_LANGUAGE}}"
decided_at: "{{YYYY-MM-DD}}"
---

# Итоговое архитектурное решение

## Рекомендация Council

- Recommendation: `{{COUNCIL_RECOMMENDATION}}`
- Design maturity: `{{DESIGN_MATURITY}}`
- Human review: `{{HUMAN_REVIEW_STATUS}}`
- Implementation start: `NOT_REQUESTED`

Рекомендация Council не является человеческим approval или разрешением менять
проект.

## Краткое решение

{{WHAT_WAS_DECIDED}}

## Соответствие бизнес-требованиям

| Бизнес-требование | Как решение его поддерживает | Evidence |
|---|---|---|
| {{BR_ID}} | {{RATIONALE}} | {{LINK}} |

## Выбранный вариант

- Option: {{OPTION_ID_AND_NAME}}
- Reasons: {{REASONS}}
- Solution Space Coverage Gate: `{{PASS|REWORK|BLOCKED|NOT_APPLICABLE_L1}}`
- Architecture Options: {{ARCHITECTURE_OPTIONS_LINK_OR_NOT_APPLICABLE}}
- Target architecture: [target-architecture.md](target-architecture.md)

## Отклонённые альтернативы

| Вариант | Причина отклонения | Условия пересмотра |
|---|---|---|
| {{OPTION}} | {{RATIONALE}} | {{TRIGGER_OR_NEVER}} |

## Судьба blocking findings

| Finding | Решение | Evidence/владелец |
|---|---|---|
| {{ID}} | {{CLOSED_ESCALATED_ACCEPTED_RISK}} | {{LINK_OR_OWNER}} |

## Условия

| ID | Условие | Владелец | Срок | Последствие невыполнения |
|---|---|---|---|---|
| COND-001 | {{CONDITION}} | {{OWNER}} | {{DATE_OR_STAGE}} | {{CONSEQUENCE}} |

## Остаточные риски

- {{RISK_ID_AND_SUMMARY}}

## Человеческое review

- Required: yes
- Approver: {{OWNER_OR_NA}}
- Reviewed revision: {{REVISION_OR_NA}}
- Decision: {{AWAITING_HUMAN_REVIEW/CHANGES_REQUESTED/APPROVED/REJECTED/ON_HOLD}}
- Date/evidence: {{DATE_AND_LINK}}

Существенная правка требований, evidence или архитектуры повышает revision и
возвращает статус в `AWAITING_HUMAN_REVIEW`.

## Что делать дальше

{{REVIEW_APPROVE_REQUEST_CHANGES_REJECT_HOLD_OR_EXPLICITLY_START_IMPLEMENTATION}}

Даже после `APPROVED` реализация начинается только по отдельной явной команде
пользователя. См. [Implementation Handoff](implementation-handoff.md).
