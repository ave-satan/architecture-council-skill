---
architecture_revision: "{{REVISION}}"
feature: "{{FEATURE_NAME}}"
artifact: verification_plan
status: "{{DRAFT|READY|COMPLETE}}"
owner: verification_strategist
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# План проверки

## Стратегия

{{HOW_CORRECTNESS_AND_QUALITY_WILL_BE_PROVEN}}

## Покрытие требований

<!-- AC:VERIFICATIONS -->

| Verification ID | Требование | Метод | Среда/этап | Тестовые данные/нагрузка | Критерий прохождения | Эксплуатационный сигнал | Владелец |
|---|---|---|---|---|---|---|---|
| VER-001 | {{REQ_ID}} | {{contract/load/failure-injection/rehearsal/manual}} | {{CI/STAGING/PROD}} | {{DATA}} | {{CRITERION}} | {{METRIC_OR_NA}} | {{OWNER}} |

## Проверка контрактов

- Public APIs/events: {{PLAN}}
- Compatibility: {{PLAN}}
- Error behavior: {{PLAN}}
- Idempotency/retry: {{PLAN}}

## Проверка атрибутов качества

### Производительность

- Workload model: {{MODEL}}
- Dataset: {{DATASET}}
- Targets: {{QA_IDS_AND_TARGETS}}
- Evidence location: `evidence/benchmarks/`

### Надёжность

- Failure scenarios: {{SCENARIOS}}
- Recovery checks: {{CHECKS}}
- RPO/RTO or equivalent: {{TARGETS_OR_NA}}

### Безопасность и приватность

- Authorization/abuse cases: {{PLAN}}
- Data handling checks: {{PLAN}}
- Threat model evidence: {{LINK_OR_NA}}

### Миграция

- Rehearsal: {{PLAN_OR_NA}}
- Reconciliation: {{PLAN}}
- Rollback validation: {{PLAN}}

## Проверка в production

<!-- AC:SIGNALS -->

| Signal ID | Сигнал | Query/dashboard | Ожидаемый диапазон | Порог alert/rollback | Владелец |
|---|---|---|---|---|---|
| SIG-001 | {{METRIC_LOG_TRACE}} | {{LINK_OR_QUERY}} | {{RANGE}} | {{THRESHOLD}} | {{OWNER}} |

## Пробелы evidence

| ID | Недостающее evidence | Влияние | Действие | Владелец | Срок |
|---|---|---|---|---|---|
| {{ID}} | {{GAP}} | {{IMPACT}} | {{ACTION}} | {{OWNER}} | {{DATE_OR_STAGE}} |

## Verification gate

- `MUST` coverage: {{COUNT}}/{{TOTAL}}
- Unverifiable architecture decisions: {{IDS_OR_NONE}}
- Missing production signals: {{IDS_OR_NONE}}
- Unfinished no-go evidence: {{IDS_OR_NONE}}
- Result: `{{PASS|CONDITIONAL_PASS|REWORK|BLOCKED}}`

`CONDITIONAL_PASS` запрещён при незавершённом no-go evidence. Изменяющие проект
spikes и benchmarks выполняются только после отдельной явной команды
пользователя.
