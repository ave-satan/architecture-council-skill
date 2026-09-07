---
architecture_revision: "{{REVISION}}"
feature: "{{FEATURE_NAME}}"
stage: requirements
status: "{{DRAFT|PASS|REWORK|BLOCKED}}"
owner: "{{OWNER}}"
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# Каталог требований

## Соглашения

- Types: `BR`, `FR`, `QA`, `INV`, `CON`, `TR`.
- Origin: `stated`, `discovered`, `derived`, `proposed`.
- Priority: `MUST`, `SHOULD`, `MAY`.
- Approval: `approved`, `needs_approval`, `rejected`, `superseded`.

## Бизнес-требования

### BR-001: {{TITLE}}

- Формулировка: {{ATOMIC_BUSINESS_OUTCOME}}
- Приоритет: `{{MUST|SHOULD|MAY}}`
- Происхождение: `{{ORIGIN}}`
- Источник: {{SOURCE}}
- Владелец: {{OWNER}}
- Согласование: `{{STATUS}}`
- Сценарии: {{SCN_IDS}}
- Критерий приёмки: {{OBSERVABLE_SUCCESS}}

## Функциональные требования

### FR-001: {{TITLE}}

- Формулировка: {{OBSERVABLE_BEHAVIOR}}
- Приоритет: `{{MUST|SHOULD|MAY}}`
- Происхождение: `{{ORIGIN}}`
- Источник: {{SOURCE}}
- Владелец: {{OWNER}}
- Согласование: `{{STATUS}}`
- Производное от: {{BR_OR_FR_IDS}}
- Сценарии: {{SCN_IDS}}
- Критерий приёмки: {{TESTABLE_CRITERION}}

## Атрибуты качества

### QA-PERF-001: {{TITLE}}

- Категория: `{{performance|reliability|availability|security|scalability|maintainability|observability}}`
- Формулировка: {{MEASURABLE_QUALITY_REQUIREMENT}}
- Условия/нагрузка: {{CONDITION}}
- Цель: {{NUMERIC_TARGET_OR_EXPLICIT_TBD}}
- Измерение: {{HOW_AND_WHERE}}
- Приоритет: `{{MUST|SHOULD|MAY}}`
- Происхождение: `{{ORIGIN}}`
- Источник: {{SOURCE}}
- Владелец: {{OWNER}}
- Согласование: `{{STATUS}}`
- Производное от: {{REQUIREMENT_IDS}}
- Сценарии: {{SCN_IDS}}
- Критерий приёмки: {{TESTABLE_CRITERION}}

## Инварианты

### INV-001: {{TITLE}}

- Формулировка: {{ALWAYS_TRUE_RULE}}
- Приоритет: `{{MUST|SHOULD|MAY}}`
- Происхождение: `{{ORIGIN}}`
- Источник: {{SOURCE}}
- Владелец: {{OWNER}}
- Согласование: `{{STATUS}}`
- Производное от: {{REQUIREMENT_IDS}}
- Сценарии: {{SCN_IDS}}
- Критерий приёмки: {{HOW_TO_PROVE}}

## Ограничения

### CON-001: {{TITLE}}

- Формулировка: {{SOLUTION_SPACE_CONSTRAINT}}
- Приоритет: `{{MUST|SHOULD|MAY}}`
- Происхождение: `{{ORIGIN}}`
- Источник: {{SOURCE}}
- Владелец: {{OWNER}}
- Согласование: `{{STATUS}}`
- Производное от: {{REQUIREMENT_IDS}}
- Сценарии: {{SCN_IDS}}
- Действует до: {{DATE_STAGE_OR_PERMANENT}}
- Последствие: {{IMPACT}}
- Критерий приёмки: {{HOW_TO_PROVE_OR_NA}}

## Переходные требования

### TR-001: {{TITLE}}

- Формулировка: {{MIGRATION_OR_COEXISTENCE_BEHAVIOR}}
- Приоритет: `{{MUST|SHOULD|MAY}}`
- Происхождение: `{{ORIGIN}}`
- Источник: {{SOURCE}}
- Владелец: {{OWNER}}
- Согласование: `{{STATUS}}`
- Производное от: {{REQUIREMENT_IDS}}
- Сценарии: {{SCN_IDS}}
- Применяется на этапе: {{TRANSITION_STAGE}}
- Условие удаления: {{WHEN_NO_LONGER_APPLIES}}
- Критерий приёмки: {{HOW_TO_PROVE}}

## Матрица трассировки

<!-- AC:TRACEABILITY -->

| Бизнес-цель | Требование | Сценарий | Архитектура/ADR | Инкремент | Проверка | Эксплуатационный сигнал |
|---|---|---|---|---|---|---|
| {{BR_ID}} | {{REQ_ID}} | {{SCN_ID}} | {{LINK_OR_ADR}} | {{INC_ID}} | {{VER_ID}} | {{SIG_ID_OR_JUSTIFIED_NA}} |

Каждая колонка обязательна. `N/A; reason=обоснование; owner=владелец` допустим в неприменимых звеньях,
кроме самого Requirement. Все объявленные требования должны иметь строку.
BR/SCN/INC/VER/SIG ссылаются на реальные определения; Architecture/ADR —
Markdown-ссылка на целевую архитектуру/активный ADR или ID активного ADR.
VER обязан явно перечислять проверяемый requirement ID. Машинные IDs и markers
сохраняются при переводе, а их пояснения пишутся на языке пользователя.

## Противоречия и пробелы

| ID | Требования | Проблема | Владелец | Решение/статус |
|---|---|---|---|---|
| {{ID}} | {{REQ_IDS}} | {{DESCRIPTION}} | {{OWNER}} | {{STATUS_OR_LINK}} |

## Результат gate

- Result: `{{PASS|REWORK|BLOCKED}}`
- Unapproved `MUST`: {{COUNT_AND_IDS_OR_NONE}}
- Unresolved `MUST` conflicts: {{COUNT_AND_IDS_OR_NONE}}
- Incomplete traceability chains: {{COUNT_AND_IDS_OR_NONE}}
- Next stage: {{STAGE}}
