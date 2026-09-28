---
feature: "{{FEATURE_NAME}}"
artifact: formal_risk_acceptance
risk_id: "{{RISK_ID}}"
status: "{{PROPOSED|ACCEPTED|REJECTED|EXPIRED|NOT_REQUIRED}}"
architecture_revision: "{{REVISION}}"
artifact_language: "{{USER_LANGUAGE}}"
accepted_at: "{{YYYY-MM-DD}}"
---

# Формальное принятие риска: {{RISK_ID}}

## Риск

{{PRECISE_RISK_AND_FAILURE_SCENARIO}}

## Экспозиция

- Вероятность: {{ASSESSMENT_AND_BASIS}}
- Влияние: {{ASSESSMENT_AND_BASIS}}
- Затронутые пользователи/данные/бизнес: {{SCOPE}}

## Почему риск не устраняется сейчас

{{RATIONALE_COST_TIMELINE_OR_TECHNICAL_LIMIT}}

## Существующие меры и обнаружение

- Меры снижения риска: {{CONTROL}}
- Обнаружение: {{METRIC_ALERT_AUDIT}}
- Восстановление: {{RUNBOOK_OR_ACTION}}

## Решение о принятии

- Уполномоченный владелец: {{NAME_ROLE}}
- Условия: {{CONDITIONS}}
- Действует до/условие пересмотра: {{DATE_OR_TRIGGER}}
- Решение: `{{ACCEPTED|REJECTED}}`
- Источник решения: {{LINK}}

При `NOT_REQUIRED` укажи причину и ссылку на реестр рисков, подтверждающую, что
для текущей ревизии нет риска, требующего формального принятия.
