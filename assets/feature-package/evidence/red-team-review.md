---
architecture_revision: "{{REVISION}}"
feature: "{{FEATURE_NAME}}"
artifact: red_team_review
run_id: "{{RUN_ID}}"
subject_revision: "{{ARCHITECTURE_REVISION}}"
status: "{{DRAFT|CHANGES_REQUIRED|EVIDENCE_REQUIRED|NO_BLOCKING_OBJECTION}}"
actor_id: "{{INDEPENDENT_AGENT_OR_PERSON}}"
input_revision: "{{ARCHITECTURE_REVISION_OR_HASH}}"
artifact_language: "{{USER_LANGUAGE}}"
reviewed_at: "{{YYYY-MM-DD}}"
---

# Независимое Red Team review

## Подтверждение независимости

- Не автор Candidate Architecture: {{yes/no}}
- Не выполнял specialist review в этом прогоне: {{yes/no}}
- Не является Arbiter: {{yes/no}}
- Запись процесса: [Process Ledger](../process-ledger.md)

## Scope атаки

- Бизнес-сценарии и потеря требований
- Предположения и недостающее evidence
- Частичные отказы, retry и идемпотентность
- Безопасность, приватность и abuse
- Консистентность, потеря и дублирование данных
- Нагрузка, деградация и backpressure
- Совместимость, миграция, rollout и rollback
- Наблюдаемость, диагностика и восстановление
- Стоимость поставки и эксплуатации

Явные исключения: {{NONE_OR_SCOPE_AND_REASON}}

## Главный вызов архитектуре

{{STRONGEST_CASE_AGAINST_THE_CANDIDATE}}

## Findings

### RED-001: {{TITLE}}

- Severity: `{{blocking|major|minor|note}}`
- Уверенность: `{{high|medium|low}}`
- Тип: `{{fact|inference|assumption|recommendation|unknown}}`
- Требования: {{REQ_IDS}}
- Evidence: {{SOURCES}}

#### Сценарий атаки/отказа

1. {{STEP}}
2. {{STEP}}
3. {{FAILURE_OR_VIOLATION}}

#### Влияние

{{IMPACT}}

#### Условие опровержения finding

{{EVIDENCE_OR_CHANGE}}

## Проверка пропущенной альтернативы

- Проверенные оси карты: {{AXES}}
- Возможная ложная бинарная развилка: {{DESCRIPTION_OR_NONE}}
- Пропущенное семейство/гибрид: {{APPROACH_OR_NONE}}
- Почему оно может быть жизнеспособно: {{RATIONALE}}
- Выводимо из уже известных требований без нового scope: {{yes/no}}
- Статус: `{{NONE|MISSED_SOLUTION_FAMILY|NEW_REQUIREMENT_OR_FACT}}`
- Требуемое follow-up: {{ACTION}}

`MISSED_SOLUTION_FAMILY` требует минимум `CHANGES_REQUIRED`, возврата на Stage 4
и повторного арбитража. Простое исключение без requirement или evidence finding
не закрывает.

## Ответ архитектуры

| Finding | Ответ | Изменение/revision | Evidence | Статус |
|---|---|---|---|---|
| RED-001 | {{RESPONSE}} | {{LINK_OR_REVISION}} | {{LINK}} | {{OPEN/CLOSED/ESCALATED/ACCEPTED_RISK}} |

## Red Team gate

- Значимые findings имеют ответы: {{yes/no}}
- Новые blocking risks устранены или эскалированы: {{yes/no}}
- Пропущенные семейства разрешены: {{yes/no/not_applicable}}
- Итоговый статус: `{{STATUS}}`
