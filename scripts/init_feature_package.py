#!/usr/bin/env python3
"""Создаёт Architecture Package Protocol v1.2.6 из ресурсов локального skill."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import shlex
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Optional

from package_contract import mandatory_roles
from diagnostics import BEGIN, END, event_errors, event_rows


SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSETS_ROOT = SKILL_ROOT / "assets"
TEMPLATE_ROOT = ASSETS_ROOT / "feature-package"
MANIFEST = ASSETS_ROOT / "template-manifest.yaml"
SPECIALIST_ROLE_BY_STEM = {
    "domain-architecture": "domain_architect",
    "implementation-maintainability": "implementation_maintainability",
    "security-privacy": "security_privacy",
    "performance-reliability": "performance_reliability",
    "data-consistency": "data_consistency",
    "operations-observability": "operations_observability",
    "verification": "verification_strategist",
    "evolution-integration": "evolution_integration",
}
SENSITIVE_VALUE_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", re.IGNORECASE),
    re.compile(r"\b(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*\S+", re.IGNORECASE),
    re.compile(r"\bauthorization\s*:\s*bearer\s+\S+", re.IGNORECASE),
)


def parse_manifest_lists(
    path: Path,
) -> tuple[dict[str, list[str]], dict[str, dict[str, list[str]]]]:
    flat: dict[str, list[str]] = defaultdict(list)
    nested: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    section: Optional[str] = None
    subsection: Optional[str] = None

    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        top = re.match(r"^([a-zA-Z0-9_]+):\s*$", raw)
        if top:
            section = top.group(1)
            subsection = None
            continue
        sub = re.match(r"^  ([a-zA-Z0-9_]+):\s*$", raw)
        if sub and section:
            subsection = sub.group(1)
            continue
        item = re.match(r"^(\s*)-\s+(.+?)\s*$", raw)
        if item and section:
            value = item.group(2).strip().strip("\"'")
            if len(item.group(1)) >= 4 and subsection:
                nested[section][subsection].append(value)
            elif len(item.group(1)) >= 2:
                flat[section].append(value)
    return dict(flat), {key: dict(value) for key, value in nested.items()}


def package_relative(manifest_path: str) -> Path:
    prefix = "feature-package/"
    value = manifest_path[len(prefix) :] if manifest_path.startswith(prefix) else manifest_path
    return Path(value)


def parse_roles(value: Optional[str]) -> list[str]:
    if not value:
        return []
    roles = [item.strip() for item in value.split(",") if item.strip()]
    duplicates = sorted({role for role in roles if roles.count(role) > 1})
    if duplicates:
        raise ValueError(f"Роли повторяются: {', '.join(duplicates)}")
    return roles


def validate_initial_summary(value: Optional[str]) -> None:
    if value is None:
        return
    for pattern in SENSITIVE_VALUE_PATTERNS:
        if pattern.search(value):
            raise ValueError(
                "initial-log-summary похож на секрет или credential; используй безопасное резюме"
            )


def required_paths(level: str, context: str, roles: list[str]) -> list[Path]:
    flat, nested = parse_manifest_lists(MANIFEST)
    base_level = "l2" if level == "L3" else level.casefold()
    values = list(flat.get(f"required_for_{base_level}", []))
    if level in {"L1", "L2", "L3"}:
        values += flat.get(f"required_for_{context}", [])
    if level == "L3":
        values += flat.get("additional_for_l3", [])

    known_roles = nested.get("conditional_by_role", {})
    unknown = sorted(set(roles) - set(known_roles))
    if unknown:
        raise ValueError(
            "Неизвестные role IDs: "
            + ", ".join(unknown)
            + ". Допустимы: "
            + ", ".join(sorted(known_roles))
        )
    for role in roles:
        values += known_roles.get(role, [])
    return sorted({package_relative(value) for value in values})


def verbose_paths() -> list[Path]:
    flat, _ = parse_manifest_lists(MANIFEST)
    return [package_relative(value) for value in flat.get("required_for_verbose", [])]


def source_for(relative: Path) -> Path:
    direct = TEMPLATE_ROOT / relative
    if direct.is_file():
        return direct
    if relative.parts[:2] == ("evidence", "specialist-reviews"):
        return TEMPLATE_ROOT / "evidence" / "specialist-review.template.md"
    raise FileNotFoundError(f"Для обязательного артефакта нет шаблона: {relative}")


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def copy_support_files(target: Path, level: str, context: str) -> None:
    support = [
        Path("adr/ADR-NNN-template.md"),
        Path("evidence/benchmark.template.md"),
        Path("evidence/conflict.template.md"),
        Path("evidence/human-decision-request.template.md"),
        Path("evidence/specialist-review.template.md"),
        Path("evidence/specialist-reviews/README.md"),
        Path("evidence/spike.template.md"),
        Path("feature-classification.md"),
    ]
    support.append(
        Path("current-system.md") if context == "brownfield" else Path("system-context.md")
    )
    for relative in support:
        copy_file(TEMPLATE_ROOT / relative, target / relative)


def substitute_known_values(
    target: Path,
    *,
    feature: str,
    slug: str,
    language: str,
    level: str,
    context: str,
    revision: str,
    roles: list[str],
    diagnostics_mode: str,
) -> None:
    context_link = (
        "[Current System Dossier](current-system.md)"
        if context == "brownfield"
        else "[System Context](system-context.md)"
    )
    threat_model = (
        "[Threat Model](evidence/threat-model.md)"
        if level == "L3"
        else "N/A — для выбранного уровня не требуется; владелец: Council Orchestrator"
    )
    replacements = {
        "{{FEATURE_NAME}}": feature,
        "{{FEATURE_SLUG}}": slug,
        "{{USER_LANGUAGE}}": language,
        "{{YYYY-MM-DD}}": date.today().isoformat(),
        "{{REVISION}}": revision,
        "{{L0|L1|L2|L3}}": level,
        "{{greenfield|brownfield}}": context,
        "{{CURRENT_SYSTEM_OR_SYSTEM_CONTEXT_LINK}}": context_link,
        "{{THREAT_MODEL_LINK_OR_NOT_APPLICABLE}}": threat_model,
        "{{DIAGNOSTICS_MODE}}": diagnostics_mode,
    }
    role_list = ", ".join(f'"{role}"' for role in roles)

    for path in target.rglob("*"):
        if path.suffix not in {".md", ".mmd", ".yaml", ".yml"}:
            continue
        text = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace('"' + old + '"', json.dumps(new, ensure_ascii=False))
            text = text.replace(old, new)
        if path.parent.name == "specialist-reviews" and path.name != "README.md":
            role = SPECIALIST_ROLE_BY_STEM.get(path.stem)
            if role:
                text = text.replace("{{ROLE}}", role)
        if path.name in {"process-ledger.md", "feature-classification.md"}:
            text = re.sub(
                r'^selected_roles:\s*\[.*?\]\s*$',
                f"selected_roles: [{role_list}]",
                text,
                flags=re.MULTILINE,
            )
        path.write_text(text, encoding="utf-8")


def initialize_verbose_log(
    target: Path,
    *,
    feature: str,
    language: str,
    revision: str,
    initial_summary: Optional[str],
) -> None:
    evidence = target / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    run_id = "AC-" + timestamp.replace("-", "").replace(":", "").replace("Z", "Z")
    summary = initial_summary or (
        "Инициализирован диагностический прогон Architecture Council."
        if language == "ru"
        else "Architecture Council verbose run initialized."
    )
    event = {
        "sequence": 1,
        "timestamp": timestamp,
        "event": "run_started",
        "status": "IN_PROGRESS",
        "stage": "initialization",
        "actor_id": "council-orchestrator",
        "role": "council_orchestrator",
        "input_revision": revision,
        "artifacts": ["README.md"],
        "source": "system",
        "summary": summary,
    }
    errors = event_errors(event)
    if errors:
        raise ValueError("; ".join(errors))
    markdown_summary = summary.replace("|", "\\|").replace("\r", " ").replace("\n", " ")
    (evidence / "process-log.jsonl").write_text(
        json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    markdown = f'''---
feature: {json.dumps(feature, ensure_ascii=False)}
artifact: process_log
architecture_revision: {json.dumps(revision, ensure_ascii=False)}
diagnostics_mode: "VERBOSE"
run_id: "{run_id}"
artifact_language: "{language}"
updated_at: "{date.today().isoformat()}"
---

# Временная шкала Architecture Council

Журнал содержит только наблюдаемые события процесса. Он не является
нормативной архитектурой и не должен содержать chain-of-thought, сырые prompts,
секреты, исходный код или полные tool outputs.

| # | Timestamp | Event | Stage | Actor/Role | Status | Artifacts | Summary |
|---:|---|---|---|---|---|---|---|
{BEGIN}
{event_rows([event])}{END}
'''
    (evidence / "process-log.md").write_text(markdown, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="Новый или пустой каталог Architecture Package")
    parser.add_argument("--level", choices=("L1", "L2", "L3"), required=True)
    parser.add_argument("--context", choices=("greenfield", "brownfield"), required=True)
    parser.add_argument("--language", required=True, help="Код языка, например ru или en")
    parser.add_argument("--feature", required=True, help="Название фичи на языке пользователя")
    parser.add_argument("--slug", required=True, help="Стабильный файловый slug фичи")
    parser.add_argument("--revision", default="architecture-v1")
    parser.add_argument("--roles", help="Role IDs через запятую")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Включить диагностический process log для разработки или dry run",
    )
    parser.add_argument(
        "--initial-log-summary",
        help="Локализованное краткое описание первого события VERBOSE",
    )
    args = parser.parse_args()

    try:
        roles = parse_roles(args.roles)
        validate_initial_summary(args.initial_log_summary)
        if args.verbose and args.initial_log_summary is not None and not args.initial_log_summary.strip():
            raise ValueError("initial-log-summary не может быть пустым")
        roles = sorted(set(roles) | mandatory_roles(args.level, args.context))
        paths = required_paths(args.level, args.context, roles)
    except (ValueError, FileNotFoundError) as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        return 2

    target = args.target.resolve()
    if target.exists() and not target.is_dir():
        print(f"[ERROR] Target существует и не является каталогом: {target}", file=sys.stderr)
        return 2
    if target.exists() and any(target.iterdir()):
        print(f"[ERROR] Target не пуст; существующий пакет не перезаписан: {target}", file=sys.stderr)
        return 2

    target.mkdir(parents=True, exist_ok=True)
    try:
        for relative in paths:
            copy_file(source_for(relative), target / relative)
        copy_support_files(target, args.level, args.context)
        if args.verbose:
            for relative in verbose_paths():
                if relative.name == "verbose-review.md":
                    copy_file(source_for(relative), target / relative)
        substitute_known_values(
            target,
            feature=args.feature,
            slug=args.slug,
            language=args.language,
            level=args.level,
            context=args.context,
            revision=args.revision,
            roles=roles,
            diagnostics_mode="VERBOSE" if args.verbose else "NORMAL",
        )
        if args.verbose:
            initialize_verbose_log(
                target,
                feature=args.feature,
                language=args.language,
                revision=args.revision,
                initial_summary=args.initial_log_summary,
            )
    except (OSError, ValueError) as error:
        print(f"[ERROR] Не удалось создать пакет: {error}", file=sys.stderr)
        return 2

    validator = SKILL_ROOT / "scripts" / "validate_package.py"
    role_arg = f" --roles {','.join(roles)}" if roles else ""
    print(f"Architecture Package создан: {target}")
    print(f"Уровень/контекст: {args.level}/{args.context}; язык: {args.language}")
    print(f"Выбранные роли: {', '.join(roles) if roles else 'нет дополнительных ролей'}")
    print("Следующий шаг: заполнить пакет по стадиям Protocol v1.2.6.")
    if args.verbose:
        print("Диагностика: VERBOSE; события добавляет только Council Orchestrator через log_event.py.")
    print(
        "Проверка шаблона: "
        f"python3 {shlex.quote(str(validator))} {shlex.quote(str(target))} --level {args.level} "
        f"--context {args.context} --language {args.language}{role_arg} "
        "--template-mode"
        + (" --verbose" if args.verbose else "")
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
