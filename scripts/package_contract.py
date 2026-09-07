"""Language-neutral, cross-artifact structural contracts for Architecture Council."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

PLACEHOLDER_RE = re.compile(r"\{\{[^{}]+\}\}")
LINK_RE = re.compile(r"\[[^\]]*\]\((<[^>]+>|[^)]+)\)")
CORE_ROLES = {"intake_requirements", "domain_architect", "solution_architect", "implementation_maintainability", "arbiter"}
KNOWN_ROLES = CORE_ROLES | {"system_discovery", "solution_space_challenger", "alternative_architect", "red_team", "security_privacy", "performance_reliability", "data_consistency", "operations_observability", "verification_strategist", "evolution_integration"}
RECOMMENDATIONS = {"ACCEPTED", "ACCEPTED_WITH_CONDITIONS", "REWORK_REQUIRED", "REJECTED", "BLOCKED", "ESCALATED"}
HUMAN_STATUSES = {"AWAITING_HUMAN_REVIEW", "CHANGES_REQUESTED", "APPROVED", "REJECTED", "ON_HOLD"}
MATURITIES = {"DESIGN_CANDIDATE", "EVIDENCE_AUTHORIZED", "IMPLEMENTATION_READY", "NOT_READY"}
README_MARKERS = ("summary", "overview", "reading", "documents", "adrs", "interpretation", "next", "implementation")
REQ_PATTERN = r"(?:BR|FR|QA(?:-[A-Z]+)?|INV|CON|TR)-\d{3,}"


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---[ \t]*\n(.*?)\n---(?:\n|$)", text, re.S)
    result = {}
    if match:
        for line in match[1].splitlines():
            pair = re.match(r"^([\w]+):[ \t]*(.*?)\s*$", line)
            if pair:
                value = pair[2]
                if value.startswith('"'):
                    try:
                        value = json.loads(value)
                    except json.JSONDecodeError:
                        value = value.strip('"')
                else:
                    value = value.strip("'")
                result[pair[1]] = str(value)
    return result


def text_at(package: Path, name: str) -> str:
    path = package / name
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def useful(value: str) -> bool:
    return bool(value.strip()) and value.strip().casefold() not in {"tbd", "pending", "none", "—", "-"} and not PLACEHOLDER_RE.search(value)


def mandatory_roles(level: str, context: str) -> set[str]:
    roles = set(CORE_ROLES)
    if level in {"L2", "L3"}:
        roles |= {"solution_space_challenger", "red_team"}
        if context == "brownfield":
            roles.add("system_discovery")
    if level == "L3":
        roles.add("security_privacy")
    return roles


def roles_value(value: str) -> set[str]:
    return {part.strip().strip('"\'') for part in value.strip("[]").split(",") if part.strip() and not PLACEHOLDER_RE.search(part)}


def selected_roles(package: Path, cli_roles=None) -> set[str]:
    # CLI can add a role, never erase requirements recorded in the package.
    stored = roles_value(frontmatter(text_at(package, "process-ledger.md")).get("selected_roles", ""))
    return stored | roles_value(cli_roles or "")


def without_code(text: str) -> str:
    return re.sub(r"^\s*(```|~~~).*?^\s*\1\s*$", "", text, flags=re.S | re.M)


def cells(line: str) -> list[str]:
    return [part.strip().replace(r"\|", "|") for part in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def table(text: str, marker: str) -> list[list[str]]:
    """Read first table after a stable marker, excluding the localized header."""
    token = f"<!-- {marker} -->"
    if text.count(token) != 1:
        return []
    lines = text.split(token, 1)[1].splitlines()
    started = False
    rows = []
    for line in lines:
        if line.lstrip().startswith("|"):
            started = True
            if re.fullmatch(r"\|[\s:|\-]+\|", line.strip()):
                continue
            rows.append(cells(line))
        elif started or line.startswith("<!-- AC:"):
            break
    return rows[1:]


def heading_ids(text: str, pattern: str) -> set[str]:
    return {m[1] for m in re.finditer(r"^#{1,6}\s+[^\n]*?\b(" + pattern + r")\b", without_code(text), re.M)}


def markdown_anchors(text: str) -> set[str]:
    text = without_code(text)
    anchors = set(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)["\']', text))
    occurrences = defaultdict(int)
    for title in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
        title = re.sub(r"<!--.*?-->", "", title).strip()
        title = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", title)
        title = re.sub(r"<[^>]*>", "", title).casefold()
        slug = re.sub(r"[^\w\- ]", "", title).replace(" ", "-")
        n = occurrences[slug]
        anchors.add(slug if n == 0 else f"{slug}-{n}")
        occurrences[slug] += 1
    return anchors


def resolve_link(source: Path, raw: str) -> tuple[Path, str, tuple[int, int] | None]:
    target = unquote(raw.strip().strip("<>"))
    path, _, fragment = target.partition("#")
    line_range = None
    suffix = re.search(r":(\d+)(?:[-:](\d+))?$", path)
    if suffix:
        line_range = (int(suffix[1]), int(suffix[2] or suffix[1]))
        path = path[:suffix.start()]
    elif re.fullmatch(r"L\d+(?:-L?\d+)?", fragment):
        nums = [int(x) for x in re.findall(r"\d+", fragment)]
        line_range = (nums[0], nums[-1])
        fragment = ""
    return ((source.parent / path).resolve() if path else source.resolve(), fragment, line_range)


def link_errors(source: Path, raw: str) -> list[str]:
    target = raw.strip().strip("<>")
    if re.match(r"^[A-Za-z][\w+.-]*://", target) or target.startswith(("mailto:", "data:")):
        return []  # Remote URLs are not fetched by this local validator.
    path, fragment, bounds = resolve_link(source, raw)
    if not path.exists():
        return [f"Неразрешимая ссылка: {raw}"]
    if bounds:
        if not path.is_file() or bounds[0] < 1 or bounds[1] < bounds[0] or bounds[1] > len(path.read_text(encoding="utf-8", errors="replace").splitlines()):
            return [f"Несуществующий диапазон строк: {raw}"]
    if fragment and path.is_file() and path.suffix == ".md":
        if fragment not in markdown_anchors(path.read_text(encoding="utf-8")):
            return [f"Несуществующий раздел: {raw}"]
    return []


def check_links(package, report, template_mode, allow_missing_render):
    for path in package.rglob("*.md"):
        for raw in LINK_RE.findall(without_code(path.read_text(encoding="utf-8"))):
            if template_mode and PLACEHOLDER_RE.search(raw):
                continue
            if (template_mode or allow_missing_render) and "diagrams/rendered/" in raw:
                continue
            for error in link_errors(path, raw):
                report.error(f"{path.relative_to(package)}: {error}")


def check_readme(package, language, report, template_mode):
    text = text_at(package, "README.md")
    for marker in README_MARKERS:
        if text.count(f"<!-- AC:README:{marker} -->") != 1:
            report.error(f"README: отсутствует уникальный marker AC:README:{marker}")
    if template_mode:
        return
    meta = frontmatter(text)
    if meta.get("artifact_language") != language:
        report.error("README: artifact_language не совпадает с --language")
    if meta.get("implementation_start") != "NOT_REQUESTED":
        report.error("README: implementation_start должен быть NOT_REQUESTED")
    if meta.get("diagnostics_mode") not in {"NORMAL", "VERBOSE"}:
        report.error("README: diagnostics_mode должен быть NORMAL или VERBOSE")


def is_na(value: str) -> bool:
    if not value.startswith("N/A;"):
        return False
    parts = dict(re.findall(r"(?:^|;)\s*(reason|owner)=([^;]+)", value))
    return all(useful(parts.get(key, "")) for key in ("reason", "owner"))


def check_traceability(package, report, template_mode=False):
    req_text = text_at(package, "requirements.md")
    if "<!-- AC:TRACEABILITY -->" not in req_text:
        report.error("Requirements: отсутствует marker AC:TRACEABILITY")
    if template_mode:
        return
    definitions = heading_ids(req_text, REQ_PATTERN)
    if not definitions:
        report.error("Requirements: отсутствуют определения требований")
    rows = table(req_text, "AC:TRACEABILITY")
    br_ids = {x for x in definitions if x.startswith("BR-")}
    scenarios = heading_ids(text_at(package, "feature-charter.md"), r"SCN-\d{3,}")
    increments = heading_ids(text_at(package, "delivery-plan.md"), r"INC-\d{3,}")
    verification_text = text_at(package, "verification-plan.md")
    ver_rows = table(verification_text, "AC:VERIFICATIONS")
    ver_ids = {r[0] for r in ver_rows if r and re.fullmatch(r"VER-\d{3,}", r[0])}
    signal_ids = {r[0] for r in table(verification_text, "AC:SIGNALS") if r and re.fullmatch(r"SIG-\d{3,}", r[0])}
    adrs = {frontmatter(p.read_text()).get("id", "") for p in (package / "adr").glob("*.md")
            if frontmatter(p.read_text()).get("status") not in {"SUPERSEDED", "REJECTED"}}
    observed = set()
    for row in rows:
        if len(row) != 7:
            report.error("Traceability: ожидается 7 колонок")
            continue
        business, req, scenario, arch, inc, ver, signal = row
        observed.add(req)
        if req not in definitions:
            report.error(f"Traceability: неизвестное требование {req}")
        for i, value in enumerate(row):
            if not useful(value):
                report.error(f"Traceability {req}: пустое обязательное звено {i + 1}")
            if value.startswith("N/A") and (i == 1 or not is_na(value)):
                report.error(f"Traceability {req}: N/A требует reason и owner")
        for label, value, known in (("BR", business, br_ids), ("SCN", scenario, scenarios), ("INC", inc, increments), ("VER", ver, ver_ids), ("SIG", signal, signal_ids)):
            if is_na(value):
                continue
            refs = set(re.findall(r"\b" + label + r"-\d{3,}\b", value))
            if not refs or refs - known:
                report.error(f"Traceability {req}: неизвестная связь {label}: {value}")
        if not is_na(arch):
            links = LINK_RE.findall(arch)
            ids = set(re.findall(r"\bADR-\d{3,}\b", arch))
            if not links and (not ids or ids - adrs):
                report.error(f"Traceability {req}: отсутствует разрешимая архитектура/ADR")
            for link in links:
                path, _, _ = resolve_link(package / "requirements.md", link)
                if path != (package / "target-architecture.md").resolve() and path.parent != (package / "adr").resolve():
                    report.error(f"Traceability {req}: architecture link должен вести к Target или ADR")
                if path.parent == (package / "adr").resolve() and path.is_file():
                    adr_meta = frontmatter(path.read_text())
                    current_revision = frontmatter(text_at(package, "README.md")).get("architecture_revision")
                    if adr_meta.get("status") in {"SUPERSEDED", "REJECTED"} or adr_meta.get("architecture_revision") != current_revision:
                        report.error(f"Traceability {req}: ссылка ведёт к неактуальному ADR")
                for error in link_errors(package / "requirements.md", link):
                    report.error(error)
        if not is_na(ver):
            for vid in re.findall(r"\bVER-\d{3,}\b", ver):
                if not any(r[0] == vid and req in re.findall(REQ_PATTERN, r[1]) for r in ver_rows if len(r) >= 2):
                    report.error(f"Traceability {req}: {vid} не проверяет это требование")
    for req in sorted(definitions - observed):
        report.error(f"Traceability: потеряно требование {req}")


def role_runs(package):
    return table(text_at(package, "process-ledger.md"), "AC:ROLE_RUNS")


def output_path(package, value):
    links = LINK_RE.findall(value)
    raw = links[0] if len(links) == 1 else value.strip('`')
    if re.match(r"^[A-Za-z][\w+.-]*://", raw):
        return None
    path, _, _ = resolve_link(package / "process-ledger.md", raw)
    return path if path.is_relative_to(package.resolve()) and path.is_file() else None


def waiver_for(package, actor, roles, revision, report):
    for row in table(text_at(package, "process-ledger.md"), "AC:WAIVERS"):
        if len(row) != 7:
            continue
        wid, wa, wr, rev, person, stamp, evidence = row
        if wa != actor or roles_value(wr) != roles or rev != revision:
            continue
        path = output_path(package, evidence)
        try:
            datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        except ValueError:
            continue
        if not useful(wid) or not useful(person) or path is None:
            continue
        meta = frontmatter(path.read_text())
        if (meta.get("status") == "APPROVED" and meta.get("architecture_revision") == revision
                and meta.get("approved_by") == person and meta.get("approved_at") == stamp):
            report.warn(f"WAIVED {wid}: {actor}, {', '.join(sorted(roles))}; человеческое evidence требует ручной проверки")
            return True
    return False


def check_roles(package, roles, report, template_mode):
    if template_mode:
        return
    readme = frontmatter(text_at(package, "README.md"))
    revision = readme.get("architecture_revision", "")
    rows = role_runs(package)
    latest = {}
    actors = defaultdict(set)
    ids = set()
    for row in rows:
        if len(row) != 9 or not all(useful(x) for x in row):
            report.error("Process Ledger: неполная запись Role Runs (9 обязательных колонок)")
            continue
        run, stage, role, actor, input_rev, output, gate, started, completed = row
        if run in ids:
            report.error(f"Role Runs: повторный run_id {run}")
        ids.add(run)
        if role not in KNOWN_ROLES:
            report.error(f"Role Runs: неизвестная роль {role}")
        actors[actor].add(role)
        latest[role] = row
        try:
            start = datetime.fromisoformat(started.replace("Z", "+00:00"))
            end = datetime.fromisoformat(completed.replace("Z", "+00:00"))
            if start.tzinfo is None or end.tzinfo is None or end < start:
                raise ValueError()
        except (ValueError, TypeError):
            report.error(f"Role Runs {run}: неверные Started/Completed")
    coverage = {row[0]: row for row in table(text_at(package, "process-ledger.md"), "AC:ROLE_COVERAGE") if row}
    for role in sorted(roles):
        if role not in latest:
            report.gate(f"Для выбранной роли нет завершённого запуска: {role}")
            continue
        run = latest[role]
        if run[6] != "PASS":
            report.error(f"Role Runs {run[0]}: последний результат должен быть PASS")
        path = output_path(package, run[5])
        if path is None or not useful(re.sub(r"\A---.*?\n---", "", path.read_text(), count=1, flags=re.S)):
            report.error(f"Role Runs {run[0]}: отсутствует непустой output")
        else:
            meta = frontmatter(path.read_text())
            if meta.get("architecture_revision", meta.get("revision")) != revision:
                report.error(f"Role Runs {run[0]}: output относится к другой revision")
            if role in {"arbiter", "red_team", "alternative_architect"} or path.parent.name == "specialist-reviews":
                for key, value in (("run_id", run[0]), ("actor_id", run[3]), ("input_revision", run[4])):
                    if meta.get(key) != value:
                        report.error(f"Role Runs {run[0]}: {key} output не совпадает с ledger")
        covered = coverage.get(role, [])
        if len(covered) != 6 or covered[-1] != "COMPLETE" or output_path(package, covered[1]) != path or path is None:
            report.error(f"Role Coverage {role}: нужен COMPLETE с тем же output")
    for actor, actor_roles in actors.items():
        conflict = (("arbiter" in actor_roles or "red_team" in actor_roles) and len(actor_roles) > 1
                    or {"solution_architect", "alternative_architect"} <= actor_roles
                    or {"solution_architect", "solution_space_challenger"} <= actor_roles)
        if conflict and not waiver_for(package, actor, actor_roles, revision, report):
            report.error(f"Actor {actor}: несовместимые роли {sorted(actor_roles)} без действующего waiver")


def check_solution_space_coverage(package, level, report, template_mode):
    if level == "L1":
        return
    text = text_at(package, "evidence/architecture-options.md")
    for marker in ("SSC:MAP", "SSC:FAMILIES", "SSC:CHALLENGE", "SSC:GATE"):
        if text.count(f"<!-- {marker} -->") != 1:
            report.error(f"Architecture Options: отсутствует уникальный marker {marker}")
    if template_mode:
        return
    meta = frontmatter(text)
    if meta.get("solution_space_coverage") != "PASS":
        report.gate("Solution Space Coverage Gate должен иметь PASS до арбитража")
    if meta.get("missed_solution_family_status") not in {"NONE", "REWORKED"}:
        report.gate("Открытый MISSED_SOLUTION_FAMILY блокирует арбитраж")
    matches = [row for row in role_runs(package) if len(row) == 9 and row[0] == meta.get("coverage_challenger_run_id")]
    if len(matches) != 1 or matches[0][2] != "solution_space_challenger" or matches[0][6] != "PASS":
        report.gate("Coverage: нет завершённого Solution Space Challenger run")
    elif (meta.get("coverage_challenger_actor_id") != matches[0][3]
          or meta.get("coverage_input_revision") != matches[0][4]
          or output_path(package, matches[0][5]) != (package / "evidence/architecture-options.md").resolve()):
        report.error("Coverage: actor/input/output не совпадают с challenger run")
    families = table(text, "SSC:FAMILIES")
    if not families or any(len(row) != 6 or not all(useful(x) for x in row) for row in families):
        report.error("Coverage: нужны заполненные строки семейств (6 колонок)")
    if not table(text, "AC:OPTIONS"):
        report.error("Coverage: отсутствуют варианты AC:OPTIONS")
    elif not any(len(row) >= 3 and row[2] == "VIABLE" for row in table(text, "AC:OPTIONS")):
        report.gate("Coverage: нет VIABLE кандидата; используй draft для незавершённого evidence")


def check_status_consistency(package, report, template_mode):
    if template_mode:
        return
    readme = frontmatter(text_at(package, "README.md"))
    revision = readme.get("architecture_revision", "")
    if not useful(revision):
        report.error("README: отсутствует architecture_revision")
    for key, choices in (("council_recommendation", RECOMMENDATIONS), ("human_review_status", HUMAN_STATUSES), ("design_maturity", MATURITIES)):
        if readme.get(key) not in choices:
            report.error(f"README: неизвестное значение {key}")
    for path in sorted(package.glob("*.md")) + sorted((package / "adr").glob("*.md")):
        if ".template." in path.name or path.name.endswith("-template.md"):
            continue
        meta = frontmatter(path.read_text())
        if path.parent.name == "adr" and meta.get("status") in {"SUPERSEDED", "REJECTED"}:
            continue
        actual = meta.get("architecture_revision", meta.get("revision"))
        if actual != revision:
            report.error(f"{path.relative_to(package)}: architecture_revision не совпадает с {revision}")
        if "revision" in meta and meta["revision"] != revision:
            report.error(f"{path.name}: конфликт revision и architecture_revision")
        for key in ("council_recommendation", "human_review_status", "design_maturity"):
            required = path.parent == package and (path.name in {"README.md", "decision-brief.md", "final-decision.md"} or key == "human_review_status" and path.name == "implementation-handoff.md")
            if (required or key in meta) and meta.get(key) != readme.get(key):
                report.error(f"{path.name}: не совпадает {key}")
        if path.name == "human-review.md" and meta.get("status") != readme.get("human_review_status"):
            report.error("human-review.md: не совпадает human review status")
        if path.parent == package and path.name in {"README.md", "final-decision.md", "implementation-handoff.md"} and meta.get("implementation_start") != "NOT_REQUESTED":
            report.error(f"{path.name}: implementation_start должен быть NOT_REQUESTED")
    for path in (package / "evidence").rglob("*.md"):
        meta = frontmatter(path.read_text())
        if meta.get("status") == "SUPERSEDED" or path.name in {"process-log.md", "README.md"} or ".template." in path.name:
            continue
        if meta.get("architecture_revision") != revision:
            report.error(f"{path.relative_to(package)}: активный evidence относится к другой revision")
        for field in ("subject_revision",):
            if field in meta and meta[field] != revision:
                report.error(f"{path.name}: не совпадает {field}")


def classification_digest(package):
    digest = hashlib.sha256()
    for name in ("feature-charter.md", "requirements.md", "current-system.md", "system-context.md"):
        path = package / name
        if path.is_file():
            digest.update(name.encode() + b"\0" + path.read_bytes() + b"\0")
    return digest.hexdigest()


def check_classification(package, level, context, roles, report, template_mode):
    if template_mode:
        return
    meta = frontmatter(text_at(package, "feature-classification.md"))
    if meta.get("level") != level or meta.get("context") != context:
        report.error("Classification: --level/--context не совпадают с документом")
    if meta.get("classification_basis_sha256") != classification_digest(package):
        report.error("Classification устарела: пересмотри риски/роли и выполни record_classification.py")
    for role in roles - KNOWN_ROLES:
        report.error(f"Неизвестная выбранная роль: {role}")
    for role in mandatory_roles(level, context) - roles:
        report.error(f"Отсутствует обязательная роль профиля: {role}")
    recorded = roles_value(meta.get("selected_roles", ""))
    if recorded != roles:
        report.error("Classification selected_roles не совпадают с ledger/CLI")


def mermaid_blocks(text):
    """Read fenced blocks, ignoring Mermaid examples inside other code fences."""
    fence = None
    body = []
    for number, line in enumerate(text.splitlines(), 1):
        if fence is None:
            match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
            if match:
                fence, language, start = match[1], match[2].strip(), number
                body = []
        elif re.fullmatch(r" {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*", line):
            if language == "mermaid":
                yield start, "\n".join(body), True
            fence = None
        else:
            body.append(line)
    if fence is not None and language == "mermaid":
        yield start, "\n".join(body), False


def check_diagrams(package, report, allow_missing_render=False, context="greenfield"):
    revision = frontmatter(text_at(package, "README.md")).get("architecture_revision")
    sources = [(path, 0, path.read_text(), True) for path in package.glob("diagrams/**/*.mmd")]
    for path in package.rglob("*.md"):
        sources.extend((path, line, body, closed) for line, body, closed in mermaid_blocks(path.read_text()))
    found = set()
    for path, line, text, closed in sources:
        location = str(path.relative_to(package)) + (f":{line}" if line else "")
        if not closed:
            report.error(f"{location}: незакрытый блок mermaid")
        fields = dict(re.findall(r"^\s*%%\s+ac_(\w+):\s*(.+)$", text, re.M))
        content = [s.strip() for s in text.splitlines() if s.strip() and not s.lstrip().startswith("%%")]
        if not content:
            report.error(f"{location}: пустая схема mermaid")
        if fields.get("kind") == "research":
            if not path.relative_to(package).parts[0] == "evidence":
                report.error(f"{location}: ac_kind research разрешён только в evidence; обязательные схемы остаются нормативными")
            elif fields.get("id") or fields.get("normative"):
                report.error(f"{location}: исследовательская схема не должна объявлять ac_id или ac_normative")
            continue
        if fields.get("kind") not in (None, "normative"):
            report.error(f"{location}: неизвестный ac_kind {fields['kind']}")
        required = ("state", "purpose", "scope", "legend", "revision", "normative") + (("id",) if line else ())
        missing = ["ac_" + field for field in required if not fields.get(field)]
        if missing:
            report.error(f"{location}: нет metadata {', '.join(missing)}")
        if line and fields.get("id"):
            key = (str(path.relative_to(package)), fields["id"])
            if key in found:
                report.error(f"{location}: повторный ac_id {fields['id']}")
            found.add(key)
        if revision and fields.get("revision") and not PLACEHOLDER_RE.search(revision) and fields["revision"] != revision:
            report.error(f"{location}: revision схемы не совпадает с пакетом")
        ref = fields.get("normative", "")
        if ref and not PLACEHOLDER_RE.search(ref):
            for error in link_errors(path, ref):
                report.error(f"{location}: {error}")
    required = [("target-architecture.md", "target-container", "diagrams/target/container-view.mmd"),
                ("target-architecture.md", "key-flow", "diagrams/target/key-flow-sequence.mmd")]
    if context == "brownfield":
        required.append(("current-system.md", "current-container", "diagrams/current/container-view.mmd"))
    for document, identifier, legacy in required:
        if (document, identifier) not in found and not (package / legacy).is_file():
            report.error(f"{document}: отсутствует обязательная схема {identifier}")


def check_evidence_locations(package, context, report):
    current = frontmatter(text_at(package, "current-system.md"))
    for path in [package / "current-system.md", *(package / "evidence").rglob("*.md")]:
        if not path.is_file():
            continue
        text = path.read_text()
        if "<!-- AC:CODE_EVIDENCE -->" not in text:
            continue
        rows = table(text, "AC:CODE_EVIDENCE")
        meta = frontmatter(text)
        if not rows and meta.get("code_evidence_status") == "NOT_APPLICABLE" and useful(meta.get("code_evidence_reason", "")):
            continue
        root = Path(meta.get("repository_root", current.get("repository_root", "")))
        if not root.is_absolute() or not root.is_dir() or not rows:
            report.error(f"{path.name}: code evidence требует repository_root и записи либо обоснованный NOT_APPLICABLE")
            continue
        for row in rows:
            if len(row) != 5:
                report.error(f"{path.name}: code evidence ожидает 5 колонок")
                continue
            claim, filename, revision, start, end = row
            try:
                relative = Path(filename)
                if relative.is_absolute() or ".." in relative.parts:
                    raise ValueError("нужен repo-relative путь")
                if revision.startswith("WORKTREE:"):
                    source = (root / relative).resolve()
                    if not source.is_relative_to(root.resolve()):
                        raise ValueError("source вне repository_root")
                    raw = source.read_bytes()
                    if hashlib.sha256(raw).hexdigest() != revision.removeprefix("WORKTREE:"):
                        raise ValueError("WORKTREE hash изменился")
                else:
                    if not re.fullmatch(r"[a-f0-9]{40}(?:[a-f0-9]{24})?", revision):
                        raise ValueError("нужен полный commit SHA или WORKTREE:sha256")
                    result = subprocess.run(["git", "-C", str(root), "show", "--no-ext-diff", "--no-textconv", f"{revision}:{filename}"], capture_output=True, timeout=10)
                    if result.returncode:
                        raise ValueError("файл отсутствует на указанной revision")
                    raw = result.stdout
                lo, hi = int(start), int(end)
                if not 1 <= lo <= hi <= len(raw.splitlines()):
                    raise ValueError("несуществующий диапазон строк")
            except (ValueError, OSError, subprocess.TimeoutExpired) as error:
                report.error(f"{path.name} {claim}: {error}")
