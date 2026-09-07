---
architecture_revision: "{{REVISION}}"
conflict_id: "CONFLICT-{{NNN}}"
subject: "{{SUBJECT}}"
type: "{{FACT|REQUIREMENT|ARCHITECTURE_TRADEOFF|RISK_ACCEPTANCE|OWNERSHIP}}"
status: "{{OPEN|EVIDENCE_PENDING|ESCALATED|RESOLVED|ACCEPTED_RISK}}"
owner: "{{ARBITER_OR_DECISION_OWNER}}"
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# CONFLICT-{{NNN}}: {{SUBJECT}}

## Почему это важно

{{BUSINESS_AND_ARCHITECTURAL_IMPACT}}

## Позиции

### {{PARTICIPANT_A}}

- Позиция: {{POSITION}}
- Требования: {{REQ_IDS}}
- Предположения: {{ASM_IDS_OR_STATEMENTS}}
- Evidence: {{SOURCES}}
- Последствия отклонения: {{CONSEQUENCES}}

### {{PARTICIPANT_B}}

- Позиция: {{POSITION}}
- Требования: {{REQ_IDS}}
- Предположения: {{ASM_IDS_OR_STATEMENTS}}
- Evidence: {{SOURCES}}
- Последствия отклонения: {{CONSEQUENCES}}

## Спорные пункты

- {{FACT_REQUIREMENT_PRIORITY_RISK_OR_BOUNDARY}}

## Путь разрешения

- Тип конфликта: `{{TYPE}}`
- Требуемое evidence/решение: {{ACTION}}
- Владелец: {{OWNER}}
- Срок: {{DATE_OR_STAGE}}

## Адресный раунд

- Новое evidence: {{LINK_OR_NONE}}
- Ответ позиции A: {{SUMMARY}}
- Ответ позиции B: {{SUMMARY}}
- Консенсус: {{yes/no}}

## Решение

- Статус: `{{STATUS}}`
- Решение: {{DECISION}}
- Обоснование: {{RATIONALE}}
- Условия: {{CONDITIONS_OR_NONE}}
- Принятый риск: {{RISK_ID_OR_NONE}}
- Владелец решения: {{OWNER}}
- Связанный ADR: {{LINK_OR_NONE}}
