---
architecture_revision: "{{REVISION}}"
feature: "{{FEATURE_NAME}}"
artifact: current_system
status: "{{DRAFT|PASS|REWORK|BLOCKED}}"
owner: system_discovery
repository_root: "{{ABSOLUTE_REPOSITORY_ROOT}}"
code_evidence_status: "{{AVAILABLE|NOT_APPLICABLE}}"
code_evidence_reason: "{{REASON_IF_NOT_APPLICABLE}}"
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# Текущая система

- Границы и источники: {{BOUNDARY_AND_PRIMARY_SOURCES}}
- Текущий сквозной поток: {{FLOW}}
- Подтверждённые факты / противоречия: {{FACTS_AND_CONFLICTS}}

```mermaid
%% ac_id: current-container
%% ac_state: current
%% ac_purpose: обзор текущей системы {{FEATURE_NAME}}
%% ac_scope: {{SCOPE}}
%% ac_legend: стрелка — наблюдаемая связь
%% ac_revision: {{REVISION}}
%% ac_normative: current-system.md
flowchart LR
    User[{{ACTOR}}] --> Client[{{CLIENT}}] --> Service[{{SERVICE}}] --> Store[({{STORE}})]
```

## Поверхности изменения

| Компонент/контракт | Владелец | Текущее поведение и данные | Ограничение/режим отказа | Основания |
|---|---|---|---|---|
| {{ITEM}} | {{OWNER}} | {{BEHAVIOR}} | {{LIMIT_OR_FAILURE}} | {{LINK}} |

## Исполнение, проверки и эксплуатация

| Область | Наблюдаемое состояние | Основания / неизвестность | Следующее действие и владелец |
|---|---|---|---|
| Развёртывание / конфигурация | {{STATE}} | {{LINK_OR_UNKNOWN}} | {{ACTION}} |
| Тесты / контракты | {{STATE}} | {{LINK_OR_UNKNOWN}} | {{ACTION}} |
| Логи / метрики / восстановление | {{STATE}} | {{LINK_OR_UNKNOWN}} | {{ACTION}} |

- Область воздействия: {{COMPONENTS_CONTRACTS_DATA_TESTS_OPERATIONS}}
- Итог исследования: `{{PASS|REWORK|BLOCKED}}`; {{RATIONALE}}

<!-- AC:CODE_EVIDENCE -->
| ID утверждения | Путь от корня репозитория | Ревизия | Начальная строка | Конечная строка |
|---|---|---|---:|---:|
| {{CLAIM_ID}} | {{PATH}} | {{FULL_COMMIT_SHA_OR_WORKTREE_SHA256}} | {{START}} | {{END}} |
