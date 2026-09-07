---
feature: "{{FEATURE_NAME}}"
artifact: process_log
architecture_revision: "{{REVISION}}"
diagnostics_mode: "VERBOSE"
run_id: "{{RUN_ID}}"
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# Временная шкала Architecture Council

Журнал содержит только наблюдаемые события процесса. Он не является
нормативной архитектурой и не должен содержать chain-of-thought, сырые prompts,
секреты, исходный код или полные tool outputs.

| # | Timestamp | Event | Stage | Actor/Role | Status | Artifacts | Summary |
|---:|---|---|---|---|---|---|---|
<!-- AC:EVENTS:BEGIN -->
| 1 | {{ISO8601}} | run_started | initialization | council-orchestrator/council_orchestrator | IN_PROGRESS | README.md | {{SAFE_LOCALIZED_SUMMARY}} |
<!-- AC:EVENTS:END -->
