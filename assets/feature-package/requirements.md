---
architecture_revision: "{{REVISION}}"
feature: "{{FEATURE_NAME}}"
stage: requirements
status: "{{DRAFT|PASS|REWORK|BLOCKED}}"
owner: "{{OWNER}}"
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# Требования, риски и допущения

Для каждого требования укажи `Priority`, `Origin`, источник/владельца и проверяемый
критерий. Разделяй `BR`, `FR`, `QA`, `INV`, `CON`, `TR`; не превращай предпочтение
или гипотезу реализации в обязательное ограничение.

## BR-001: {{TITLE}}

- Priority / Origin: `{{MUST|SHOULD|MAY}}` / `{{stated|discovered|derived|proposed}}`
- Источник / владелец: {{SOURCE_AND_OWNER}}
- Формулировка: {{ATOMIC_REQUIREMENT}}
- Приёмка: {{MEASURABLE_CRITERION}}

## FR-001: {{TITLE}}

- Priority / Origin: `{{MUST|SHOULD|MAY}}` / `{{stated|discovered|derived|proposed}}`
- Источник / владелец: {{SOURCE_AND_OWNER}}
- Формулировка: {{ATOMIC_REQUIREMENT}}
- Приёмка: {{MEASURABLE_CRITERION}}

{{ADD_QA_INV_CON_TR_SECTIONS_ONLY_WHEN_THEY_EXIST_USING_THE_SAME_COMPACT_SHAPE}}

## Риски, допущения и условия

| ID | Тип | Формулировка и последствие | Владелец | Проверка/mitigation | Статус |
|---|---|---|---|---|---|
| {{RISK_OR_ASM_OR_COND_ID}} | {{RISK|ASSUMPTION|CONDITION}} | {{ITEM_AND_IMPACT}} | {{OWNER}} | {{EVIDENCE_OR_ACTION}} | {{OPEN|VALIDATED|MITIGATED|ACCEPTED|CLOSED}} |

## Матрица трассировки

<!-- AC:TRACEABILITY -->
| BR | Requirement | SCN | Architecture/ADR | INC | VER | SIG |
|---|---|---|---|---|---|---|
| {{BR_ID_OR_NA}} | {{REQUIREMENT_ID_OR_LINK}} | {{SCN_ID_OR_NA}} | {{TARGET_OR_ADR_LINK_OR_NA}} | {{INC_ID_OR_NA}} | {{VER_ID_OR_NA}} | {{SIG_ID_OR_NA}} |

Неприменимая связь: `N/A; reason=...; owner=...`.

## Gate

{{PASS_REWORK_OR_BLOCKED_WITH_ONLY_MATERIAL_GAPS}}
