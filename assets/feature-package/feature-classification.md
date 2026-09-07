---
architecture_revision: "{{REVISION}}"
feature: "{{FEATURE_NAME}}"
stage: classification
status: "{{PASS|REWORK|BLOCKED}}"
level: "{{L0|L1|L2|L3}}"
context: "{{greenfield|brownfield}}"
selected_roles: ["{{ROLE_ID}}"]
classification_basis_sha256: "{{RECORD_AFTER_CLASSIFICATION_REVIEW}}"
owner: council_orchestrator
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# Классификация фичи

## Оценки

| Ось | 0–3 | Обоснование | Evidence |
|---|---:|---|---|
| Влияние на бизнес | {{N}} | {{RATIONALE}} | {{SOURCE}} |
| Ширина архитектурных изменений | {{N}} | {{RATIONALE}} | {{SOURCE}} |
| Влияние на данные | {{N}} | {{RATIONALE}} | {{SOURCE}} |
| Чувствительность NFR | {{N}} | {{RATIONALE}} | {{SOURCE}} |
| Влияние на безопасность | {{N}} | {{RATIONALE}} | {{SOURCE}} |
| Неопределённость | {{N}} | {{RATIONALE}} | {{SOURCE}} |

**Итого:** {{TOTAL}}

## Жёсткие триггеры

- {{TRIGGER_OR_NONE}}

Для чувствительных данных отдельно зафиксируй владельца, масштаб, нормативные
обязательства, blast radius, восстановимость и последствия компрометации. Сам
факт чувствительности данных без этого анализа не является автоматическим L3.

## Итоговый уровень

`{{LEVEL}}`

Обоснование: {{RATIONALE}}

## Состав Council

| Role ID | Роль | Подключается | Actor ID/план запуска | Причина или основание исключения |
|---|---|---|---|---|
| intake_requirements | Intake & Requirements | yes | {{ACTOR_OR_PENDING}} | mandatory core |
| domain_architect | Domain Architect | {{yes/no}} | {{ACTOR_OR_PENDING}} | {{RATIONALE}} |
| system_discovery | System Discovery | {{yes/no}} | {{ACTOR_OR_PENDING}} | {{RATIONALE}} |
| solution_architect | Solution Architect | {{yes/no}} | {{ACTOR_OR_PENDING}} | {{RATIONALE}} |
| implementation_maintainability | Implementation & Maintainability | {{yes/no}} | {{ACTOR_OR_PENDING}} | {{RATIONALE}} |
| security_privacy | Security & Privacy | {{yes/no}} | {{ACTOR_OR_PENDING}} | {{RISK_SIGNAL_OR_EXCLUSION}} |
| performance_reliability | Performance & Reliability | {{yes/no}} | {{ACTOR_OR_PENDING}} | {{RISK_SIGNAL_OR_EXCLUSION}} |
| data_consistency | Data & Consistency | {{yes/no}} | {{ACTOR_OR_PENDING}} | {{RISK_SIGNAL_OR_EXCLUSION}} |
| operations_observability | Operations & Observability | {{yes/no}} | {{ACTOR_OR_PENDING}} | {{RISK_SIGNAL_OR_EXCLUSION}} |
| verification_strategist | Verification Strategist | {{yes/no}} | {{ACTOR_OR_PENDING}} | {{RISK_SIGNAL_OR_EXCLUSION}} |
| evolution_integration | Evolution & Integration | {{yes/no}} | {{ACTOR_OR_PENDING}} | {{RISK_SIGNAL_OR_EXCLUSION}} |
| solution_space_challenger | Solution Space Challenger | {{yes/no}} | {{INDEPENDENT_ACTOR_OR_PENDING}} | mandatory for L2-L3 |
| alternative_architect | Alternative Architect | {{yes/no}} | {{INDEPENDENT_ACTOR_OR_PENDING}} | {{RISK_SIGNAL_OR_EXCLUSION}} |
| red_team | Red Team | {{yes/no}} | {{INDEPENDENT_ACTOR_OR_PENDING}} | {{RATIONALE}} |
| arbiter | Arbiter | {{yes/no}} | {{INDEPENDENT_ACTOR_OR_PENDING}} | {{RATIONALE}} |
| human_decision_owner | Human Decision Owner | yes | {{PERSON_OR_EXTERNAL_OWNER}} | required for human review |

## План с учётом agent slots

- Доступные slots: {{N_OR_UNKNOWN}}
- Параллельные группы: {{GROUPS}}
- Последовательный fallback: {{ORDER}}
- Проверка несовместимых ролей: [Process Ledger](process-ledger.md)

## Требуемые evidence

- {{SPIKE_BENCHMARK_REVIEW_OR_NONE}}

## Результат gate

- Результат: `{{PASS|REWORK|BLOCKED}}`
- Причина: {{RATIONALE}}
- Независимые исполнители доступны: {{yes/no}}
- Следующая стадия: {{STAGE}}

## Актуальность классификации

После discovery, новых требований или смены архитектурного механизма проверь
уровень, hard triggers, роли и evidence. При изменении уровня обнови состав
пакета по manifest. Затем выполни `record_classification.py PACKAGE`: он
связывает классификацию с текущими Charter, Requirements и Context/Dossier.
Изменение этих входов требует повторной проверки классификации, а не просто
механической замены hash. Перед финальной валидацией выполняй команду после
последнего изменения входных документов.
