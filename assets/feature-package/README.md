---
feature: "{{FEATURE_NAME}}"
package_format: sectioned-v1
slug: "{{FEATURE_SLUG}}"
council_recommendation: "{{ACCEPTED|ACCEPTED_WITH_CONDITIONS|REWORK_REQUIRED|REJECTED|BLOCKED|ESCALATED}}"
design_maturity: "{{DESIGN_CANDIDATE|EVIDENCE_AUTHORIZED|IMPLEMENTATION_READY|NOT_READY}}"
human_review_status: "{{AWAITING_HUMAN_REVIEW|CHANGES_REQUESTED|APPROVED|REJECTED|ON_HOLD}}"
implementation_start: "NOT_REQUESTED"
level: "{{L0|L1|L2|L3}}"
architecture_revision: "{{REVISION}}"
decision_owner: "{{OWNER}}"
updated_at: "{{YYYY-MM-DD}}"
artifact_language: "{{USER_LANGUAGE}}"
---

# {{FEATURE_NAME}}

<!-- AC:README:summary -->

**{{PLAIN_LANGUAGE_RECOMMENDATION_AND_READINESS}}**

## Решение

{{GOAL_SELECTED_APPROACH_AND_DECISIVE_TRADEOFF_IN_THREE_TO_FIVE_SENTENCES}}

- Ближайшая альтернатива: {{OPTION_AND_WHY_NOT_SELECTED}}
- Архитектура: [целевое решение](target-architecture.md)
- Проверено: {{VERIFIED_SCOPE_WITH_LINKS}}
- Не проверено: {{MATERIAL_EVIDENCE_GAPS_OR_NONE}}

## Условия и риски

| ID | Условие или риск | Последствие | Владелец / следующий шаг |
|---|---|---|---|
| {{ID_OR_NONE}} | {{MATERIAL_ITEM}} | {{CONSEQUENCE}} | {{OWNER_AND_ACTION_OR_LINK}} |

## Решение человека

{{ONE_CONCRETE_DECISION_OR_NEXT_ACTION_WITH_CONSEQUENCES}}

<!-- AC:HUMAN_REVIEW -->
| Дата / кто | Revision | Решение и условия | Источник |
|---|---|---|---|
| {{DATE_AND_OWNER_OR_PENDING}} | {{REVISION}} | {{ACTUAL_DECISION_OR_PENDING}} | {{MESSAGE_OR_LINK_OR_PENDING}} |

<!-- AC:README:overview -->

## Документы

<!-- AC:README:reading -->

Для решения владельцу достаточно разделов выше. Остальные документы нужны для
адресного технического ревью и реализации.

<!-- AC:README:documents -->

- Требования и риски: [requirements.md](requirements.md).
- Целевая архитектура: [target-architecture.md](target-architecture.md).
- Поставка и проверки: [delivery-plan.md](delivery-plan.md).
- Исходные данные: [feature-charter.md](feature-charter.md), {{CURRENT_SYSTEM_OR_SYSTEM_CONTEXT_LINK}}.
- Аудит процесса: [Council Review](evidence/council-review.md).

<!-- AC:README:adrs -->

ADR создаются только для решений с самостоятельным жизненным циклом; их нет,
если всё нормативное решение помещается в Target и этот README.

<!-- AC:README:interpretation -->

Требования и Target — нормативные источники; evidence хранит основания и историю.
Актуальность определяет revision, а не дата открытия файла.

<!-- AC:README:next -->

Ответь на вопрос из раздела «Решение человека» прямо в задаче.
Агент запишет ответ в таблицу Human Review этого README.

<!-- AC:README:implementation -->

Утверждение архитектуры не запускает реализацию: нужна отдельная команда.
При подготовке реализации создаётся `implementation-plan.md`; обычный
дизайн-пакет его не содержит.
