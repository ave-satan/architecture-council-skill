---
feature: "{{FEATURE_NAME}}"
artifact: package_validation
architecture_revision: "{{REVISION}}"
validator_version: "1.2.7"
status: "{{PASS|FAIL|WARNINGS}}"
artifact_language: "{{USER_LANGUAGE}}"
validated_at: "{{YYYY-MM-DD}}"
---

# Проверка Architecture Package

## Команда

```text
{{VALIDATOR_COMMAND}}
```

## Результат

- Exit code: {{CODE}}
- Ошибки: {{COUNT}}
- Предупреждения: {{COUNT}}
- Статус: `{{PASS|FAIL|WARNINGS}}`

## Проверки

| Проверка | Результат | Детали |
|---|---|---|
| Обязательные артефакты | {{PASS/FAIL}} | {{DETAILS}} |
| Незавершённые placeholders | {{PASS/FAIL}} | {{DETAILS}} |
| Относительные ссылки | {{PASS/FAIL}} | {{DETAILS}} |
| Покрытие/независимость ролей | {{PASS/FAIL}} | {{DETAILS}} |
| Полная traceability | {{PASS/FAIL}} | {{DETAILS}} |
| Язык артефактов | {{PASS/WARNING/FAIL}} | {{DETAILS}} |
| README и следующие действия | {{PASS/FAIL}} | {{DETAILS}} |
| Mermaid-блоки и metadata | {{PASS/FAIL}} | {{DETAILS}} |

## Ручные проверки

- Визуальная корректность отрендеренных схем: {{PASS/NOT_RUN}}
- Семантическая корректность evidence: {{PASS/NOT_RUN}}
- Отсутствие изменений production-кода в design run: {{PASS/NOT_PROVABLE}}
