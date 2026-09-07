---
architecture_revision: "{{REVISION}}"
feature: "{{FEATURE_NAME}}"
artifact: architecture_options
status: "{{DRAFT|READY_FOR_ARBITRATION|REWORK}}"
solution_space_coverage: "{{PASS|REWORK|BLOCKED}}"
missed_solution_family_status: "{{NONE|REWORKED|OPEN}}"
coverage_challenger_run_id: "{{RUN_ID}}"
coverage_challenger_actor_id: "{{INDEPENDENT_ACTOR_ID}}"
coverage_input_revision: "{{INPUT_REVISION_OR_HASH}}"
owner: solution_architect
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# Архитектурные варианты

## Драйверы решения

1. {{BUSINESS_OR_REQUIREMENT_DRIVER}}
2. {{QUALITY_OR_CONSTRAINT_DRIVER}}

## Карта пространства решений <!-- SSC:MAP -->

Карта создаётся до выбора предпочтительного варианта. Она ограничена
релевантными осями и не требует полного декартова перебора.

### Оси поиска

| Ось | Почему релевантна | Рассмотренные механизмы | Связанные требования |
|---|---|---|---|
| {{CONTROL_DATA_TRANSPORT_TOPOLOGY_SYNC_RENDEZVOUS_FALLBACK_OR_OTHER}} | {{RATIONALE}} | {{MECHANISMS}} | {{REQ_IDS}} |

### Семейства решений <!-- SSC:FAMILIES -->

| Family ID | Семейство/механизм | Источник | Покрываемые требования | Ключевые неизвестные | Статус |
|---|---|---|---|---|---|
| SF-001 | {{SOLUTION_FAMILY}} | {{specialist/solution_architect/alternative_architect/user/red_team}} | {{REQ_IDS}} | {{UNKNOWN_OR_NONE}} | {{CANDIDATE_FAMILY|EXCLUDED_WITH_EVIDENCE|OUT_OF_SCOPE_BY_REQUIREMENT}} |

### Доказательно исключённые семейства

| Family ID | Requirement или evidence исключения | Почему комбинация/вариация не возвращает жизнеспособность | Условия пересмотра |
|---|---|---|---|
| {{SF_ID_OR_NONE}} | {{REQ_OR_EVIDENCE_LINK}} | {{RATIONALE}} | {{TRIGGER_OR_NEVER}} |

## Независимый challenge ширины поиска <!-- SSC:CHALLENGE -->

- Challenger run: {{RUN_ID}}
- Actor ID: {{INDEPENDENT_ACTOR_ID}}
- Input revision/hash: {{REQUIREMENTS_CONSTRAINTS_AND_SPECIALIST_FINDINGS_HASH}}
- Предпочтительный вариант был скрыт: {{yes/no}}
- Пропущенные оси: {{NONE_OR_AXES}}
- Пропущенные семейства или гибриды: {{NONE_OR_SF_IDS_AND_DESCRIPTION}}
- Результат разрешения: {{ADDED_EXCLUDED_WITH_EVIDENCE_OR_NONE}}

## Результат Solution Space Coverage Gate <!-- SSC:GATE -->

- Осмысленные оси перечислены: {{yes/no}}
- Семейства существенно различаются механизмами: {{yes/no}}
- Исключения опираются на requirement/evidence: {{yes/no}}
- Независимый challenge завершён: {{yes/no}}
- Пользовательские и Red Team предложения разрешены: {{yes/no/not_applicable}}
- `missed_solution_family_status`: `{{NONE|REWORKED|OPEN}}`
- `solution_space_coverage`: `{{PASS|REWORK|BLOCKED}}`

При `MISSED_SOLUTION_FAMILY` источник сохраняется как `user` или `red_team`,
этот gate становится `REWORK`, а зависимый Preliminary Decision — `SUPERSEDED`
до повторной проверки.

## Вариант A: {{NAME}}

### Краткое описание и схема

{{END_TO_END_DESCRIPTION_OR_LINK}}

### Покрытие требований

| Требование | Покрытие | Примечания |
|---|---|---|
| {{REQ_ID}} | {{FULL/PARTIAL/NONE}} | {{NOTES}} |

### Предположения

- {{ASM_ID_OR_STATEMENT}}

### Преимущества

- {{ADVANTAGE}}

### Недостатки и ограничения

- {{DISADVANTAGE}}

### Риски и пробелы evidence

- {{RISK_OR_REQUIRED_EVIDENCE}}

### Поставка и эксплуатация

- Сложность реализации: {{ASSESSMENT_AND_BASIS}}
- Время/стоимость: {{ASSESSMENT_AND_BASIS}}
- Эксплуатационная стоимость: {{ASSESSMENT_AND_BASIS}}
- Миграция/совместимость: {{ASSESSMENT}}
- Обратимость: {{ASSESSMENT}}

### Вердикт жизнеспособности

- Статус: `{{VIABLE|PLAUSIBLE_PENDING_FEASIBILITY|NOT_VIABLE}}`
- Blocking deviation: {{NONE_OR_REQ_ID}}
- Незавершённое no-go evidence: {{NONE_OR_EVIDENCE_IDS}}
- Требуемое evidence: {{NONE_OR_LINK}}

## Вариант B: {{NAME}}

{{COPY_THE_SAME_STRUCTURE_AS_OPTION_A}}

## Индекс вариантов

<!-- AC:OPTIONS -->

| Option ID | Описание/ссылка | Feasibility |
|---|---|---|
| OPT-001 | {{DESCRIPTION_OR_LINK}} | {{VIABLE|PLAUSIBLE_PENDING_FEASIBILITY|NOT_VIABLE}} |

## Сравнение

| Критерий | Gate/вес | Вариант A | Вариант B | Evidence |
|---|---|---|---|---|
| Обязательные требования | gate | {{RESULT}} | {{RESULT}} | {{LINK}} |
| Безопасность/целостность данных | gate | {{RESULT}} | {{RESULT}} | {{LINK}} |
| Соответствие бизнесу | {{PRIORITY}} | {{RESULT}} | {{RESULT}} | {{LINK}} |
| Производительность/надёжность | {{PRIORITY}} | {{RESULT}} | {{RESULT}} | {{LINK}} |
| Время/стоимость поставки | {{PRIORITY}} | {{RESULT}} | {{RESULT}} | {{LINK}} |
| Сопровождаемость/эксплуатация | {{PRIORITY}} | {{RESULT}} | {{RESULT}} | {{LINK}} |
| Обратимость | {{PRIORITY}} | {{RESULT}} | {{RESULT}} | {{LINK}} |

## Рекомендация Solution Architect

- Рекомендуемый вариант: {{OPTION}}
- Обоснование: {{RATIONALE}}
- Несогласие/неопределённость: {{DESCRIPTION}}

## Результат gate

- Solution Space Coverage Gate имеет `PASS`: {{yes/no}}
- Все представленные варианты имеют `VIABLE`: {{yes/no}}
- Варианты, ожидающие no-go evidence: {{OPTION_IDS_OR_NONE}}
- Отсутствие второго варианта обосновано: {{yes/no/not_applicable}}
- Требуется независимый output Alternative Architect: {{yes/no}}
- Независимый output присутствует: {{yes/no/not_applicable}}
- Готово к предварительному арбитражу: {{yes/no}}
