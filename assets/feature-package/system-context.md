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

| Система | Назначение | Входящий/исходящий контракт | Владелец | Основания |
|---|---|---|---|---|
| {{SYSTEM}} | {{PURPOSE}} | {{CONTRACT}} | {{OWNER}} | {{SOURCE}} |

## Среда и платформы

- Клиенты и устройства: {{PLATFORMS}}
- Исполнение/развёртывание: {{ENVIRONMENT}}
- Сети и связность: {{NETWORK_CONSTRAINTS}}
- Доступные хранилища и инфраструктура: {{CAPABILITIES}}

## Границы доверия и данные

| Граница | Что пересекает | Кто контролирует | Риск/ограничение |
|---|---|---|---|
| {{BOUNDARY}} | {{DATA_OR_ACTION}} | {{OWNER}} | {{RISK}} |

## Организационные и нормативные ограничения

- {{CONSTRAINT_AND_SOURCE}}

## Предполагаемая область воздействия

- {{COMPONENT_SYSTEM_TEAM_OR_USER_GROUP}}

## Неизвестные

| ID | Тип | Неизвестное | Влияние | Следующее действие | Владелец |
|---|---|---|---|---|---|
| Q-001 | {{discoverable/assumable/blocking}} | {{UNKNOWN}} | {{IMPACT}} | {{ACTION}} | {{OWNER}} |

## Итог определения контекста

- Внешние границы определены: {{yes/no}}
- Основные контракты и владельцы известны: {{yes/no}}
- Границы доверия обозначены: {{YES_OR_NO}}
- Неизвестные классифицированы: {{yes/no}}
- Результат: `{{PASS|PARTIAL|BLOCKED}}`
