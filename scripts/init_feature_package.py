#!/usr/bin/env python3
"""Создаёт sectioned Architecture Package Protocol v1.5.1."""

from __future__ import annotations

import argparse
import fcntl
import json
import re
import shutil
import sys
import shlex
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Optional

from package_contract import KNOWN_ROLES, mandatory_roles


SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSETS_ROOT = SKILL_ROOT / "assets"
TEMPLATE_ROOT = ASSETS_ROOT / "feature-package"
MANIFEST = ASSETS_ROOT / "template-manifest.yaml"
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


def required_paths(level: str, context: str, roles: list[str]) -> list[Path]:
    flat, nested = parse_manifest_lists(MANIFEST)
    base_level = "l2" if level == "L3" else level.casefold()
    values = list(flat.get(f"required_for_{base_level}", []))
    if level in {"L1", "L2", "L3"}:
        values += flat.get(f"required_for_{context}", [])
    if level == "L3":
        values += flat.get("additional_for_l3", [])

    unknown = sorted(set(roles) - KNOWN_ROLES)
    if unknown:
        raise ValueError(
            "Неизвестные role IDs: "
            + ", ".join(unknown)
            + ". Допустимы: "
            + ", ".join(sorted(KNOWN_ROLES))
        )
    return sorted({package_relative(value) for value in values})


def source_for(relative: Path) -> Path:
    direct = TEMPLATE_ROOT / relative
    if direct.is_file():
        return direct
    raise FileNotFoundError(f"Для обязательного артефакта нет шаблона: {relative}")


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


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
) -> None:
    context_link = (
        "[Current System Dossier](current-system.md)"
        if context == "brownfield"
        else "[System Context](system-context.md)"
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
    }
    role_list = ", ".join(f'"{role}"' for role in roles)

    for path in target.rglob("*"):
        if path.suffix not in {".md", ".mmd", ".yaml", ".yml"}:
            continue
        text = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace('"' + old + '"', json.dumps(new, ensure_ascii=False))
            text = text.replace(old, new)
        if path.name in {"feature-charter.md", "council-review.md"}:
            text = re.sub(
                r'^selected_roles:\s*\[.*?\]\s*$',
                f"selected_roles: [{role_list}]",
                text,
                flags=re.MULTILINE,
            )
        path.write_text(text, encoding="utf-8")


def reserve_package(root: Path, feature: str) -> tuple[Path, int]:
    title = feature.strip()
    if not title or title in {'.', '..'} or any(c in title for c in '/\\:') or any(ord(c) < 32 or ord(c) == 127 for c in title):
        raise ValueError("Название пакета должно быть непустым, без разделителей пути и управляющих символов")
    title = re.sub(r' +', ' ', title)
    if len(title.encode('utf-8')) > 220:
        raise ValueError("Название пакета слишком длинное; используй короткое описание")
    root.mkdir(parents=True, exist_ok=True)
    # This file is both the lock and the high-water mark. Never reuse a deleted number.
    with (root / '.package-sequence').open('a+', encoding='utf-8') as sequence:
        fcntl.flock(sequence.fileno(), fcntl.LOCK_EX)
        sequence.seek(0)
        recorded = sequence.read().strip()
        if recorded and not recorded.isdecimal():
            raise ValueError("Повреждён .package-sequence; проверь счётчик перед созданием пакета")
        numbers = [int(recorded or '0')]
        for path in root.iterdir():
            match = re.match(r'^(\d{3,})\s*[—_-]', path.name)
            if match:
                numbers.append(int(match[1]))
        number = max(numbers) + 1
        target = root / f'{number:03d} — {title}'
        target.mkdir()
        sequence.seek(0); sequence.truncate(); sequence.write(str(number) + '\n'); sequence.flush()
    return target, number


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, nargs='?', help="Явный путь для совместимости; без него создаётся пронумерованный пакет")
    parser.add_argument("--package-root", type=Path, help="Общий каталог пакетов; по умолчанию ./architecture")
    parser.add_argument("--level", choices=("L1", "L2", "L3"), required=True)
    parser.add_argument("--context", choices=("greenfield", "brownfield"), required=True)
    parser.add_argument("--language", required=True, help="Код языка, например ru или en")
    parser.add_argument("--feature", required=True, help="Название фичи на языке пользователя")
    parser.add_argument("--slug", help="Необязательный технический ID; не используется в видимом имени пакета")
    parser.add_argument("--revision", default="architecture-v1")
    parser.add_argument("--roles", help="Role IDs через запятую")
    args = parser.parse_args()
    if args.target is not None and args.package_root is not None:
        parser.error("target и --package-root нельзя использовать вместе")

    try:
        roles = parse_roles(args.roles)
        roles = sorted(set(roles) | mandatory_roles(args.level, args.context))
        paths = required_paths(args.level, args.context, roles)
    except (ValueError, FileNotFoundError) as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        return 2

    number = None
    try:
        if args.target is None:
            target, number = reserve_package((args.package_root or Path('architecture')).resolve(), args.feature)
        else:
            target = args.target.resolve()
    except (OSError, ValueError) as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        return 2
    if target.exists() and not target.is_dir():
        print(f"[ERROR] Target существует и не является каталогом: {target}", file=sys.stderr)
        return 2
    if target.exists() and any(target.iterdir()):
        print(f"[ERROR] Target не пуст; существующий пакет не перезаписан: {target}", file=sys.stderr)
        return 2

    target.mkdir(parents=True, exist_ok=True)
    try:
        (target / "adr").mkdir(exist_ok=True)
        for relative in paths:
            copy_file(source_for(relative), target / relative)
        substitute_known_values(
            target,
            feature=args.feature,
            slug=args.slug or (f'package-{number:03d}' if number is not None else target.name),
            language=args.language,
            level=args.level,
            context=args.context,
            revision=args.revision,
            roles=roles,
        )
        if number is not None:
            for name in ('README.md',):
                path = target / name
                text = path.read_text()
                text = text.replace('---\n', f'---\npackage_number: {number}\npackage_name: {json.dumps(target.name, ensure_ascii=False)}\n', 1)
                text = text.replace(f'# {args.feature}\n', f'# {target.name}\n', 1)
                path.write_text(text)
    except (OSError, ValueError) as error:
        print(f"[ERROR] Не удалось создать пакет: {error}", file=sys.stderr)
        return 2

    validator = SKILL_ROOT / "scripts" / "validate_package.py"
    role_arg = f" --roles {','.join(roles)}" if roles else ""
    print(f"Architecture Package создан: {target}")
    print(f"Уровень/контекст: {args.level}/{args.context}; язык: {args.language}")
    print(f"Выбранные роли: {', '.join(roles) if roles else 'нет дополнительных ролей'}")
    print("Следующий шаг: заполнить секции пакета по Protocol v1.5.1.")
    print(
        "Проверка шаблона: "
        f"python3 {shlex.quote(str(validator))} {shlex.quote(str(target))} --level {args.level} "
        f"--context {args.context} --language {args.language}{role_arg} "
        "--template-mode"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
