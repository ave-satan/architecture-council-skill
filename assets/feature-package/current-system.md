---
architecture_revision: "{{REVISION}}"
feature: "{{FEATURE_NAME}}"
artifact: current_system_dossier
status: "{{DRAFT|PASS|PARTIAL|BLOCKED}}"
owner: system_discovery_analyst
repository_revision: "{{COMMIT_OR_VERSION}}"
repository_root: "{{ABSOLUTE_REPOSITORY_ROOT}}"
code_evidence_status: "{{RECORDED|NOT_APPLICABLE}}"
code_evidence_reason: "{{REASON_IF_NOT_APPLICABLE}}"
artifact_language: "{{USER_LANGUAGE}}"
observed_at: "{{YYYY-MM-DD}}"
---

# Досье текущей системы

## Границы исследования

- Investigated: {{FEATURE_RELEVANT_SCOPE}}
- Explicitly excluded: {{EXCLUDED_SCOPE_AND_REASON}}
- Entry points: {{ENTRY_POINTS}}

## Текущая архитектура в одном взгляде

![Текущая архитектура](diagrams/rendered/current-container-view.svg)

Исходник: [current/container-view.mmd](diagrams/current/container-view.mmd).

## Текущий end-to-end flow

1. {{STEP_WITH_COMPONENT}}
2. {{STEP_WITH_COMPONENT}}
3. {{OBSERVABLE_OUTCOME}}

## Компоненты и владение

| Компонент | Ответственность | Собственные данные | Команда/владелец | Evidence |
|---|---|---|---|---|
| {{COMPONENT}} | {{RESPONSIBILITY}} | {{DATA}} | {{OWNER}} | {{SOURCE}} |

## Контракты и интеграции

| Контракт | Производитель | Потребитель | Ограничения совместимости | Evidence |
|---|---|---|---|---|
| {{API_EVENT_JOB}} | {{PRODUCER}} | {{CONSUMER}} | {{CONSTRAINT}} | {{SOURCE}} |

## Данные и консистентность

| Данные | System of record | Жизненный цикл | Транзакционная граница | Evidence |
|---|---|---|---|---|
| {{DATA}} | {{OWNER}} | {{LIFECYCLE}} | {{BOUNDARY}} | {{SOURCE}} |

## Runtime и deployment

- Runtime topology: {{DESCRIPTION_OR_LINK}}
- Scaling model: {{DESCRIPTION}}
- Timeouts/retries: {{DESCRIPTION}}
- Deployment mechanism: {{DESCRIPTION}}
- Relevant configuration: {{SOURCES}}

## Существующие паттерны и ADR

| Паттерн/решение | Значимость | Статус | Evidence |
|---|---|---|---|
| {{PATTERN}} | {{WHY_RELEVANT}} | {{ACTIVE_OR_STALE}} | {{SOURCE}} |

## Тесты и наблюдаемые контракты

| Поведение | Evidence | Уверенность |
|---|---|---|
| {{BEHAVIOR}} | {{TEST_METRIC_OR_TRACE}} | {{high/medium/low}} |

## Эксплуатация и известные failure modes

| Failure mode | Текущая обработка | Сигнал/runbook | Evidence |
|---|---|---|---|
| {{FAILURE}} | {{HANDLING}} | {{SIGNAL}} | {{SOURCE}} |

## Противоречия источников

| ID | Утверждение | Источник A | Источник B | Требуемое разрешение |
|---|---|---|---|---|
| DISC-001 | {{CLAIM}} | {{SOURCE_AND_VALUE}} | {{SOURCE_AND_VALUE}} | {{ACTION}} |

## Ожидаемый blast radius

- {{COMPONENT_CONTRACT_DATA_TEAM}}

## Неизвестные и адресные follow-up

| ID | Неизвестное | Влияние | Следующее действие | Владелец |
|---|---|---|---|---|
| Q-001 | {{UNKNOWN}} | {{IMPACT}} | {{DISCOVERY_SPIKE_QUESTION}} | {{OWNER}} |

## Индекс evidence

| Claim ID | Тип | Утверждение | Источник | Уверенность |
|---|---|---|---|---|
| CLM-001 | {{fact/inference/unknown}} | {{CLAIM}} | {{FULL_REPO_RELATIVE_PATH_AND_LINES_AT_REVISION}} | {{LEVEL}} |

Evidence без полного repo-relative пути и зафиксированной revision считается
неоднозначным. Будущий контракт маркируется как proposed и не записывается как
existing invariant.

## Discovery gate

- Current flow explained: {{yes/no}}
- Blast radius bounded: {{yes/no}}
- Constraints sourced: {{yes/no}}
- Unknowns explicit: {{yes/no}}
- Result: `{{PASS|PARTIAL|BLOCKED}}`

## Проверяемые ссылки на код

<!-- AC:CODE_EVIDENCE -->

| Claim ID | Repo-relative path | Revision | Start | End |
|---|---|---|---|---|
| CLM-001 | {{REPO_RELATIVE_PATH}} | {{FULL_COMMIT_SHA_OR_WORKTREE_SHA256}} | {{FIRST_LINE}} | {{LAST_LINE}} |

Для committed-кода используй полный commit SHA. Для локальных изменений —
`WORKTREE:<sha256 содержимого файла>`. Валидатор читает ровно этот snapshot
через Git или проверяет текущий hash; номера строк включительны. Для исследования
без code claims удали строку и явно укажи `code_evidence_status: NOT_APPLICABLE`
с `code_evidence_reason`. Семантика утверждения всё равно требует review.
