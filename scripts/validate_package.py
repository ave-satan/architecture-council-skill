#!/usr/bin/env python3
"""Структурная проверка Architecture Package Protocol v1.2.6 без зависимостей."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Optional

from diagnostics import check_verbose_diagnostics
from package_contract import (frontmatter, selected_roles, check_links, check_readme,
    check_status_consistency, check_traceability, check_roles, check_solution_space_coverage,
    check_diagrams, check_evidence_locations, check_classification, mandatory_roles)


PLACEHOLDER_RE = re.compile(r"\{\{[^{}]+\}\}")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FRONTMATTER_RE = re.compile(r"^---\s*$\n(.*?)\n---\s*$", re.DOTALL | re.MULTILINE)
SENSITIVE_LOG_VALUE_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", re.IGNORECASE),
    re.compile(r"\b(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*\S+", re.IGNORECASE),
    re.compile(r"\bauthorization\s*:\s*bearer\s+\S+", re.IGNORECASE),
)


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def parse_manifest_lists(path: Path) -> tuple[dict[str, list[str]], dict[str, dict[str, list[str]]]]:
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
            value = item.group(2).strip().strip('"\'')
            if len(item.group(1)) >= 4 and subsection:
                nested[section][subsection].append(value)
            elif len(item.group(1)) >= 2:
                flat[section].append(value)
    return dict(flat), {key: dict(value) for key, value in nested.items()}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def manifest_to_package_path(value: str) -> Path:
    prefix = "feature-package/"
    return Path(value[len(prefix) :] if value.startswith(prefix) else value)


def strip_line_suffix(target: str) -> str:
    return re.sub(r":\d+(?::\d+)?$", "", target)


def check_required_files(
    package: Path,
    manifest_flat: dict[str, list[str]],
    manifest_nested: dict[str, dict[str, list[str]]],
    level: str,
    context: str,
    roles: set[str],
    report: Report,
) -> None:
    base_level = "l2" if level == "L3" else level.casefold()
    required = list(manifest_flat.get(f"required_for_{base_level}", []))
    if level in {"L1", "L2", "L3"}:
        required += manifest_flat.get(f"required_for_{context}", [])
    if level == "L3":
        required += manifest_flat.get("additional_for_l3", [])
    for role in sorted(roles):
        required += manifest_nested.get("conditional_by_role", {}).get(role, [])

    for value in sorted(set(required)):
        path = package / manifest_to_package_path(value)
        if not path.is_file():
            report.error(f"Отсутствует обязательный артефакт: {path.relative_to(package)}")


def check_placeholders(package: Path, report: Report, template_mode: bool) -> None:
    if template_mode:
        return
    for path in package.rglob("*"):
        if path.suffix not in {".md", ".mmd", ".yaml", ".yml"} or ".template." in path.name:
            continue
        if PLACEHOLDER_RE.search(read_text(path)):
            report.error(f"Остались placeholders: {path.relative_to(package)}")


def prose_for_language(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]+`", "", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\A---.*?\n---", "", text, count=1, flags=re.DOTALL)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = PLACEHOLDER_RE.sub("", text)
    # Keep human link labels and table prose; exclude literal machine values.
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\b\d{4}-\d{2}-\d{2}T[\d:.+Z-]+", "", text)
    text = re.sub(r"\b[a-fA-F0-9]{32,}\b", "", text)
    text = re.sub(r"(?<!\w)(?:/?[\w.-]+/)+[\w./-]*", "", text)
    text = re.sub(r"\b[\w.-]+\.(?:md|jsonl?|py|mmd|svg|yaml)\b", "", text)
    text = re.sub(r"\b[A-Za-z][A-Za-z0-9]*_[A-Za-z0-9_]+\b", "", text)
    text = re.sub(r"\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+\b", "", text)
    return text


def check_language(package: Path, language: str, report: Report, template_mode: bool) -> None:
    if template_mode:
        return
    for path in package.rglob("*.md"):
        if ".template." in path.name or (path.name == "README.md" and path.parent != package):
            continue
        metadata = frontmatter(read_text(path))
        if metadata.get("artifact_language") != language:
            report.error(
                f"{path.relative_to(package)} не фиксирует artifact_language={language!r}"
            )

    if language not in {"ru", "en"}:
        return
    for path in list(package.rglob("*.md")) + list(package.rglob("*.mmd")):
        text = prose_for_language(read_text(path))
        cyrillic = len(re.findall(r"[А-Яа-яЁё]", text))
        latin = len(re.findall(r"[A-Za-z]", text))
        total = cyrillic + latin
        if total < 300:
            continue
        if language == "ru" and cyrillic / total < 0.35:
            report.error(f"Нарушен язык: {path.relative_to(package)} выглядит преимущественно не русским")
        if language == "en" and latin / total < 0.65:
            report.error(f"Нарушен язык: {path.relative_to(package)} выглядит преимущественно не английским")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    parser.add_argument("--level", choices=("L1", "L2", "L3"), required=True)
    parser.add_argument("--context", choices=("greenfield", "brownfield"), required=True)
    parser.add_argument("--language", required=True, help="Код языка, например ru или en")
    parser.add_argument("--roles", help="Role IDs через запятую; иначе читаются из process-ledger.md")
    parser.add_argument("--phase", choices=("draft", "review"), default="review")
    parser.add_argument("--template-mode", action="store_true", help="Разрешить placeholders шаблона")
    parser.add_argument("--allow-missing-render", action="store_true")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Требовать и проверить VERBOSE diagnostic artifacts",
    )
    args = parser.parse_args()

    package = args.package.resolve()
    if not package.is_dir():
        print(f"[ERROR] Каталог пакета не найден: {package}")
        return 2

    skill_root = Path(__file__).resolve().parents[1]
    flat, nested = parse_manifest_lists(skill_root / "assets" / "template-manifest.yaml")
    roles = selected_roles(package, args.roles)
    report = Report()

    if args.template_mode or args.phase == "review":
        check_required_files(package, flat, nested, args.level, args.context, roles | mandatory_roles(args.level, args.context), report)
        check_placeholders(package, report, args.template_mode)
        check_readme(package, args.language, report, args.template_mode)
        check_status_consistency(package, report, args.template_mode)
        check_traceability(package, report, args.template_mode)
        check_roles(package, roles | mandatory_roles(args.level, args.context), report, args.template_mode)
        check_solution_space_coverage(package, args.level, report, args.template_mode)
        check_classification(package, args.level, args.context, roles, report, args.template_mode)
        check_language(package, args.language, report, args.template_mode)
    check_links(package, report, args.template_mode or args.phase == "draft", args.allow_missing_render)
    check_verbose_diagnostics(package, flat, report, args.template_mode, args.verbose)
    check_diagrams(package, report, args.allow_missing_render, args.context)
    if not args.template_mode:
        check_evidence_locations(package, args.context, report)
    if args.phase == "draft" or args.template_mode:
        print("Проверен только черновик/шаблон; это не PASS готовности к handoff.")

    for message in report.errors:
        print(f"[ERROR] {message}")
    for message in report.warnings:
        print(f"[WARN] {message}")
    print(f"Итог: errors={len(report.errors)}, warnings={len(report.warnings)}")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
