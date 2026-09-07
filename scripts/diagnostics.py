"""Shared event contract and deterministic Markdown projection (stdlib only)."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

PLACEHOLDER_RE = re.compile(r"\{\{[^{}]+\}\}")
BEGIN = "<!-- AC:EVENTS:BEGIN -->"
END = "<!-- AC:EVENTS:END -->"
FORBIDDEN = {
    "prompt", "raw_prompt", "reasoning", "chain_of_thought", "secret", "secrets",
    "token", "tokens", "credential", "credentials", "password", "api_key",
    "raw_output", "tool_output", "source_code", "environment", "environment_variables",
}
SENSITIVE = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", re.I),
    re.compile(r"\b(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*\S+", re.I),
    re.compile(r"\bauthorization\s*:\s*bearer\s+\S+", re.I),
)


def sensitive_errors(value: object, path: str = "event") -> list[str]:
    errors = []
    if isinstance(value, dict):
        for key, child in value.items():
            location = f"{path}.{key}"
            if str(key).casefold() in FORBIDDEN:
                errors.append(f"запрещённое поле {location}")
            errors.extend(sensitive_errors(child, location))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            errors.extend(sensitive_errors(child, f"{path}[{i}]"))
    elif isinstance(value, str) and any(pattern.search(value) for pattern in SENSITIVE):
        errors.append(f"возможные секреты в поле {path}")
    return errors


def parse_timestamp(value: str) -> datetime:
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if "T" not in value or result.tzinfo is None or result.utcoffset().total_seconds() != 0:
        raise ValueError("timestamp должен быть ISO-8601 UTC с timezone")
    return result


def event_errors(event: object, template_mode: bool = False) -> list[str]:
    if not isinstance(event, dict):
        return ["событие должно быть JSON object"]
    errors = sensitive_errors(event)
    if type(event.get("sequence")) is not int or event["sequence"] < 1:
        errors.append("sequence должен быть положительным integer")
    for key in ("timestamp", "event", "status", "summary"):
        value = event.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{key} должен быть непустой строкой")
    stamp = event.get("timestamp")
    if isinstance(stamp, str) and not (template_mode and PLACEHOLDER_RE.search(stamp)):
        try:
            parse_timestamp(stamp)
        except (ValueError, OverflowError):
            errors.append("timestamp должен быть ISO-8601 UTC с timezone")
    for key in ("stage", "actor_id", "role", "input_revision", "gate", "return_to_stage", "supersedes", "source", "run_id", "occurred_at", "timing_basis"):
        if key in event and (not isinstance(event[key], str) or not event[key].strip()):
            errors.append(f"{key} должен быть непустой строкой")
    if "event_schema" in event and (type(event["event_schema"]) is not int or event["event_schema"] != 2):
        errors.append("event_schema должен быть 2 или отсутствовать у legacy события")
    if event.get("event_schema") == 2 and event.get("event") in {"role_started", "role_completed"}:
        for key in ("run_id", "actor_id", "role", "input_revision"):
            if not isinstance(event.get(key), str) or not event[key].strip():
                errors.append(f"граница роли требует {key}")
    if "occurred_at" in event:
        try:
            if parse_timestamp(event["occurred_at"]) > parse_timestamp(stamp):
                errors.append("occurred_at не может быть позже timestamp регистрации")
        except (ValueError, TypeError, AttributeError, OverflowError):
            errors.append("occurred_at и timestamp должны быть ISO-8601 UTC")
        if not event.get("timing_basis"):
            errors.append("occurred_at требует timing_basis")
    if "artifacts" in event and (
        not isinstance(event["artifacts"], list)
        or any(not isinstance(x, str) or not x.strip() for x in event["artifacts"])
    ):
        errors.append("artifacts должен быть списком непустых строк")
    if "duration_ms" in event and (type(event["duration_ms"]) is not int or event["duration_ms"] < 0):
        errors.append("duration_ms должен быть неотрицательным integer")
    if not template_mode and PLACEHOLDER_RE.search(json.dumps(event, ensure_ascii=False)):
        errors.append("событие содержит placeholders")
    return errors


def read_events(path: Path, template_mode: bool = False) -> list[dict]:
    events = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"process-log.jsonl:{line_no}: invalid JSON") from error
        errors = event_errors(event, template_mode)
        if errors:
            raise ValueError(f"process-log.jsonl:{line_no}: " + "; ".join(errors))
        if event["sequence"] != len(events) + 1:
            raise ValueError("sequence должен быть непрерывным от 1")
        if not events and event["event"] != "run_started":
            raise ValueError("Первое событие должно быть run_started")
        events.append(event)
    if not events:
        raise ValueError("process-log.jsonl не содержит событий")
    return events


def cell(value: object) -> str:
    if value is None or value == "":
        return "—"
    return (str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace("|", "&#124;").replace("\r", " ").replace("\n", " "))


def event_rows(events: list[dict]) -> str:
    rows = []
    for event in events:
        details = [f"{key}={event[key]}" for key in ("run_id", "input_revision", "occurred_at", "timing_basis")
                   if event.get("event_schema") == 2 and event.get(key)]
        summary = "; ".join(details + [event["summary"]])
        values = [event["sequence"], event["timestamp"], event["event"], event.get("stage"),
                  "/".join(str(event[k]) for k in ("actor_id", "role") if event.get(k)),
                  event["status"], ", ".join(event.get("artifacts", [])), summary]
        rows.append("| " + " | ".join(cell(value) for value in values) + " |")
    return "\n".join(rows) + "\n"


def project_markdown(markdown: str, events: list[dict]) -> str:
    if markdown.count(BEGIN) != 1 or markdown.count(END) != 1:
        raise ValueError("process-log.md: нужны уникальные AC:EVENTS:BEGIN/END markers")
    before, tail = markdown.split(BEGIN, 1)
    _, after = tail.split(END, 1)
    return before + BEGIN + "\n" + event_rows(events) + END + after


def write_projection(path: Path, events: list[dict]) -> None:
    text = project_markdown(path.read_text(encoding="utf-8"), events)
    temporary = path.with_name(path.name + ".tmp")
    try:
        temporary.write_text(text, encoding="utf-8")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def check_verbose_diagnostics(package, manifest_flat, report, template_mode, verbose_cli):
    # Kept as a public validator entrypoint for the standalone template bundle.
    from package_contract import frontmatter
    readme = package / "README.md"
    mode = frontmatter(readme.read_text()).get("diagnostics_mode") if readme.is_file() else None
    if verbose_cli and mode != "VERBOSE" and not template_mode:
        report.error("--verbose указан, но README diagnostics_mode не равен VERBOSE")
    if not verbose_cli and mode != "VERBOSE":
        return
    required = [package / value.removeprefix("feature-package/")
                for value in manifest_flat.get("required_for_verbose", [])]
    for path in required:
        if not path.is_file():
            report.error(f"Отсутствует VERBOSE артефакт: {path.relative_to(package)}")
    if any(not path.is_file() for path in required):
        return
    try:
        events = read_events(package / "evidence/process-log.jsonl", template_mode)
        if not template_mode and any(e.get("event") in {"role_started", "role_completed"} and not e.get("run_id") for e in events):
            report.warn("Legacy границы ролей без run_id: полноту истории запусков нужно проверить вручную; старые события не переписывать")
        path = package / "evidence/process-log.md"
        markdown = path.read_text(encoding="utf-8")
        if project_markdown(markdown, events) != markdown:
            report.error("process-log.md не соответствует каноническому JSONL; log_event.py --rebuild-markdown")
    except (OSError, ValueError) as error:
        report.error(str(error))
    for name in ("process-log.md", "verbose-review.md"):
        path = package / "evidence" / name
        if not template_mode and frontmatter(path.read_text()).get("diagnostics_mode") != "VERBOSE":
            report.error(f"{name}: diagnostics_mode должен быть VERBOSE")
