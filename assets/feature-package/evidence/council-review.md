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

Этот файл объединяет независимые outputs, gates и структурную проверку. Разные
секции сохраняют своих авторов и входы; общий файл не означает общего автора.

## Запуски ролей

<!-- AC:ROLE_RUNS -->
| Run ID | Stage | Role | Actor ID | Input revision/hash | Output | Gate result | Started | Completed |
|---|---|---|---|---|---|---|---|---|
| RUN-001 | {{STAGE}} | {{ROLE_ID}} | {{ACTOR_ID}} | {{REVISION_OR_HASH}} | [Секция](#run-001) | {{STATUS}} | {{ISO_TIME}} | {{ISO_TIME}} |

<!-- AC:ROLE_COVERAGE -->
| Выбранная роль | Output | Findings | Ответ refinement | Re-review | Статус |
|---|---|---|---|---|---|
| {{ROLE_ID}} | [Секция](#run-001) | {{IDS_OR_NONE}} | {{LINK_OR_NA}} | {{LINK_OR_NA}} | {{COMPLETE|MISSING}} |

<!-- AC:REVIEWS -->
| Run ID | Role | Actor ID | Input revision/hash | Verdict | Findings / response | Section |
|---|---|---|---|---|---|---|
| RUN-001 | {{ROLE_ID}} | {{ACTOR_ID}} | {{REVISION_OR_HASH}} | {{PASS|REWORK|BLOCKED}} | {{CONCISE_FINDINGS_AND_RESPONSE}} | [RUN-001](#run-001) |

<a id="run-001"></a>
### RUN-001 — {{ROLE}}

{{INDEPENDENT_CONCLUSION_WITH_MATERIAL_FINDINGS_EVIDENCE_AND_CLOSURE_ONLY}}

## Пространство решений <!-- SSC:MAP -->

| Ось | Почему релевантна | Механизмы | Требования |
|---|---|---|---|
| {{AXIS_OR_NA_L1}} | {{RATIONALE}} | {{MECHANISMS}} | {{REQ_IDS}} |

<!-- SSC:FAMILIES -->
| Family ID | Семейство/механизм | Источник | Требования | Неизвестные | Статус |
|---|---|---|---|---|---|
| SF-001 | {{FAMILY}} | {{SOURCE}} | {{REQ_IDS}} | {{UNKNOWN_OR_NONE}} | {{CANDIDATE_FAMILY|EXCLUDED_WITH_EVIDENCE|OUT_OF_SCOPE_BY_REQUIREMENT}} |

## Независимый challenge <!-- SSC:CHALLENGE -->

{{CHALLENGER_RUN_ACTOR_INPUT_FINDINGS_AND_RESOLUTION_OR_NOT_APPLICABLE_L1}}

## Coverage gate <!-- SSC:GATE -->

{{COVERAGE_AND_MISSED_FAMILY_STATUS_WITH_BASIS}}

<!-- AC:OPTIONS -->
| Option ID | Описание/ссылка | Feasibility |
|---|---|---|
| OPT-001 | {{DESCRIPTION_OR_LINK}} | {{VIABLE|PLAUSIBLE_PENDING_FEASIBILITY|NOT_VIABLE}} |

## Waivers

<!-- AC:WAIVERS -->
| Waiver ID | Actor ID | Roles | Revision | Approved by | Approved at | Evidence |
|---|---|---|---|---|---|---|

## Усиленное evidence

Для L3 и hard triggers добавь только применимые строки; ссылки допустимы, когда
сырой результат действительно нуждается в отдельном файле.

| Область | Модель/процедура | Результат и остаточный риск | Владелец / evidence | Gate |
|---|---|---|---|---|
| {{THREAT_MODEL_OR_MIGRATION_REHEARSAL_OR_RISK_ACCEPTANCE}} | {{METHOD}} | {{RESULT}} | {{OWNER_AND_LINK_OR_INLINE}} | {{PASS|REWORK|BLOCKED|NOT_APPLICABLE}} |

## Проверка пакета

<!-- AC:PACKAGE_VALIDATION -->
| Snapshot / команда | Errors | Open gates | Warnings / ручные границы | Status |
|---|---:|---:|---|---|
| {{REVISION_OR_HASH_AND_COMMAND}} | {{COUNT}} | {{COUNT}} | {{DETAILS_OR_NONE}} | {{PASS|FAIL|WARNINGS}} |

Структурный PASS не доказывает истинность evidence или разрешение реализации.
