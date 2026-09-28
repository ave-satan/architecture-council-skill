---
feature: "{{FEATURE_NAME}}"
artifact: council_review
architecture_revision: "{{REVISION}}"
selected_roles: ["{{ROLE_ID}}"]
council_recommendation: "{{ACCEPTED|ACCEPTED_WITH_CONDITIONS|REWORK_REQUIRED|REJECTED|BLOCKED|ESCALATED}}"
solution_space_coverage: "{{PASS|REWORK|BLOCKED|NOT_APPLICABLE_L1}}"
missed_solution_family_status: "{{NONE|REWORKED|OPEN|NOT_APPLICABLE_L1}}"
coverage_challenger_run_id: "{{RUN_ID_OR_NA}}"
coverage_challenger_actor_id: "{{ACTOR_ID_OR_NA}}"
coverage_input_revision: "{{INPUT_REVISION_OR_NA}}"
package_validation_status: "{{PASS|FAIL|WARNINGS}}"
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# Council Review

Этот файл объединяет независимые заключения, результаты этапов и структурную проверку. Разные
секции сохраняют своих авторов и входы; общий файл не означает общего автора.

Для каждого запуска используй отдельную непустую секцию с его Run ID в заголовке;
табличная ссылка ведёт именно к этой секции. Автора и входы повторять в ней не нужно.

## Запуски ролей

<!-- AC:ROLE_RUNS -->
| Run ID | Этап | Роль | Actor ID | Входная ревизия/hash | Вывод | Результат этапа | Начало | Завершение |
|---|---|---|---|---|---|---|---|---|
| RUN-001 | {{STAGE}} | {{ROLE_ID}} | {{ACTOR_ID}} | {{REVISION_OR_HASH}} | [Секция](#run-001) | {{STATUS}} | {{ISO_TIME}} | {{ISO_TIME}} |

<a id="run-001"></a>
### RUN-001 — {{ROLE}}

{{INDEPENDENT_CONCLUSION_WITH_MATERIAL_FINDINGS_EVIDENCE_AND_CLOSURE_ONLY}}

## Пространство решений <!-- SSC:MAP -->

| Ось | Почему релевантна | Механизмы | Требования |
|---|---|---|---|
| {{AXIS_OR_NA_L1}} | {{RATIONALE}} | {{MECHANISMS}} | {{REQ_IDS}} |

<!-- SSC:FAMILIES -->
| ID семейства | Семейство/механизм | Источник | Требования | Неизвестные | Статус |
|---|---|---|---|---|---|
| SF-001 | {{FAMILY}} | {{SOURCE}} | {{REQ_IDS}} | {{UNKNOWN_OR_NONE}} | {{CANDIDATE_FAMILY|EXCLUDED_WITH_EVIDENCE|OUT_OF_SCOPE_BY_REQUIREMENT}} |

## Независимая проверка пространства решений <!-- SSC:CHALLENGE -->

{{CHALLENGER_RUN_ACTOR_INPUT_FINDINGS_AND_RESOLUTION_OR_NOT_APPLICABLE_L1}}

## Полнота пространства решений <!-- SSC:GATE -->

{{COVERAGE_AND_MISSED_FAMILY_STATUS_WITH_BASIS}}

<!-- AC:OPTIONS -->
| ID варианта | Описание/ссылка | Жизнеспособность |
|---|---|---|
| OPT-001 | {{DESCRIPTION_OR_LINK}} | {{VIABLE|PLAUSIBLE_PENDING_FEASIBILITY|NOT_VIABLE}} |

## Согласованные отступления

<!-- AC:WAIVERS -->
| ID отступления | Actor ID | Роли | Ревизия | Кто разрешил | Дата разрешения | Источник |
|---|---|---|---|---|---|---|

## Дополнительные основания

Для L3 и жёстких триггеров добавь только применимые строки; ссылки допустимы, когда
сырой результат действительно нуждается в отдельном файле.

| Область | Модель/процедура | Результат и остаточный риск | Владелец / основания | Итог |
|---|---|---|---|---|
| {{THREAT_MODEL_OR_MIGRATION_REHEARSAL_OR_RISK_ACCEPTANCE}} | {{METHOD}} | {{RESULT}} | {{OWNER_AND_LINK_OR_INLINE}} | {{PASS|REWORK|BLOCKED|NOT_APPLICABLE}} |

## Проверка пакета

<!-- AC:PACKAGE_VALIDATION -->
| Снимок / команда | Ошибки | Незакрытые условия | Предупреждения / ручные границы | Статус |
|---|---:|---:|---|---|
| {{REVISION_AND_COMMAND}} | {{COUNT}} | {{COUNT}} | {{DETAILS_OR_NONE}} | {{PASS|FAIL|WARNINGS}} |

Оставь одну актуальную строку. Для PASS первая ячейка содержит текущую ревизию
(например, `r1; python ...`), ошибки и незакрытые условия равны `0`, статус — `PASS`.
Все пять ячеек заполнены; отсутствие предупреждений обозначается `—`.

Структурный PASS не доказывает истинность оснований или разрешение реализации.
