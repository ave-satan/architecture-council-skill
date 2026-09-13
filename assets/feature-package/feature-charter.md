---
architecture_revision: "{{REVISION}}"
feature: "{{FEATURE_NAME}}"
stage: intake
readiness: "{{DRAFT|READY|READY_WITH_ASSUMPTIONS|BLOCKED}}"
level: "{{L0|L1|L2|L3}}"
context: "{{greenfield|brownfield}}"
selected_roles: ["{{ROLE_ID}}"]
classification_basis_sha256: "{{RECORD_AFTER_CLASSIFICATION_REVIEW}}"
owner: "{{OWNER}}"
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# Устав фичи

<!-- AC:CLASSIFICATION -->
| Level / context | Основание и hard triggers | Выбранные роли | Дополнительные evidence | Gate |
|---|---|---|---|---|
| {{LEVEL}} / {{CONTEXT}} | {{RATIONALE_AND_TRIGGERS}} | {{ROLE_IDS}} | {{EVIDENCE_OR_NONE}} | {{PASS|REWORK|BLOCKED}} |

## Задача и результат

- Проблема / источник: {{PROBLEM_AND_EVIDENCE}}
- Пользователи: {{ACTORS_AND_NEEDS}}
- Наблюдаемый бизнес-результат: {{OUTCOME}}
- Метрика / цель / окно / владелец: {{SUCCESS_TARGET}}

## Сценарий SCN-001: {{NAME}}

{{TRIGGER_STEPS_AND_OBSERVABLE_OUTCOME}}

## Scope

| Включено | Исключено и почему |
|---|---|
| {{IN_SCOPE}} | {{OUT_OF_SCOPE_AND_REASON}} |

## Входные ограничения

| Формулировка / источник | Факт, ограничение, предпочтение или гипотеза | Защищаемая потребность / область | Статус или трактовки |
|---|---|---|---|
| {{STATEMENT_AND_SOURCE}} | {{TYPE}} | {{NEED_AND_SCOPE}} | {{CONFIRMED_OR_OPEN}} |

Требования, ожидания качества, риски и допущения ведутся в
[requirements.md](requirements.md), а не повторяются здесь.

## Открытые вопросы и готовность

| ID | Вопрос / влияние | Владелец / срок | Статус |
|---|---|---|---|
| Q-001 | {{QUESTION_AND_IMPACT}} | {{OWNER_AND_DUE}} | {{OPEN|ASSUMED|CLOSED|BLOCKING}} |

- Readiness / blocking scope: `{{READY|READY_WITH_ASSUMPTIONS|BLOCKED}}` / {{SCOPE_OR_NONE}}
- Следующая стадия: {{STAGE}}
