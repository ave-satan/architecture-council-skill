# Заключения профильных специалистов

Создай отдельный файл для каждой роли, выбранной в Feature Classification,
используя [шаблон review](../specialist-review.template.md). Имена файлов должны совпадать с
`conditional_by_role` в `template-manifest.yaml`.

Каждое заключение фиксирует `run_id`, `actor_id`, входную revision/hash и ссылку
на соответствующую запись в Process Ledger. Первичные заключения не показываются
другим специалистам до завершения независимого раунда.
