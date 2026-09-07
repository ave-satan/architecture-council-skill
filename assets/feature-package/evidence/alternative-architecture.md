---
architecture_revision: "{{REVISION}}"
feature: "{{FEATURE_NAME}}"
artifact: alternative_architecture
run_id: "{{RUN_ID}}"
actor_id: "{{INDEPENDENT_ACTOR_ID}}"
input_revision: "{{REQUIREMENTS_AND_REVISION_OR_HASH}}"
status: "{{PLAUSIBLE_PENDING_FEASIBILITY|VIABLE|NOT_VIABLE}}"
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# Независимый архитектурный контрвариант

## Independence statement

- Candidate Architecture до завершения контрварианта не использовалась: {{yes/no}}
- Исполнитель не является Solution Architect, specialist, Red Team или Arbiter:
  {{yes/no}}
- Запись процесса: [Process Ledger](../process-ledger.md)

## Драйверы и ограничения

- {{REQUIREMENT_OR_CONSTRAINT}}

## Контрвариант

{{END_TO_END_DESCRIPTION}}

## Покрытие требований

| Requirement | Coverage | Evidence/assumption |
|---|---|---|
| {{REQ_ID}} | {{FULL/PARTIAL/NONE}} | {{LINK_OR_ASM_ID}} |

## Компромиссы

- Преимущества: {{ADVANTAGES}}
- Недостатки: {{DISADVANTAGES}}
- Стоимость и сложность: {{ASSESSMENT}}
- Эксплуатация: {{ASSESSMENT}}
- Обратимость: {{ASSESSMENT}}

## Feasibility

- Status: `{{PLAUSIBLE_PENDING_FEASIBILITY|VIABLE|NOT_VIABLE}}`
- No-go evidence: {{LINKS_OR_MISSING}}
- Риски: {{RISK_IDS}}
- Что требуется для честного сравнения: {{ACTION_OR_NONE}}
