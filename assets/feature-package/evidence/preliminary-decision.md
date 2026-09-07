---
architecture_revision: "{{REVISION}}"
feature: "{{FEATURE_NAME}}"
artifact: preliminary_decision
run_id: "{{RUN_ID}}"
actor_id: "{{INDEPENDENT_ARBITER_ID}}"
input_revision: "{{OPTIONS_REVISION_OR_HASH}}"
status: "{{CANDIDATE_SELECTED|EVIDENCE_REQUIRED|REWORK|BLOCKED|SUPERSEDED}}"
solution_space_coverage: "{{PASS|REWORK|BLOCKED}}"
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# Предварительный выбор варианта

## Проверка независимости

- Arbiter не создавал варианты и не выполнял specialist review: {{yes/no}}
- Запись процесса: [Process Ledger](../process-ledger.md)

## Проверка ширины выбора

- Architecture Options: [карта и варианты](architecture-options.md)
- Solution Space Coverage Gate: `{{PASS|REWORK|BLOCKED}}`
- Challenger run: {{RUN_ID}}
- Открытые `MISSED_SOLUTION_FAMILY`: {{NONE_OR_SF_IDS}}

Arbiter не выбирает кандидата, пока coverage gate не имеет `PASS`.

## Варианты, допущенные к сравнению

| Вариант | Feasibility status | Обязательные отклонения | Evidence gaps |
|---|---|---|---|
| {{OPTION}} | {{STATUS}} | {{NONE_OR_REQ_IDS}} | {{LINKS_OR_NONE}} |

## Предварительное решение

- Selected candidate: {{OPTION_OR_NONE}}
- Status: `{{CANDIDATE_SELECTED|EVIDENCE_REQUIRED|REWORK|BLOCKED|SUPERSEDED}}`
- Business rationale: {{RATIONALE}}
- Отклонённые варианты: {{OPTIONS_AND_REASONS}}

## Обязательные изменения до Final Arbitration

| ID | Изменение/evidence | Владелец | Gate |
|---|---|---|---|
| {{ID}} | {{ACTION}} | {{OWNER}} | {{STAGE}} |

## Недопустимые риски

- {{RISK_ID_OR_NONE}}
