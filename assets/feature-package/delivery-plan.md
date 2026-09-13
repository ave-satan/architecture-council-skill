---
architecture_revision: "{{REVISION}}"
feature: "{{FEATURE_NAME}}"
artifact: delivery_evolution_and_verification_plan
status: "{{DRAFT|READY|IN_PROGRESS|COMPLETE}}"
owner: "{{OWNER}}"
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# Поставка и переход

{{SLICING_STRATEGY_AND_WHY}}

## Инкремент INC-001: {{NAME}}

| Поле | Значение |
|---|---|
| Наблюдаемый результат | {{USER_OR_SYSTEM_VISIBLE_CAPABILITY}} |
| Требования | {{REQ_IDS}} |
| Scope / контракты / данные | {{BOUNDED_SCOPE}} |
| Зависимости | {{INC_EXTERNAL_DECISION_OR_NONE}} |
| Приёмка | {{TESTABLE_CRITERIA}} |
| Проверка | {{VER_IDS_OR_LINKS}} |
| Владелец / статус | {{OWNER}} / {{PLANNED|READY|IN_PROGRESS|DONE|BLOCKED}} |

## Переход, rollout и rollback

| Этап | Изменение и совместимость | Gate / сигнал успеха | Rollback или cleanup |
|---|---|---|---|
| {{STAGE}} | {{CURRENT_TO_TARGET_CHANGE}} | {{CRITERION}} | {{ACTION_OR_POINT_OF_NO_RETURN}} |

- Миграция/backfill/reconciliation: {{PLAN_OR_NOT_APPLICABLE_WITH_REASON}}
- Временные механизмы и условие удаления: {{ITEMS_OR_NONE}}
- Репетиция перехода: {{REQUIRED_EVIDENCE_OR_NOT_APPLICABLE}}

## Зависимости и отложенная работа

| ID | Зависимость или элемент | Причина / mitigation | Владелец | Условие продолжения |
|---|---|---|---|---|
| {{ID}} | {{ITEM}} | {{RATIONALE}} | {{OWNER}} | {{TRIGGER}} |

## Проверка требований

<!-- AC:VERIFICATIONS -->
| Verification ID | Требование | Метод | Среда/этап | Данные/нагрузка | Критерий | Сигнал | Владелец |
|---|---|---|---|---|---|---|---|
| VER-001 | {{REQ_IDS}} | {{METHOD}} | {{ENVIRONMENT}} | {{DATA}} | {{CRITERION}} | {{SIG_ID_OR_NA}} | {{OWNER}} |

<!-- AC:SIGNALS -->
| Signal ID | Сигнал | Query/наблюдение | Ожидаемое | Alert/rollback | Владелец |
|---|---|---|---|---|---|
| SIG-001 | {{SIGNAL}} | {{QUERY_OR_METHOD}} | {{EXPECTED}} | {{THRESHOLD}} | {{OWNER}} |

- Evidence gaps / gate: {{MATERIAL_GAPS_AND_PASS_REWORK_OR_BLOCKED}}

План описывает будущую реализацию и не является командой её начать.
