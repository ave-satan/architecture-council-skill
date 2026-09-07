#!/usr/bin/env python3
"""Record the input digest after the Council has rechecked classification and roles."""
import argparse
import re
from pathlib import Path
from package_contract import classification_digest, frontmatter, mandatory_roles, selected_roles


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    args = parser.parse_args()
    package = args.package.resolve()
    path = package / "feature-classification.md"
    text = path.read_text(encoding="utf-8")
    meta = frontmatter(text)
    level, context = meta.get("level"), meta.get("context")
    if level not in {"L1", "L2", "L3"} or context not in {"greenfield", "brownfield"}:
        parser.error("Сначала заполни level и context в Classification")
    roles = selected_roles(package)
    if mandatory_roles(level, context) - roles:
        parser.error("В ledger отсутствуют обязательные роли нового профиля")
    if not all((package / name).is_file() for name in ("feature-charter.md", "requirements.md", "current-system.md" if context == "brownfield" else "system-context.md")):
        parser.error("Отсутствуют входы классификации")
    import json
    values = {"classification_basis_sha256": classification_digest(package), "selected_roles": json.dumps(sorted(roles))}
    for key, value in values.items():
        line = f"{key}: {value}"
        pattern = rf"^{key}:.*$"
        if re.search(pattern, text, re.M):
            text = re.sub(pattern, lambda _: line, text, count=1, flags=re.M)
        else:
            text = text.replace("---\n", "---\n" + line + "\n", 1)
    path.write_text(text, encoding="utf-8")
    print("Зафиксированы входы Classification. Команда не оценивает риск и не утверждает решение за человека.")


if __name__ == "__main__":
    main()
