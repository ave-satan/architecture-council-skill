"""Contract regressions through public CLI and real on-disk architecture packages."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import shlex
from concurrent.futures import ThreadPoolExecutor
import tempfile
import unittest
from pathlib import Path

from package_fixture import complete_package, run, set_meta, STAMP, SCRIPTS


class NumberedPackageCLI(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='council-names-', dir='/private/tmp')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'architecture'

    def create(self, title='Синхронизация календаря', *extra):
        return run('init_feature_package.py', '--package-root', self.root, '--level', 'L2',
                   '--context', 'greenfield', '--language', 'ru', '--feature', title, *extra)

    def test_numbered_name_and_quoted_validation_command(self):
        result = self.create('Календарь «Работа»', '--verbose')
        self.assertEqual(0, result.returncode, result.stderr)
        path = self.root / '001 — Календарь «Работа»'
        text = (path / 'README.md').read_text()
        self.assertIn('package_number: 1', text)
        self.assertIn('# 001 — Календарь «Работа»', text)
        self.assertIn('# 001 — Календарь «Работа»', (path / 'decision-brief.md').read_text())
        command = shlex.split(result.stdout.split('Проверка шаблона: ', 1)[1])
        self.assertIn(str(path), command)
        check = subprocess.run([sys.executable, *command[1:]], capture_output=True, text=True)
        self.assertEqual(0, check.returncode, check.stdout + check.stderr)

    def test_existing_numbers_and_deleted_package_are_not_reused(self):
        (self.root / '008 — Старая задача').mkdir(parents=True)
        self.assertEqual(0, self.create().returncode)
        shutil.rmtree(self.root / '009 — Синхронизация календаря')
        self.assertEqual(0, self.create().returncode)
        self.assertTrue((self.root / '010 — Синхронизация календаря').is_dir())

    def test_concurrent_creation_gets_distinct_numbers(self):
        with ThreadPoolExecutor(max_workers=3) as pool:
            results = list(pool.map(lambda _: self.create(), range(3)))
        for result in results:
            self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual({'001', '002', '003'}, {p.name[:3] for p in self.root.iterdir() if p.is_dir()})

    def test_invalid_title_and_corrupt_counter_do_not_create_packages(self):
        for title in ('', '../escape', 'Новый/пакет', 'Новый\nпакет'):
            self.assertEqual(2, self.create(title).returncode)
        self.assertFalse(self.root.exists())
        self.root.mkdir(); (self.root / '.package-sequence').write_text('broken')
        self.assertEqual(2, self.create().returncode)
        self.assertEqual(['.package-sequence'], [p.name for p in self.root.iterdir()])

    def test_default_root_is_architecture_in_current_project(self):
        result = subprocess.run([sys.executable, str(SCRIPTS / 'init_feature_package.py'), '--level', 'L1',
                                 '--context', 'greenfield', '--language', 'ru', '--feature', 'Импорт встреч'],
                                cwd=self.temp.name, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((self.root / '001 — Импорт встреч' / 'README.md').is_file())


class PackageCLI(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="council-regression-", dir="/private/tmp")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.package = self.root / "package"
        self.roles = complete_package(self.package)

    def validate(self, *extra, package=None, level="L2", context="greenfield", language="en"):
        return run("validate_package.py", package or self.package, "--level", level, "--context", context,
                   "--language", language, "--allow-missing-render", *extra)

    def assertRejected(self, result, text):
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(text, result.stdout)

    def replace(self, name, old, new):
        path = self.package / name
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new))

    def stamp(self):
        result = run("record_classification.py", self.package)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_completed_profiles_accept_real_links_and_outputs(self):
        for level in ("L1", "L2", "L3"):
            for context in ("greenfield", "brownfield"):
                with self.subTest(level=level, context=context):
                    package = self.root / f"{level}-{context}"
                    complete_package(package, level=level, context=context)
                    result = self.validate(package=package, level=level, context=context)
                    self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                    self.assertIn("errors=0, warnings=0", result.stdout)

    def test_empty_traceability_cannot_drop_a_requirement(self):
        path = self.package / "requirements.md"
        path.write_text("\n".join(line for line in path.read_text().splitlines() if not line.startswith("| BR-001 |")) + "\n")
        self.stamp()
        self.assertRejected(self.validate(), "потеряно требование FR-001")

    def test_traceability_references_must_exist(self):
        path = self.package / "requirements.md"
        original = path.read_text()
        for before, after, error in [("INC-001", "INC-999", "неизвестная связь INC"),
                                     ("VER-001", "VER-999", "неизвестная связь VER"),
                                     ("SIG-001", "SIG-999", "неизвестная связь SIG"),
                                     ("SCN-001", "SCN-999", "неизвестная связь SCN")]:
            with self.subTest(reference=before):
                path.write_text(original.replace(before, after)); self.stamp()
                self.assertRejected(self.validate(), error)
        path.write_text(original)

    def test_verification_must_cover_the_linked_requirement(self):
        self.replace("verification-plan.md", "BR-001, FR-001", "BR-001")
        self.assertRejected(self.validate(), "VER-001 не проверяет это требование")

    def test_justified_na_is_supported_but_empty_reason_is_rejected(self):
        self.replace("requirements.md", "| SIG-001 |", "| N/A; reason=User inspects the local result; owner=Maintainer |")
        self.stamp(); self.assertEqual(0, self.validate().returncode)
        self.replace("requirements.md", "reason=User inspects the local result", "reason=")
        self.stamp(); self.assertRejected(self.validate(), "N/A требует reason и owner")

    def test_cli_roles_cannot_hide_recorded_or_mandatory_roles(self):
        set_meta(self.package / "process-ledger.md", selected_roles=["solution_space_challenger"])
        self.assertRejected(self.validate("--roles", "solution_space_challenger"), "Отсутствует обязательная роль профиля")

    def test_unknown_challenger_and_unfinished_role_are_rejected(self):
        set_meta(self.package / "evidence/architecture-options.md", coverage_challenger_run_id="RUN-999")
        self.assertRejected(self.validate(), "нет завершённого Solution Space Challenger")
        self.replace("process-ledger.md", "| PASS |", "| BLOCKED |")
        self.assertRejected(self.validate(), "последний результат должен быть PASS")

    def test_missing_output_and_incomplete_coverage_are_rejected(self):
        (self.package / "evidence/arbiter-review.md").unlink()
        self.assertRejected(self.validate(), "отсутствует непустой output")
        self.replace("process-ledger.md", "| COMPLETE |", "| MISSING |")
        self.assertRejected(self.validate(), "нужен COMPLETE")

    def test_output_identity_must_match_the_completed_run(self):
        set_meta(self.package / "evidence/arbiter-review.md", actor_id="different-actor")
        self.assertRejected(self.validate(), "actor_id output не совпадает")

    def test_open_solution_family_blocks_arbitration(self):
        set_meta(self.package / "evidence/architecture-options.md", missed_solution_family_status="OPEN", solution_space_coverage="REWORK")
        result = self.validate()
        self.assertRejected(result, "MISSED_SOLUTION_FAMILY")
        self.assertIn("должен иметь PASS", result.stdout)

    def test_reworked_family_with_real_challenger_passes(self):
        set_meta(self.package / "evidence/architecture-options.md", missed_solution_family_status="REWORKED")
        self.assertEqual(0, self.validate().returncode)

    def test_target_revision_and_design_maturity_are_checked(self):
        set_meta(self.package / "target-architecture.md", architecture_revision="r0")
        self.assertRejected(self.validate(), "target-architecture.md: architecture_revision")
        set_meta(self.package / "target-architecture.md", architecture_revision="r1")
        set_meta(self.package / "decision-brief.md", design_maturity="NOT_READY")
        self.assertRejected(self.validate(), "не совпадает design_maturity")

    def test_historical_adr_is_retained_without_rewriting_revision(self):
        path = self.package / "adr/ADR-001.md"
        path.write_text('---\nid: ADR-001\narchitecture_revision: r0\nartifact_language: en\nstatus: SUPERSEDED\n---\n# Old design\nReplaced by the current local writer.\n')
        self.assertEqual(0, self.validate().returncode)
        set_meta(path,status="ACCEPTED")
        self.assertRejected(self.validate(), "ADR-001.md: architecture_revision")

    def test_translated_readme_uses_stable_markers(self):
        # The completed fixture uses English headings, not magic Russian phrases.
        self.assertEqual(0, self.validate().returncode)
        self.replace("README.md", "<!-- AC:README:next -->", "")
        self.assertRejected(self.validate(), "AC:README:next")

    def test_changed_requirements_require_reclassification(self):
        path = self.package / "requirements.md"
        path.write_text(path.read_text() + "\nA newly supplied constraint changes the expected export size.\n")
        self.assertRejected(self.validate(), "Classification устарела")
        self.stamp(); self.assertEqual(0, self.validate().returncode)

    def test_l3_upgrade_requires_the_new_core_and_artifacts(self):
        set_meta(self.package / "feature-classification.md", level="L3")
        self.assertRejected(self.validate(level="L3"), "security_privacy")
        self.assertIn("threat-model.md", self.validate(level="L3").stdout)

    def test_current_diagram_revision_is_checked(self):
        self.replace("target-architecture.md", "ac_revision: r1", "ac_revision: r0")
        self.assertRejected(self.validate(), "revision схемы не совпадает")

    def test_inline_mermaid_needs_no_render_or_separate_directory(self):
        self.assertFalse((self.package / 'diagrams').exists())
        result = run('validate_package.py', self.package, '--level', 'L2', '--context', 'greenfield', '--language', 'en')
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn('errors=0, warnings=0', result.stdout)

    def test_missing_empty_unclosed_and_duplicate_mermaid_are_rejected(self):
        p = self.package / 'target-architecture.md'; original = p.read_text()
        changes = [
            (lambda s: s.replace('ac_id: key-flow', 'ac_id: other'), 'отсутствует обязательная схема key-flow'),
            (lambda s: s.replace('ac_id: key-flow', 'ac_id: target-container'), 'повторный ac_id'),
            (lambda s: s.replace('flowchart LR\nDatabase --> CSV', ''), 'пустая схема'),
            (lambda s: s.rsplit('```', 1)[0], 'незакрытый блок'),
            (lambda s: s.replace('ac_normative: target-architecture.md', 'ac_normative: missing.md'), 'missing.md'),
        ]
        for change, diagnostic in changes:
            with self.subTest(diagnostic=diagnostic):
                p.write_text(change(original))
                self.assertRejected(self.validate(), diagnostic)

    def test_research_diagram_is_explicit_and_cannot_replace_required_diagram(self):
        p = self.package / 'evidence/research.md'
        header = '---\narchitecture_revision: r1\nartifact_language: en\n---\n'
        body = '```mermaid\n  %% ac_kind: research\nflowchart LR\nA --> B\n```\n'
        p.write_text(header + body)
        self.assertEqual(0, self.validate().returncode)
        p.write_text(header + body.replace('A --> B', '').replace('flowchart LR', ''))
        self.assertRejected(self.validate(), 'пустая схема')
        p.write_text(header + body.rsplit('```', 1)[0])
        self.assertRejected(self.validate(), 'незакрытый блок')
        p.write_text(header + body)
        target = self.package / 'target-architecture.md'
        target.write_text(re.sub(r'```mermaid\n.*?```', body, target.read_text(), flags=re.S))
        self.assertRejected(self.validate(), 'отсутствует обязательная схема')

    def test_missing_diagram_metadata_has_one_diagnostic_without_revision_cascade(self):
        (self.package / 'evidence/research.md').write_text('---\narchitecture_revision: r1\nartifact_language: en\n---\n```mermaid\nflowchart LR\nA --> B\n```\n')
        result = self.validate()
        self.assertRejected(result, 'нет metadata')
        self.assertIn('errors=1, warnings=0', result.stdout)
        self.assertNotIn('revision схемы не совпадает', result.stdout)

    def test_open_coverage_gate_is_distinct_but_still_fails_review(self):
        set_meta(self.package / 'evidence/architecture-options.md', solution_space_coverage='REWORK')
        result = self.validate()
        self.assertRejected(result, '[ERROR][GATE]')
        self.assertIn('open_gates=1', result.stdout)

    def test_legacy_mermaid_sources_remain_valid_without_renders(self):
        p = self.package / 'target-architecture.md'; text = p.read_text()
        blocks = re.findall(r'```mermaid\n(.*?)```', text, re.S)
        p.write_text(re.sub(r'```mermaid\n.*?```', '', text, flags=re.S))
        folder = self.package / 'diagrams/target'; folder.mkdir(parents=True)
        for name, body in zip(('container-view.mmd', 'key-flow-sequence.mmd'), blocks):
            (folder / name).write_text(body.replace('ac_normative: target-architecture.md', 'ac_normative: ../../target-architecture.md'))
        result = self.validate()
        self.assertEqual(0, result.returncode, result.stdout)

    def test_tilde_fences_and_nested_code_examples(self):
        p = self.package / 'target-architecture.md'
        p.write_text(p.read_text().replace('```', '~~~') + '\n````text\n```mermaid\nNot an actual diagram\n```\n````\n')
        result = self.validate()
        self.assertEqual(0, result.returncode, result.stdout)

    def test_real_anchors_and_line_ranges(self):
        path = self.package / "README.md"
        original = path.read_text()
        for link, valid in [("target-architecture.md#export",True), ("target-architecture.md#missing",False),
                            ("target-architecture.md:1",True), ("target-architecture.md:99999",False)]:
            with self.subTest(link=link):
                path.write_text(original + f"\n[Source]({link})\n")
                result = self.validate()
                self.assertEqual(0 if valid else 1, result.returncode, result.stdout)

    def test_waiver_is_scoped_to_actor_roles_revision_and_approval(self):
        # Same person performs two roles only when an explicit, structurally bound waiver exists.
        self.replace("process-ledger.md", "| actor-5 |", "| actor-3 |")
        set_meta(self.package / "evidence/arbiter-review.md", actor_id="actor-3")
        self.assertRejected(self.validate(), "несовместимые роли")
        path = self.package / "process-ledger.md"
        path.write_text(path.read_text() + f"| WV-001 | actor-3 | solution_architect,arbiter | r1 | Review owner | {STAMP} | [Decision](waiver.md) |\n")
        (self.package / "waiver.md").write_text(f'---\narchitecture_revision: r1\nartifact_language: en\nstatus: APPROVED\napproved_by: Review owner\napproved_at: {STAMP}\n---\n# Synthetic waiver\nThis fixture models the recorded human decision; no real authorization is asserted.\n')
        result = self.validate(); self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn("WAIVED WV-001", result.stdout)
        set_meta(self.package / "waiver.md", architecture_revision="r0")
        self.assertRejected(self.validate(), "несовместимые роли")

    def test_external_url_with_explicit_port_remains_external(self):
        path = self.package / "README.md"
        path.write_text(path.read_text() + "\n[Endpoint](https://example.invalid:8443)\n")
        self.assertEqual(0, self.validate().returncode)

    def test_traceability_cannot_target_a_superseded_adr(self):
        path = self.package / "adr/ADR-001.md"
        path.write_text('---\nid: ADR-001\narchitecture_revision: r0\nartifact_language: en\nstatus: SUPERSEDED\n---\n# Old decision\nHistorical only.\n')
        self.replace("requirements.md", "[Design](target-architecture.md)", "[Old ADR](adr/ADR-001.md)")
        self.stamp()
        self.assertRejected(self.validate(), "неактуальному ADR")

    def test_review_status_mismatch_is_rejected(self):
        set_meta(self.package / "human-review.md", status="APPROVED")
        self.assertRejected(self.validate(), "не совпадает human review status")

    def test_draft_never_reports_handoff_readiness(self):
        p=self.root / "draft"
        run("init_feature_package.py",p,"--level","L1","--context","greenfield","--language","ru","--feature","Черновик","--slug","draft")
        result=self.validate("--phase","draft",package=p,level="L1",language="ru")
        self.assertEqual(0,result.returncode,result.stdout)
        self.assertIn("не PASS готовности",result.stdout)
        self.assertEqual(1,self.validate(package=p,level="L1",language="ru").returncode)

    def test_former_false_pass_combination_is_rejected(self):
        path = self.package / "requirements.md"
        path.write_text("\n".join(line for line in path.read_text().splitlines() if not line.startswith("| BR-001 |")) + "\n")
        self.stamp()
        set_meta(self.package / "target-architecture.md", architecture_revision="r0")
        set_meta(self.package / "evidence/architecture-options.md", coverage_challenger_run_id="RUN-NOT-EXISTS")
        self.replace("process-ledger.md", "| PASS |", "| BLOCKED |")
        result = self.validate()
        self.assertRejected(result, "потеряно требование FR-001")
        self.assertIn("последний результат должен быть PASS", result.stdout)
        self.assertIn("target-architecture.md: architecture_revision", result.stdout)
        self.assertIn("нет завершённого Solution Space Challenger", result.stdout)

    def test_code_evidence_uses_frozen_commit_and_validates_worktree_hash(self):
        repo=self.root/'repo';repo.mkdir()
        def git(*args):
            return subprocess.run(['git','-C',str(repo),*args],text=True,capture_output=True,check=True).stdout.strip()
        git('init','-q')
        source=repo/'example.py';source.write_text('first\nsecond\nthird\n')
        git('add','example.py')
        git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','-c','commit.gpgsign=false','commit','-qm','fixture')
        sha=git('rev-parse','HEAD')
        source.write_text('changed\n')
        evidence=self.package/'evidence/code-source.md'
        prefix=f'---\narchitecture_revision: r1\nartifact_language: en\nrepository_root: {json.dumps(str(repo))}\n---\n# Code evidence\n<!-- AC:CODE_EVIDENCE -->\n| Claim | Path | Revision | Start | End |\n|---|---|---|---|---|\n'
        evidence.write_text(prefix+f'| CLM-001 | example.py | {sha} | 2 | 3 |\n')
        self.assertEqual(0,self.validate().returncode)
        evidence.write_text(prefix+f'| CLM-001 | example.py | {sha} | 2 | 99 |\n')
        self.assertRejected(self.validate(),"несуществующий диапазон")
        digest=hashlib.sha256(source.read_bytes()).hexdigest()
        evidence.write_text(prefix+f'| CLM-001 | example.py | WORKTREE:{digest} | 1 | 1 |\n')
        self.assertEqual(0,self.validate().returncode)
        source.write_text('changed again\n')
        self.assertRejected(self.validate(),"WORKTREE hash изменился")


    def test_adr_navigation_index_needs_no_package_decision(self):
        path = self.package / 'adr/README.md'
        path.write_text('---\narchitecture_revision: r1\nartifact_language: en\n---\n# Decisions\nNo decisions have been accepted.\n')
        result = self.validate()
        self.assertEqual(0, result.returncode, result.stdout)
        set_meta(path, architecture_revision='old')
        self.assertRejected(self.validate(), 'architecture_revision')

    def test_language_ignores_machine_values_but_checks_table_prose(self):
        path = self.package / 'evidence/language-probe.md'
        metadata = '---\narchitecture_revision: r1\nartifact_language: en\n---\n'
        machine = '| RUN-SEC-001 | security_privacy | /root/reviewer | [evidence.md](evidence.md) | ' + 'a' * 64 + ' | 2026-09-06T08:00:00Z |\n'
        path.write_text(metadata + '# Review\n' + ('The evidence is sufficient for this limited review. ' * 30) + '\n' + machine * 30)
        # Use a real local link, so language checks do not hide link errors.
        (self.package / 'evidence/evidence.md').write_text(metadata + '# Evidence\n')
        self.assertEqual(0, self.validate().returncode)
        path.write_text(metadata + machine * 30 + '| ' + 'Проверка подтверждает только описанные ограничения. ' * 60 + ' |\n')
        self.assertRejected(self.validate(), 'language-probe.md выглядит')


    def test_russian_prose_with_large_machine_table_is_not_misclassified(self):
        path = self.package / 'evidence/russian-probe.md'
        metadata = '---\narchitecture_revision: r1\nartifact_language: ru\n---\n'
        machine = '| RUN-SEC-001 | security_privacy | /root/security_review | intake-v1-sha256:' + 'a' * 64 + ' | 2026-09-06T08:00:00Z |\n'
        path.write_text(metadata + ('Проверены фактические ограничения и результаты исследования. ' * 15) + '\n' + machine * 100)
        # Other fixture documents remain English. Inspect this document's CLI diagnostic.
        self.assertNotIn('russian-probe.md выглядит', self.validate(language='ru').stdout)
        path.write_text(metadata + ('The actual constraints and review results have been verified. ' * 30) + '\n' + machine * 100)
        self.assertRejected(self.validate(language='ru'), 'russian-probe.md выглядит')


class LoggerCLI(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='council-log-test-',dir='/private/tmp');self.addCleanup(self.temp.cleanup)
        self.package=Path(self.temp.name)/'package'
        result=run('init_feature_package.py',self.package,'--level','L1','--context','greenfield','--language','ru','--feature','Журнал','--slug','log','--verbose')
        self.assertEqual(0,result.returncode,result.stderr)
        self.jsonl=self.package/'evidence/process-log.jsonl';self.md=self.package/'evidence/process-log.md'

    def append(self,*extra):
        return run('log_event.py',self.package,'--event','gate_evaluated','--status','PASS','--summary','Проверка завершена',*extra)

    def test_artifact_links_resolve_and_jsonl_keeps_original_paths(self):
        from urllib.parse import unquote
        artifact = 'evidence/Замер (календарь).md'
        (self.package / artifact).write_text('# Замер\n')
        result = self.append('--artifact', artifact)
        self.assertEqual(0, result.returncode, result.stderr)
        destinations = re.findall(r'\]\(([^)]+)\)', self.md.read_text())
        self.assertTrue(destinations)
        targets = {(self.md.parent / unquote(raw)).resolve() for raw in destinations}
        self.assertIn((self.package / artifact).resolve(), targets)
        self.assertTrue(all(path.exists() for path in targets))
        self.assertEqual([artifact], json.loads(self.jsonl.read_text().splitlines()[-1])['artifacts'])
        before = self.md.read_bytes()
        rebuilt = run('log_event.py', self.package, '--rebuild-markdown')
        self.assertEqual(0, rebuilt.returncode, rebuilt.stderr)
        self.assertEqual(before, self.md.read_bytes())

    def test_invalid_events_are_rejected_before_either_file_changes(self):
        before=(self.jsonl.read_bytes(),self.md.read_bytes())
        for extra in [('--timestamp','bad-date'),('--timestamp','2026-09-06'),('--event','   '),('--status',' '),('--summary',' '),('--duration-ms','-1'),('--artifact','https://example.invalid/report?api_key=DUMMY_REVIEW_SECRET')]:
            with self.subTest(extra=extra):
                result=self.append(*extra);self.assertEqual(2,result.returncode,result.stdout)
                self.assertEqual(before,(self.jsonl.read_bytes(),self.md.read_bytes()))
                self.assertNotIn('DUMMY_REVIEW_SECRET',result.stderr)

    def test_valid_event_is_projected_with_safe_markdown_cells(self):
        result=self.append('--summary','Проверено | поле\nи <!-- AC:EVENTS:END -->')
        self.assertEqual(0,result.returncode,result.stderr)
        self.assertEqual(2,len(self.jsonl.read_text().splitlines()))
        self.assertIn('&#124;',self.md.read_text())
        result=run('validate_package.py',self.package,'--level','L1','--context','greenfield','--language','ru','--template-mode','--allow-missing-render','--verbose')
        self.assertEqual(0,result.returncode,result.stdout)

    def test_mismatched_projection_is_detected_and_rebuilt_without_append(self):
        before=self.jsonl.read_bytes()
        self.md.write_text(self.md.read_text().replace('| IN_PROGRESS |','| PASS |'))
        result=run('validate_package.py',self.package,'--level','L1','--context','greenfield','--language','ru','--template-mode','--allow-missing-render','--verbose')
        self.assertEqual(1,result.returncode);self.assertIn('не соответствует',result.stdout)
        self.assertEqual(2,self.append().returncode)
        result=run('log_event.py',self.package,'--rebuild-markdown');self.assertEqual(0,result.returncode,result.stderr)
        self.assertEqual(before,self.jsonl.read_bytes())
        self.assertIn('| IN_PROGRESS |',self.md.read_text())

    def test_final_jsonl_line_without_lf_gets_a_separator(self):
        self.jsonl.write_bytes(self.jsonl.read_bytes().rstrip(b"\n"))
        result = self.append()
        self.assertEqual(0, result.returncode, result.stderr)
        events = [json.loads(line) for line in self.jsonl.read_text().splitlines()]
        self.assertEqual([1, 2], [event["sequence"] for event in events])

    def test_role_boundary_requires_identity_before_append(self):
        before = (self.jsonl.read_bytes(), self.md.read_bytes())
        result = self.append('--event', 'role_completed')
        self.assertEqual(2, result.returncode)
        self.assertIn('run_id', result.stderr)
        self.assertEqual(before, (self.jsonl.read_bytes(), self.md.read_bytes()))

    def test_late_role_boundary_keeps_registration_and_observed_time(self):
        before = self.jsonl.read_bytes()
        result = self.append('--event', 'role_completed', '--run-id', 'RUN-SEC-01',
                             '--actor-id', '/root/security', '--role', 'security_privacy',
                             '--input-revision', 'source-r2-hash', '--timestamp', '2026-09-06T08:10:00Z',
                             '--occurred-at', '2026-09-06T08:00:00Z', '--timing-basis', 'Часы в отчёте reviewer')
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue(self.jsonl.read_bytes().startswith(before))
        event = json.loads(self.jsonl.read_text().splitlines()[-1])
        self.assertEqual('2026-09-06T08:10:00Z', event['timestamp'])
        self.assertEqual('2026-09-06T08:00:00Z', event['occurred_at'])
        self.assertIn('RUN-SEC-01', self.md.read_text())
        self.assertIn('source-r2-hash', self.md.read_text())
        self.assertEqual(0, run('log_event.py', self.package, '--rebuild-markdown').returncode)

    def test_invalid_observed_time_never_changes_logs(self):
        before = (self.jsonl.read_bytes(), self.md.read_bytes())
        for extra in [('--occurred-at', 'bad'),
                      ('--occurred-at', '2026-09-06T08:00:00Z'),
                      ('--occurred-at', '2026-09-06T10:00:00Z', '--timing-basis', 'clock')]:
            result = self.append('--timestamp', '2026-09-06T09:00:00Z', *extra)
            self.assertEqual(2, result.returncode)
            self.assertEqual(before, (self.jsonl.read_bytes(), self.md.read_bytes()))

    def test_normal_mode_refuses_logging(self):
        set_meta(self.package/'README.md',diagnostics_mode='NORMAL')
        before=(self.jsonl.read_bytes(),self.md.read_bytes())
        self.assertEqual(2,self.append().returncode)
        self.assertEqual(before,(self.jsonl.read_bytes(),self.md.read_bytes()))

    def test_corrupted_sequence_refuses_additional_append(self):
        self.jsonl.write_text(self.jsonl.read_text().replace('"sequence":1','"sequence":3'))
        before=self.jsonl.read_bytes();self.assertEqual(2,self.append().returncode)
        self.assertEqual(before,self.jsonl.read_bytes())

    def test_missing_verbose_artifact_fails_validation(self):
        (self.package/'evidence/verbose-review.md').unlink()
        result=run('validate_package.py',self.package,'--level','L1','--context','greenfield','--language','ru','--template-mode','--allow-missing-render','--verbose')
        self.assertEqual(1,result.returncode);self.assertIn('Отсутствует VERBOSE',result.stdout)

    def test_nonempty_target_is_never_overwritten(self):
        before=self.jsonl.read_bytes()
        result=run('init_feature_package.py',self.package,'--level','L1','--context','greenfield','--language','ru','--feature','Другое','--slug','other')
        self.assertEqual(2,result.returncode);self.assertEqual(before,self.jsonl.read_bytes())


if __name__ == '__main__':
    unittest.main()
