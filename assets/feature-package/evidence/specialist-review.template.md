---
architecture_revision: "{{REVISION}}"
review_id: "{{ROLE_PREFIX}}-REVIEW-{{NNN}}"
run_id: "{{RUN_ID}}"
role: "{{ROLE}}"
subject: "{{ARTIFACT_AND_REVISION}}"
status: "{{NO_OBJECTION|CHANGES_REQUIRED|EVIDENCE_REQUIRED|BLOCKING_CONFLICT}}"
actor_id: "{{AGENT_OR_PERSON}}"
input_revision: "{{REVISION_OR_HASH}}"
incompatible_roles_confirmed: true
artifact_language: "{{USER_LANGUAGE}}"
reviewed_at: "{{YYYY-MM-DD}}"
---

# Review роли {{ROLE}}

## Scope

- Reviewed: {{SCOPE}}
- Excluded: {{EXCLUSIONS_AND_REASON}}

## Входы

- {{REQUIREMENT_DOCUMENT_CODE_METRIC_BENCHMARK}}

## Краткий вывод

{{CONCISE_VERDICT_AND_MAIN_REASON}}

## Findings

### {{PREFIX}}-001: {{TITLE}}

- Severity: `{{blocking|major|minor|note}}`
- Confidence: `{{high|medium|low}}`
- Type: `{{fact|inference|assumption|recommendation|unknown}}`
- Requirements: {{REQ_IDS}}
- Components: {{COMPONENTS}}
- Evidence: {{SOURCES_OR_MISSING}}

#### Проблема

{{CONCRETE_PROBLEM_OR_SCENARIO}}

#### Влияние

{{BUSINESS_TECHNICAL_OPERATIONAL_IMPACT}}

#### Обязательное или рекомендуемое изменение

{{CHANGE}}

#### Проверка закрытия

{{CLOSURE_CRITERION}}

## Предположения

| ID | Формулировка | Последствия ошибки | Требуемая проверка |
|---|---|---|---|
| {{ID}} | {{STATEMENT}} | {{IMPACT}} | {{ACTION}} |

## Открытые вопросы

- {{QUESTION_OR_NONE}}

## Предлагаемые решения

- {{DECISION_OR_NONE}}

## Повторное review

- Architecture response: {{LINK}}
- Reviewed revision: {{REVISION}}
- Finding statuses: {{CLOSED/OPEN/ESCALATED}}
- Final review status: `{{STATUS}}`
