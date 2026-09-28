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
| Область / контракты / данные | {{BOUNDED_SCOPE}} |
| Зависимости | {{INC_EXTERNAL_DECISION_OR_NONE}} |
| Приёмка | {{TESTABLE_CRITERIA}} |
| Проверка | {{VER_IDS_OR_LINKS}} |
| Владелец / статус | {{OWNER}} / {{PLANNED|READY|IN_PROGRESS|DONE|BLOCKED}} |

## Переход, выпуск и откат

| Этап | Изменение и совместимость | Критерий / сигнал успеха | Откат или очистка |
|---|---|---|---|
| {{STAGE}} | {{CURRENT_TO_TARGET_CHANGE}} | {{CRITERION}} | {{ACTION_OR_POINT_OF_NO_RETURN}} |

- Миграция/дозаполнение/сверка данных: {{PLAN_OR_NOT_APPLICABLE_WITH_REASON}}
- Временные механизмы и условие удаления: {{ITEMS_OR_NONE}}
- Репетиция перехода: {{REQUIRED_EVIDENCE_OR_NOT_APPLICABLE}}

## Зависимости и отложенная работа

| ID | Зависимость или элемент | Причина / меры снижения риска | Владелец | Условие продолжения |
|---|---|---|---|---|
| {{ID}} | {{ITEM}} | {{RATIONALE}} | {{OWNER}} | {{TRIGGER}} |

## Проверка требований

Один VER может покрывать несколько требований и этапов. Используй применимые
существующие результаты; добавляй случаи для непокрытого поведения и значимых
различий условий. Подтверждённые исходные факты остаются ссылками на источники.

<!-- AC:VERIFICATIONS -->
| ID проверки | Требование | Метод | Среда/этап | Данные/нагрузка | Критерий | Сигнал | Владелец |
|---|---|---|---|---|---|---|---|
| VER-001 | {{REQ_IDS}} | {{METHOD}} | {{ENVIRONMENT}} | {{DATA}} | {{CRITERION}} | {{SIG_ID_OR_NA}} | {{OWNER}} |

<!-- AC:SIGNALS -->
| ID сигнала | Сигнал | Запрос/наблюдение | Ожидаемое | Оповещение/откат | Владелец |
|---|---|---|---|---|---|
| SIG-001 | {{SIGNAL}} | {{QUERY_OR_METHOD}} | {{EXPECTED}} | {{THRESHOLD}} | {{OWNER}} |

- Недостающие основания / итог: {{MATERIAL_GAPS_AND_PASS_REWORK_OR_BLOCKED}}

План описывает будущую реализацию и не является командой её начать.
