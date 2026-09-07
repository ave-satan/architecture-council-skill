---
architecture_revision: "{{REVISION}}"
feature: "{{FEATURE_NAME}}"
artifact: greenfield_system_context
status: "{{DRAFT|PASS|PARTIAL|BLOCKED}}"
owner: system_discovery_analyst
artifact_language: "{{USER_LANGUAGE}}"
observed_at: "{{YYYY-MM-DD}}"
---

# Контекст greenfield-системы

## Границы исследования

- Исследовано: {{SCOPE}}
- Явно исключено: {{EXCLUDED_SCOPE_AND_REASON}}
- Источники: {{PRODUCT_DOCS_POLICIES_INTERVIEWS_EXTERNAL_CONTRACTS}}

## Пользователи и акторы

| Актор | Цель | Доверие/полномочия | Ограничения | Источник |
|---|---|---|---|---|
| {{ACTOR}} | {{GOAL}} | {{TRUST}} | {{CONSTRAINT}} | {{SOURCE}} |

## Внешние системы и контракты

| Система | Назначение | Входящий/исходящий контракт | Владелец | Evidence |
|---|---|---|---|---|
| {{SYSTEM}} | {{PURPOSE}} | {{CONTRACT}} | {{OWNER}} | {{SOURCE}} |

## Среда и платформы

- Клиенты и устройства: {{PLATFORMS}}
- Runtime/deployment: {{ENVIRONMENT}}
- Сети и connectivity: {{NETWORK_CONSTRAINTS}}
- Доступные хранилища и инфраструктура: {{CAPABILITIES}}

## Trust boundaries и данные

| Граница | Что пересекает | Кто контролирует | Риск/ограничение |
|---|---|---|---|
| {{BOUNDARY}} | {{DATA_OR_ACTION}} | {{OWNER}} | {{RISK}} |

## Организационные и нормативные ограничения

- {{CONSTRAINT_AND_SOURCE}}

## Предполагаемый blast radius

- {{COMPONENT_SYSTEM_TEAM_OR_USER_GROUP}}

## Неизвестные

| ID | Тип | Неизвестное | Влияние | Следующее действие | Владелец |
|---|---|---|---|---|---|
| Q-001 | {{discoverable/assumable/blocking}} | {{UNKNOWN}} | {{IMPACT}} | {{ACTION}} | {{OWNER}} |

## Context gate

- Внешние границы определены: {{yes/no}}
- Основные контракты и владельцы известны: {{yes/no}}
- Trust boundaries обозначены: {{yes/no}}
- Неизвестные классифицированы: {{yes/no}}
- Result: `{{PASS|PARTIAL|BLOCKED}}`
