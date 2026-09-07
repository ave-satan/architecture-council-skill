#!/usr/bin/env python3
"""Append a validated event to canonical JSONL, then regenerate its Markdown view."""
from __future__ import annotations

import argparse
import fcntl
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from diagnostics import event_errors, project_markdown, read_events, write_projection
from package_contract import frontmatter


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    for name in ("event", "status", "summary", "stage", "actor-id", "role", "input-revision", "gate", "return-to-stage", "supersedes", "timestamp", "run-id", "occurred-at", "timing-basis"):
        parser.add_argument("--" + name)
    parser.add_argument("--artifact", action="append", dest="artifacts")
    parser.add_argument("--duration-ms", type=int)
    parser.add_argument("--source", choices=("agent", "user", "system", "validator"))
    parser.add_argument("--rebuild-markdown", action="store_true", help="Восстановить представление из JSONL без нового события")
    args = parser.parse_args()
    package = args.package.resolve()
    jsonl = package / "evidence/process-log.jsonl"
    markdown = package / "evidence/process-log.md"
    appended = False
    try:
        if frontmatter((package / "README.md").read_text()).get("diagnostics_mode") != "VERBOSE":
            raise ValueError("Запись разрешена только при diagnostics_mode: VERBOSE")
        # The existing JSONL is also the lock file; invalid input creates no files.
        with jsonl.open("r+", encoding="utf-8") as stream:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
            events = read_events(jsonl)
            if args.rebuild_markdown:
                if any(getattr(args, key) is not None for key in ("event", "status", "summary", "artifacts", "timestamp")):
                    raise ValueError("--rebuild-markdown не принимает новое событие")
                write_projection(markdown, events)
                print("Markdown восстановлен из канонического JSONL; события не изменены")
                return 0
            event = {"sequence": len(events) + 1, "event_schema": 2,
                     "timestamp": args.timestamp if args.timestamp is not None else datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")}
            for key in ("event", "status", "summary", "stage", "actor_id", "role", "input_revision", "gate", "return_to_stage", "supersedes", "source", "duration_ms", "artifacts", "run_id", "occurred_at", "timing_basis"):
                value = getattr(args, key)
                if value is not None:
                    event[key] = value.strip() if isinstance(value, str) else value
            errors = event_errors(event)
            if errors:
                raise ValueError("; ".join(errors))
            before = markdown.read_text(encoding="utf-8")
            if project_markdown(before, events) != before:
                raise ValueError("Markdown не соответствует JSONL; сначала --rebuild-markdown")
            # Validate the future projection before touching the canonical stream.
            project_markdown(before, events + [event])
            needs_separator = bool(jsonl.stat().st_size) and not jsonl.read_bytes().endswith(b"\n")
            stream.seek(0, 2)
            if needs_separator:
                stream.write("\n")
            stream.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")
            stream.flush()
            appended = True
            write_projection(markdown, events + [event])
    except (OSError, ValueError) as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        if appended:
            print("Событие уже сохранено в JSONL. Не повторяй append; выполни --rebuild-markdown.", file=sys.stderr)
        return 2
    print(f"Добавлено событие #{event['sequence']}: {event['event']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
