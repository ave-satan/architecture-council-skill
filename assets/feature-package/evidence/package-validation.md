---
feature: "{{FEATURE_NAME}}"
artifact: package_validation
architecture_revision: "{{REVISION}}"
validator_version: "1.2.8"
status: "{{PASS|FAIL|WARNINGS}}"
artifact_language: "{{USER_LANGUAGE}}"
validated_at: "{{YYYY-MM-DD}}"
---

# Проверка Architecture Package

## Команда

```text
{{VALIDATOR_COMMAND}}
```

## Текущий срез

- Фаза и входная ревизия/hash: {{PHASE_AND_INPUT_REVISION_OR_HASH}}
- Структурные ошибки: {{COUNT_AND_LINKS_OR_NONE}}
- Незакрытые gates: {{COUNT_AND_LINKS_OR_NONE}}
- Исторические ограничения/предупреждения: {{DETAILS_OR_NONE}}

Обновляй этот результат после проверки; прежние значимые срезы сохраняй по ссылке.

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

- Содержание схем: {{PASS/NOT_RUN}}; отображение Mermaid предполагается в редакторе пользователя.
- Семантическая корректность evidence: {{PASS/NOT_RUN}}
- Отсутствие изменений production-кода в design run: {{PASS/NOT_PROVABLE}}
