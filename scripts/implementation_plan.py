"""Structural checks for the optional implementation task index."""
import re

from package_contract import (LINK_RE, REQ_PATTERN, compact_package, frontmatter, heading_ids,
                              resolve_link, table, text_at, useful)


def ids(value, pattern):
    labels = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', value)
    return set(re.findall(r'\b' + pattern + r'\b', labels))


def check_implementation_plan(package, report, required=False, draft=False, template=False):
    compact = compact_package(package)
    path = package / ('implementation-plan.md' if compact else 'implementation-tasks.md')
    handoff = package / 'implementation-handoff.md'
    if not path.is_file():
        if required:
            report.error(f'Implementation plan: отсутствует {path.name}')
            if not compact and not handoff.is_file():
                report.error('Implementation plan: отсутствует implementation-handoff.md')
        return
    if not compact and not handoff.is_file():
        report.error('Implementation plan: отсутствует implementation-handoff.md')
    text = path.read_text()
    if text.count('<!-- AC:IMPLEMENTATION_TASKS -->') != 1:
        report.error('Implementation plan: нужен один AC:IMPLEMENTATION_TASKS')
    if template or draft:
        return
    meta = frontmatter(text)
    if not useful(meta.get('code_revision', '')):
        report.error('Implementation plan: отсутствует code_revision')
    for card in (package / 'implementation').rglob('*.md'):
        card_meta = frontmatter(card.read_text())
        for key in ('architecture_revision', 'artifact_language'):
            if card_meta.get(key) != meta.get(key):
                report.error(f'{card.name}: не совпадает {key} индекса задач')
    requirements = heading_ids(text_at(package, 'requirements.md'), REQ_PATTERN)
    increments = heading_ids(text_at(package, 'delivery-plan.md'), r'INC-\d{3,}')
    verifications = {r[0] for r in table(text_at(package, 'verification-plan.md'), 'AC:VERIFICATIONS') if r}
    tasks, covered_req, covered_inc = {}, set(), set()
    for row in table(text, 'AC:IMPLEMENTATION_TASKS'):
        if len(row) != 9:
            report.error('Implementation plan: ожидается 9 колонок')
            continue
        task, inc, req, deps, status, blocker, acceptance, verification, evidence = row
        task_ids = ids(task, r'TASK-\d{3,}')
        if len(task_ids) != 1 or not LINK_RE.search(task):
            report.error('Implementation plan: Task требует ссылку с одним TASK ID')
            continue
        tid = next(iter(task_ids))
        target, _, _ = resolve_link(path, LINK_RE.findall(task)[0])
        try:
            relative = target.relative_to(package.resolve())
            allowed = relative == path.relative_to(package) or bool(relative.parts) and relative.parts[0] == 'implementation'
        except ValueError:
            allowed = False
        if not allowed or not target.is_file() or tid not in heading_ids(target.read_text(), r'TASK-\d{3,}'):
            report.error(f'{tid}: ссылка не ведёт к карточке задачи')
        if tid in tasks:
            report.error(f'{tid}: повторный ID задачи')
        dependencies = ids(deps, r'TASK-\d{3,}')
        if deps not in {'—', '-'} and not dependencies:
            report.error(f'{tid}: неверные Dependencies')
        tasks[tid] = (status, dependencies)
        inc_ids, req_ids = ids(inc, r'INC-\d{3,}'), ids(req, REQ_PATTERN)
        ver_ids = ids(verification, r'VER-\d{3,}')
        if len(inc_ids) != 1 or inc_ids - increments:
            report.error(f'{tid}: неизвестный или неоднозначный INC')
        if not req_ids or req_ids - requirements:
            report.error(f'{tid}: неизвестные Requirements')
        if not ver_ids or ver_ids - verifications:
            report.error(f'{tid}: неизвестная Verification')
        if not useful(acceptance):
            report.error(f'{tid}: отсутствует Acceptance')
        if status not in {'PLANNED', 'READY', 'BLOCKED', 'IN_PROGRESS', 'DONE', 'CANCELLED'}:
            report.error(f'{tid}: неизвестный Status')
        if status in {'BLOCKED', 'CANCELLED'} and not useful(blocker):
            report.error(f'{tid}: отсутствует причина Blocker')
        if status in {'READY', 'IN_PROGRESS'} and blocker not in {'—', '-'}:
            report.error(f'{tid}: готовая задача содержит Blocker')
        if status == 'DONE' and not LINK_RE.search(evidence):
            report.error(f'{tid}: DONE требует Evidence-ссылку')
        if status != 'CANCELLED':
            covered_req |= req_ids
            covered_inc |= inc_ids
    if not tasks:
        report.error('Implementation plan: нет задач')
    for tid, (status, deps) in tasks.items():
        if deps - tasks.keys():
            report.error(f'{tid}: неизвестная зависимость')
        if status in {'READY', 'IN_PROGRESS'} and any(tasks.get(d, ('MISSING',))[0] != 'DONE' for d in deps):
            report.error(f'{tid}: зависимости ещё не DONE')
    # Kahn traversal detects self-dependencies and cycles without recursion limits.
    remaining = {tid: deps & tasks.keys() for tid, (_, deps) in tasks.items()}
    while remaining:
        ready = {tid for tid, deps in remaining.items() if not deps}
        if not ready:
            report.error('Implementation plan: цикл зависимостей')
            break
        remaining = {tid: deps - ready for tid, deps in remaining.items() if tid not in ready}
    if requirements - covered_req:
        report.error('Implementation plan: потеряны требования ' + ', '.join(sorted(requirements - covered_req)))
    if increments - covered_inc:
        report.error('Implementation plan: потеряны инкременты ' + ', '.join(sorted(increments - covered_inc)))
