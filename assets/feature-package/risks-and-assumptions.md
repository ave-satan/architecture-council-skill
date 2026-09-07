---
architecture_revision: "{{REVISION}}"
feature: "{{FEATURE_NAME}}"
artifact: risks_and_assumptions
owner: "{{OWNER}}"
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# Риски и предположения

## Реестр рисков

| ID | Риск | Вероятность | Влияние | Экспозиция | Mitigation | Владелец | Trigger | Статус |
|---|---|---|---|---|---|---|---|---|
| RISK-001 | {{RISK}} | {{low/medium/high}} | {{low/medium/high/critical}} | {{SUMMARY}} | {{MITIGATION}} | {{OWNER}} | {{SIGNAL}} | {{OPEN/MITIGATED/ACCEPTED/CLOSED}} |

## Принятые риски

| ID | Риск | Кто принял | Обоснование | Условия | Дата review |
|---|---|---|---|---|---|
| RISK-001 | {{RISK}} | {{AUTHORIZED_OWNER}} | {{RATIONALE}} | {{CONDITIONS}} | {{DATE}} |

## Предположения

| ID | Формулировка | Основание | Последствия ошибки | Владелец | Проверить до | Evidence | Статус |
|---|---|---|---|---|---|---|---|
| ASM-001 | {{STATEMENT}} | {{BASIS}} | {{IMPACT}} | {{OWNER}} | {{DATE_OR_STAGE}} | {{LINK_OR_NONE}} | {{OPEN/VALIDATED/INVALIDATED}} |

## Условия принятия

| ID | Условие | Решение-источник | Владелец | Срок | Evidence выполнения | Статус |
|---|---|---|---|---|---|---|
| COND-001 | {{CONDITION}} | {{FINAL_DECISION_OR_ADR}} | {{OWNER}} | {{DATE_OR_STAGE}} | {{LINK_OR_NONE}} | {{OPEN/DONE/BREACHED}} |

## Условия пересмотра

- {{LOAD_COST_INCIDENT_DATE_REQUIREMENT_CHANGE_TRIGGER}}
