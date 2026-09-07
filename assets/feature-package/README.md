---
feature: "{{FEATURE_NAME}}"
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
diagnostics_mode: "{{DIAGNOSTICS_MODE}}"
---

# {{FEATURE_NAME}}

<!-- AC:README:summary -->

Начни с [краткого решения](decision-brief.md): это единственный обязательный
документ для решения владельца. Ревизия: **{{REVISION}}**.

<!-- AC:README:overview -->
<!-- AC:README:reading -->
<!-- AC:README:documents -->

## Подробности по задаче

- Обоснование: [рекомендация Council](final-decision.md), [риски](risks-and-assumptions.md).
- Реализация после разрешения: [требования](requirements.md), [архитектура](target-architecture.md), [поставка](delivery-plan.md), [проверки](verification-plan.md), [переход](evolution-plan.md).
- Исходные данные: [цель](feature-charter.md), {{CURRENT_SYSTEM_OR_SYSTEM_CONTEXT_LINK}}.
- Аудит процесса: [роли и gates](process-ledger.md), [исследования](evidence/).

<!-- AC:README:adrs -->

Архитектурные решения: [ADR](adr/).

<!-- AC:README:interpretation -->

Требования и Target — нормативные источники; evidence хранит основания и историю.
Актуальность определяет revision, а не дата открытия файла.

<!-- AC:README:next -->

Ответь на вопрос в [кратком решении](decision-brief.md) прямо в задаче.
Агент запишет ответ в [human-review.md](human-review.md).

<!-- AC:README:implementation -->

Утверждение архитектуры не запускает реализацию: нужна отдельная команда.
[Handoff](implementation-handoff.md) содержит инструкции для этого запуска.
