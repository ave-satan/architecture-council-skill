---
feature: "{{FEATURE_NAME}}"
artifact: process_ledger
architecture_revision: "{{REVISION}}"
selected_roles: ["{{ROLE_ID}}"]
artifact_language: "{{USER_LANGUAGE}}"
diagnostics_mode: "{{DIAGNOSTICS_MODE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# Журнал процесса Architecture Council

{{PROCESS_LOG_LINK_OR_DISABLED}} Этот документ остаётся нормативным
подтверждением ролей, независимости и gates.

## Правила идентификации

- `actor_id` стабилен в пределах прогона и однозначно обозначает агента или
  человека.
- Каждая роль получает входную revision/hash до начала работы.
- Нехватка agent slots приводит к последовательному запуску нового исполнителя,
  а не к совмещению несовместимых ролей.

## Запуски ролей

<!-- AC:ROLE_RUNS -->

| Run ID | Stage | Role | Actor ID | Input revision/hash | Output | Gate result | Started | Completed |
|---|---|---|---|---|---|---|---|---|
| RUN-001 | {{STAGE}} | {{ROLE_ID}} | {{ACTOR_ID}} | {{REVISION_OR_HASH}} | {{LINK}} | {{STATUS}} | {{TIME}} | {{TIME}} |

## Покрытие ролей

<!-- AC:ROLE_COVERAGE -->

| Выбранная роль | Независимый output | Findings | Ответ refinement | Re-review | Статус |
|---|---|---|---|---|---|
| {{ROLE_ID}} | {{LINK}} | {{IDS_OR_NONE}} | {{LINK_OR_NA}} | {{LINK_OR_NA}} | {{COMPLETE|MISSING}} |

## Проверка несовместимых ролей

| Actor ID | Выполненные роли | Допустимо | Основание/waiver |
|---|---|---|---|
| {{ACTOR_ID}} | {{ROLES}} | {{yes/no}} | {{RATIONALE_OR_LINK}} |

Запрещённые сочетания без человеческого waiver:

- `solution_architect` + `alternative_architect`;
- `solution_architect` + `solution_space_challenger`;
- автор Candidate Architecture + `red_team`;
- любой specialist + `red_team`;
- автор, specialist, Alternative Architect или Red Team + `arbiter`.

## Возвраты и refinement-циклы

| Cycle | Trigger | From stage | To stage | New evidence/change | Outcome |
|---|---|---|---|---|---|
| {{N}} | {{FINDING_OR_DECISION}} | {{STAGE}} | {{STAGE}} | {{LINK}} | {{RESULT}} |

## Process gate

- Все выбранные роли имеют outputs: {{yes/no}}
- Input revisions зафиксированы: {{yes/no}}
- Несовместимые роли не совмещены: {{yes/no/waiver}}
- Missing roles: {{NONE_OR_IDS}}
- Result: `{{PASS|REWORK|BLOCKED}}`

## Явные отступления от независимости

<!-- AC:WAIVERS -->

| Waiver ID | Actor ID | Roles | Revision | Approved by | Approved at | Evidence |
|---|---|---|---|---|---|---|

Если waiver нет, оставь таблицу без строк. Иначе укажи точный набор Role IDs
через запятую, revision, человека и ISO-8601 дату с timezone. Ссылка ведёт к
локальному evidence человеческого решения с metadata `status: APPROVED`,
`architecture_revision`, `approved_by`, `approved_at` и указанием источника
команды. Валидатор проверяет структуру, а подлинность решения проверяется по
переписке/источнику человеком. Waiver не подменяет отсутствующий output:
выполненная работа остаётся COMPLETE, отступление отображается как WARNING.
