# Architecture diagrams

## Rules

- Храни редактируемые текстовые исходники; используй стандарт проекта или Mermaid.
- Укажи `current`, `target` или `transition` в metadata каждой схемы.
- Укажи назначение, scope, легенду, архитектурную revision и ссылку на
  нормативный текст.
- Подписи и пояснения пиши на языке пользователя.
- Для Architecture at a Glance подготовь отображаемый render или проверь
  нативное отображение Mermaid.
- Обновляй схему и текстовую архитектуру в одной revision.
- Удали placeholders до передачи пакета на review.
- Если render не проверен визуально, зафиксируй gap; статическая проверка исходника
  не считается визуальной проверкой.

## Minimum for L2–L3

- `target/container-view.mmd` — component/container overview.
- `target/key-flow-sequence.mmd` — critical end-to-end flow.

For an existing system also maintain `current/container-view.mmd`. Add state,
data, trust-boundary, deployment, failure and migration diagrams when the
corresponding relationship is material to the decision.
