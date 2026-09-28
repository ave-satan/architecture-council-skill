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

## Область анализа и активы

- Защищаемые активы: {{DATA_MONEY_IDENTITY_AVAILABILITY}}
- В области анализа: {{COMPONENTS_FLOWS}}
- Вне области анализа: {{EXCLUSIONS_AND_OWNER}}

## Акторы и границы доверия

{{DESCRIPTION_AND_LINK_TO_TRUST_BOUNDARY_DIAGRAM}}

## Точки входа и потоки данных

| Точка входа/поток | Аутентификация | Авторизация | Чувствительные данные |
|---|---|---|---|
| {{ENTRY}} | {{MECHANISM}} | {{POLICY}} | {{DATA}} |

## Угрозы

| ID | Угроза/злоупотребление | Условия | Влияние | Текущая защита | Требуемая защита | Проверка | Статус |
|---|---|---|---|---|---|---|---|
| THR-001 | {{THREAT}} | {{PRECONDITIONS}} | {{IMPACT}} | {{CONTROL}} | {{CONTROL}} | {{VER_ID}} | {{STATUS}} |

## Остаточные риски

- {{RISK_ID_FROM_RISKS_AND_ASSUMPTIONS_OR_NONE}}

Используй только нормативные `RISK-NNN` из
[требований: риски и допущения](../requirements.md); локальные сокращения и
переопределение ID риска запрещены.

## Решение специалиста по безопасности

- Статус: {{NO_OBJECTION|CHANGES_REQUIRED|BLOCKING_CONFLICT}}
- Рецензент: {{OWNER}}
- Основания: {{LINKS}}
