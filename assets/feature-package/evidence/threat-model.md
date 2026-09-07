---
architecture_revision: "{{REVISION}}"
feature: "{{FEATURE_NAME}}"
artifact: threat_model
status: "{{DRAFT|REVIEWED|ACCEPTED|NOT_APPLICABLE}}"
owner: security_privacy
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# Модель угроз

## Scope и активы

- Protected assets: {{DATA_MONEY_IDENTITY_AVAILABILITY}}
- In scope: {{COMPONENTS_FLOWS}}
- Out of scope: {{EXCLUSIONS_AND_OWNER}}

## Акторы и trust boundaries

{{DESCRIPTION_AND_LINK_TO_TRUST_BOUNDARY_DIAGRAM}}

## Точки входа и потоки данных

| Точка входа/поток | Аутентификация | Авторизация | Чувствительные данные |
|---|---|---|---|
| {{ENTRY}} | {{MECHANISM}} | {{POLICY}} | {{DATA}} |

## Угрозы

| ID | Угроза/abuse case | Условия | Влияние | Текущая защита | Требуемая защита | Проверка | Статус |
|---|---|---|---|---|---|---|---|
| THR-001 | {{THREAT}} | {{PRECONDITIONS}} | {{IMPACT}} | {{CONTROL}} | {{CONTROL}} | {{VER_ID}} | {{STATUS}} |

## Остаточные риски

- {{RISK_ID_FROM_RISKS_AND_ASSUMPTIONS_OR_NONE}}

Используй только нормативные `RISK-NNN` из
[Risks and Assumptions](../risks-and-assumptions.md); локальные сокращения и
переопределение risk ID запрещены.

## Решение Security reviewer

- Status: {{NO_OBJECTION|CHANGES_REQUIRED|BLOCKING_CONFLICT}}
- Reviewer: {{OWNER}}
- Evidence: {{LINKS}}
