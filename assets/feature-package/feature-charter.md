---
architecture_revision: "{{REVISION}}"
feature: "{{FEATURE_NAME}}"
stage: intake
readiness: "{{DRAFT|READY|READY_WITH_ASSUMPTIONS|BLOCKED}}"
owner: "{{OWNER}}"
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# Устав фичи

## Проблема

{{WHO_HAS_WHAT_PROBLEM_AND_WHY_IT_MATTERS}}

## Доказательства проблемы

- {{USER_FEEDBACK_METRIC_INCIDENT_OR_SOURCE}}

## Пользователи и участники

| Участник | Потребность | Текущая проблема |
|---|---|---|
| {{ACTOR}} | {{NEED}} | {{PAIN}} |

## Бизнес-результат

{{DESIRED_OBSERVABLE_RESULT}}

## Метрики успеха

| Метрика | Базовый уровень | Цель | Окно измерения | Владелец |
|---|---:|---:|---|---|
| {{METRIC}} | {{BASELINE_OR_UNKNOWN}} | {{TARGET}} | {{WINDOW}} | {{OWNER}} |

## Основные сценарии

### Сценарий SCN-001: {{NAME}}

1. {{STEP}}
2. {{STEP}}
3. {{OBSERVABLE_OUTCOME}}

## Scope

### Включено

- {{ITEM}}

### Исключено

- {{ITEM_AND_REASON}}

## Бизнес-правила и инварианты

- {{RULE_OR_LINK_TO_REQUIREMENT}}

## Ограничения и предположения о решении

| Формулировка / источник | Тип: факт, ограничение, предпочтение, гипотеза | Защищаемая потребность и область действия | Подтверждено / открытая трактовка |
|---|---|---|---|
| {{STATEMENT_AND_SOURCE_LINK}} | {{TYPE}} | {{NEED_AND_SCOPE}} | {{CONFIRMATION_OR_CONDITIONAL_INTERPRETATIONS}} |

Уточняй только существенную неоднозначность. Предложенный механизм не становится
обязательным без основания; подтверждённые требования сохраняются.


## Известные ожидания качества

| Категория | Ожидание | Статус |
|---|---|---|
| Performance | {{EXPECTATION_OR_UNKNOWN}} | {{stated/proposed/unknown}} |
| Reliability | {{EXPECTATION_OR_UNKNOWN}} | {{stated/proposed/unknown}} |
| Security | {{EXPECTATION_OR_UNKNOWN}} | {{stated/proposed/unknown}} |
| Availability | {{EXPECTATION_OR_UNKNOWN}} | {{stated/proposed/unknown}} |

## Предположения

| ID | Формулировка | Основание | Последствия ошибки | Владелец | Проверить до |
|---|---|---|---|---|---|
| ASM-001 | {{STATEMENT}} | {{BASIS}} | {{IMPACT}} | {{OWNER}} | {{DATE_OR_STAGE}} |

## Открытые вопросы

| ID | Тип | Вопрос | Влияние | Владелец | Статус |
|---|---|---|---|---|---|
| Q-001 | {{discoverable/assumable/blocking}} | {{QUESTION}} | {{IMPACT}} | {{OWNER}} | {{STATUS}} |

## Раунды уточнений

| Раунд | Дата | Вопросы | Решения | Новые вопросы |
|---|---|---|---|---|
| 1 | {{DATE}} | {{LINK_OR_IDS}} | {{LINK_OR_IDS}} | {{IDS_OR_NONE}} |

## Решение о готовности

`READY` допустим только при определённых обязательных outcomes и success
targets. Для обратимых non-blocking `TBD` используй `READY_WITH_ASSUMPTIONS` и
укажи владельца, срок и влияние.

- Status: `{{READY|READY_WITH_ASSUMPTIONS|BLOCKED}}`
- Rationale: {{RATIONALE}}
- Blocking scope: {{NONE_OR_SCOPE}}
- Unresolved success targets: {{NONE_OR_IDS_WITH_OWNER_AND_DUE}}
- Next stage: {{STAGE}}
