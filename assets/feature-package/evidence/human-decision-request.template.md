---
architecture_revision: "{{REVISION}}"
decision_id: "HD-{{NNN}}"
status: "{{OPEN|DECIDED|SUPERSEDED}}"
required_owner: "{{PRODUCT|RISK|LEGAL|PLATFORM|OTHER_OWNER}}"
blocking_scope: "{{LOCAL_SCOPE|GLOBAL}}"
solution_space_gate: "{{PASS|NOT_APPLICABLE_L1|NOT_APPLICABLE_REQUIREMENT_CLARIFICATION}}"
options_revision: "{{REVISION_OR_NOT_APPLICABLE}}"
artifact_language: "{{USER_LANGUAGE}}"
requested_at: "{{YYYY-MM-DD}}"
---

# Требуется человеческое решение: HD-{{NNN}}

## Требуется одно решение

{{ONE_CONCRETE_QUESTION}}

Один Human Decision Request не объединяет финансовое, продуктовое, retention,
legal или risk-решения, если у них разные владельцы или возможные ответы.

## Почему агенты не могут решить вопрос

{{BUSINESS_RISK_LEGAL_IRREVERSIBLE_OR_EXTERNAL_AUTHORITY_REASON}}

## Проверка полноты выбора

- Тип запроса: {{ARCHITECTURE_CHOICE|REQUIREMENT_CLARIFICATION|AUTHORITY_DECISION}}
- Architecture Options: {{LINK_OR_NOT_APPLICABLE}}
- Solution Space Coverage Gate: `{{PASS|NOT_APPLICABLE_L1|NOT_APPLICABLE_REQUIREMENT_CLARIFICATION}}`
- Рассмотренные семейства: {{SF_IDS_OR_NOT_APPLICABLE}}
- Доказательно исключённые семейства: {{SF_IDS_AND_LINKS_OR_NONE}}

Для выбора архитектурного механизма в L2–L3 обязателен `PASS`. В L1 допустим
`NOT_APPLICABLE_L1` с кратким обоснованием сравнения. Раннее уточнение
требования или полномочия явно маркируется `NOT_APPLICABLE_REQUIREMENT_CLARIFICATION`
и не выдаётся за полный набор технических вариантов.

## Вариант A: {{NAME}}

- Consequences: {{CONSEQUENCES}}
- Risks: {{RISKS}}
- Cost/timeline: {{IMPACT}}

## Вариант B: {{NAME}}

- Consequences: {{CONSEQUENCES}}
- Risks: {{RISKS}}
- Cost/timeline: {{IMPACT}}

## Рекомендация Council

- Recommended option: {{OPTION}}
- Rationale: {{RATIONALE}}
- Confidence: {{high/medium/low}}

## Заблокированный scope

- Blocked: {{WORK}}
- Can continue: {{WORK_OR_NONE}}

## Решение

- Selected option: {{OPTION}}
- Decided by: {{AUTHORIZED_OWNER}}
- Date: {{YYYY-MM-DD}}
- Conditions: {{CONDITIONS_OR_NONE}}
- Normative update: {{REQUIREMENT_ADR_CONSTRAINT_SCOPE_OR_RISK_LINK}}
