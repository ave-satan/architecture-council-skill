---
architecture_revision: "{{REVISION}}"
feature: "{{FEATURE_NAME}}"
artifact: pilot_observations
protocol_version: "1.2.7"
artifact_language: "{{USER_LANGUAGE}}"
updated_at: "{{YYYY-MM-DD}}"
---

# Наблюдения dry run

## Краткий итог

{{WHAT_WORKED_WHAT_FAILED_AND_WHY}}

## Прохождение стадий

| Stage | Вход | Выход | Gate | Возвраты | Нарушения/waivers |
|---|---|---|---|---:|---|
| {{STAGE}} | {{INPUT}} | {{OUTPUT}} | {{STATUS}} | {{N}} | {{NONE_OR_DESCRIPTION}} |

## Роли и независимость

| Роль | Actor ID | Output | Input revision | Независимость подтверждена |
|---|---|---|---|---|
| {{ROLE}} | {{ACTOR_ID}} | {{LINK}} | {{REVISION}} | {{yes/no/waiver}} |

## Refinement и пользовательские вмешательства

| Событие | Причина | Что изменилось | Кто решил | Затраты/turns |
|---|---|---|---|---|
| {{EVENT}} | {{REASON}} | {{CHANGE}} | {{OWNER}} | {{VALUE}} |

Если пользователь или Red Team после `PASS` предлагает ранее не рассмотренное
семейство, проверь критерии `MISSED_SOLUTION_FAMILY` и зафиксируй событие здесь
с источником идеи и возвратом на Stage 4.

## Пробелы протокола и шаблонов

| ID | Наблюдение | Влияние | Предлагаемое изменение | Приоритет |
|---|---|---|---|---|
| PILOT-001 | {{OBSERVATION}} | {{IMPACT}} | {{CHANGE}} | {{HIGH_MEDIUM_LOW}} |

## Что сохранить без изменений

- {{PRACTICE}}
