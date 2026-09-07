---
architecture_revision: "{{REVISION}}"
feature: "{{FEATURE_NAME}}"
artifact: arbiter_review
run_id: "{{RUN_ID}}"
actor_id: "{{INDEPENDENT_ARBITER_ID}}"
input_revision: "{{ARCHITECTURE_REVISION_OR_HASH}}"
council_recommendation: "{{ACCEPTED|ACCEPTED_WITH_CONDITIONS|REWORK_REQUIRED|REJECTED|BLOCKED|ESCALATED}}"
artifact_language: "{{USER_LANGUAGE}}"
reviewed_at: "{{YYYY-MM-DD}}"
---

# Независимое заключение Arbiter

## Проверка независимости

- Не автор архитектуры: {{yes/no}}
- Не Solution Space Challenger: {{yes/no}}
- Не Alternative Architect: {{yes/no}}
- Не specialist reviewer: {{yes/no}}
- Не Red Team: {{yes/no}}
- Запись процесса: [Process Ledger](../process-ledger.md)

## Проверенные входы

- {{NORMATIVE_ARTIFACT_AND_REVISION}}

## Solution Space Coverage

- Architecture Options revision: {{REVISION_AND_LINK}}
- Coverage gate: `{{PASS|REWORK|BLOCKED|NOT_APPLICABLE_L1}}`
- Independent challenger run: {{RUN_ID}}
- Открытые `MISSED_SOLUTION_FAMILY`: {{NONE_OR_SF_IDS}}

Рекомендация `ACCEPTED*` недопустима, если coverage gate не `PASS` для L2–L3. Для L1
используй `NOT_APPLICABLE_L1` и оцени обоснование решения в Target Architecture.

## Соответствие бизнес-требованиям

| Бизнес-требование | Покрытие | Решение/evidence | Вердикт |
|---|---|---|---|
| {{BR_ID}} | {{DESCRIPTION}} | {{LINKS}} | {{PASS/FAIL/CONDITIONAL}} |

## Blocking findings и условия

| ID | Решение | Владелец | Evidence/срок |
|---|---|---|---|
| {{ID}} | {{CLOSED_ESCALATED_ACCEPTED_RISK_OPEN}} | {{OWNER}} | {{LINK_OR_DATE}} |

## Рекомендация Council

- Рекомендация: `{{RECOMMENDATION}}`
- Зрелость дизайна: `{{DESIGN_CANDIDATE|EVIDENCE_AUTHORIZED|IMPLEMENTATION_READY|NOT_READY}}`
- Обоснование: {{RATIONALE}}
- Человеческое review обязательно: yes
- Реализация авторизована: no
