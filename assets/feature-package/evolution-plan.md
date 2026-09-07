---
architecture_revision: "{{REVISION}}"
feature: "{{FEATURE_NAME}}"
artifact: evolution_plan
status: "{{DRAFT|CANDIDATE|ACCEPTED}}"
owner: "{{SOLUTION_OR_EVOLUTION_ARCHITECT}}"
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# План эволюции

## Изменения current-to-target

| Область | Current | Target | Требуемое изменение | Владелец |
|---|---|---|---|---|
| {{AREA}} | {{CURRENT}} | {{TARGET}} | {{CHANGE}} | {{OWNER}} |

## Матрица совместимости

| Поверхность | Производитель/владелец | Потребители | Требование совместимости | Стратегия |
|---|---|---|---|---|
| {{API_EVENT_SCHEMA_CLIENT}} | {{OWNER}} | {{CONSUMERS}} | {{TR_OR_CON_ID}} | {{STRATEGY}} |

## Переходные состояния

### T0 — Current

- Активное поведение: {{DESCRIPTION}}
- Форма данных: {{DESCRIPTION}}

### T1 — Prepared

- Изменения развёрнуты, но неактивны: {{DESCRIPTION}}
- Forward/backward compatibility: {{DESCRIPTION}}
- Критерий входа: {{CRITERION}}
- Критерий выхода: {{CRITERION}}

### T2 — Coexistence/canary

- Старое поведение: {{DESCRIPTION}}
- Новое поведение: {{DESCRIPTION}}
- Выбор трафика/feature flag: {{DESCRIPTION}}
- Критерий входа: {{CRITERION}}
- Критерий продвижения: {{METRIC_AND_THRESHOLD}}
- Rollback trigger: {{TRIGGER}}

### T3 — Target

- Активное поведение: {{DESCRIPTION}}
- Статус legacy path: {{DESCRIPTION}}

### T4 — Cleanup

- Временные механизмы удалены: {{ITEMS}}
- Критерий удаления: {{CRITERION}}

## Миграция данных и backfill

- Изменения схемы: {{DESCRIPTION_OR_NONE}}
- Порядок миграции: {{STEPS}}
- Backfill: {{DESCRIPTION_OR_NONE}}
- Dual read/write: {{DESCRIPTION_OR_NONE}}
- Валидация/reconciliation: {{DESCRIPTION}}
- Восстановление после отказа: {{DESCRIPTION}}

## План rollout

| Этап | Scope | Входной gate | Окно наблюдения | Успех | Rollback trigger |
|---|---|---|---|---|---|
| {{STAGE}} | {{PERCENT_USERS_REGION}} | {{GATE}} | {{WINDOW}} | {{CRITERIA}} | {{TRIGGER}} |

## Rollback

- Безопасен до: {{POINT_OF_NO_RETURN_OR_ALWAYS}}
- Шаги: {{ORDERED_STEPS}}
- Обработка данных: {{DESCRIPTION}}
- Работа в процессе: {{DESCRIPTION}}
- Требуемое человеческое approval: {{YES_NO_AND_OWNER}}

## Временные механизмы

| Механизм | Зачем нужен | Владелец | Условие удаления | Tracking item |
|---|---|---|---|---|
| {{FLAG_ADAPTER_DUAL_WRITE}} | {{RATIONALE}} | {{OWNER}} | {{CONDITION}} | {{LINK}} |

## Репетиция миграции

- Обязательна: {{yes/no}}
- Среда/форма данных: {{DESCRIPTION}}
- Evidence: {{LINK}}
- Результат: {{STATUS}}

## Evolution gate

- Промежуточные состояния корректны: {{yes/no}}
- Совместимость доказана: {{yes/no}}
- Rollout измерим: {{yes/no}}
- Rollback выполним или необратимость принята: {{yes/no/link}}
- Для временных механизмов определены условия удаления: {{yes/no}}

## Переход (при необходимости)

```mermaid
%% ac_id: evolution
%% ac_state: transition
%% ac_purpose: показать безопасный переход current-to-target
%% ac_scope: {{SCOPE}}
%% ac_legend: сплошная стрелка — продвижение, пунктирная — rollback
%% ac_revision: {{REVISION}}
%% ac_normative: evolution-plan.md
flowchart LR
    T0[T0 Current]
    T1[T1 Prepared]
    T2[T2 Coexistence / Canary]
    T3[T3 Target]
    T4[T4 Cleanup]

    T0 -->|{{ENTRY_GATE}}| T1
    T1 -->|{{ENABLEMENT_GATE}}| T2
    T2 -->|{{PROMOTION_GATE}}| T3
    T3 -->|{{RETIREMENT_GATE}}| T4
    T2 -.->|{{ROLLBACK_TRIGGER}}| T1
```
