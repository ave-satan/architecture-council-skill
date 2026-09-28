"""Audit regressions through the public CLI and isolated sectioned packages."""
import re
import tempfile
import tarfile
import unittest
import zipfile
from pathlib import Path

from package_fixture import complete_compact_package, run, set_meta, STAMP


class AuditRegressionCLI(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="council-audit-", dir="/private/tmp")
        self.addCleanup(self.temp.cleanup)
        self.package = Path(self.temp.name) / "package"
        complete_compact_package(self.package)
        self.council = self.package / "evidence/council-review.md"

    def validate(self, *extra):
        return run("validate_package.py", self.package, "--level", "L2", "--context",
                   "greenfield", "--language", "en", "--allow-missing-render", *extra)

    def assertAccepted(self, result):
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("errors=0, warnings=0", result.stdout)

    def assertRejected(self, result, subject):
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(subject, result.stdout)

    def replace(self, name, old, new):
        path = self.package / name
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1))

    def validation_row(self, row):
        self.replace("evidence/council-review.md", "| r1 | 0 | 0 | None | PASS |", row)

    def restamp(self):
        result = run("record_classification.py", self.package)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def link_evidence(self, name):
        self.council.write_text(self.council.read_text()
                                + f"\n## Retained external evidence\n[Source]({name})\n")

    def implementation_tasks(self, anchor="task-001"):
        path = self.package / "implementation-plan.md"
        path.write_text(f'''---
architecture_revision: r1
artifact_language: en
code_revision: fixture-snapshot-1
implementation_start: NOT_REQUESTED
---
# Implementation plan
The actual user command determines the authorized implementation scope.
<!-- AC:IMPLEMENTATION_TASKS -->
| Task | Increment | Requirements | Dependencies | Status | Blocker | Acceptance | Verification | Evidence |
|---|---|---|---|---|---|---|---|---|
| [TASK-001 Export](#{anchor}) | [INC-001](delivery-plan.md) | [BR-001, FR-001](requirements.md) | — | READY | — | CSV roundtrip preserves books | [VER-001](delivery-plan.md) | — |
| [TASK-002 Deliver](#task-002) | [INC-001](delivery-plan.md) | [FR-001](requirements.md) | — | READY | — | The user receives a local CSV | [VER-001](delivery-plan.md) | — |
<a id="{anchor}"></a>
## TASK-001 Export
Implement the existing CSV export contract; exclude import.
<a id="task-002"></a>
## TASK-002 Deliver
Return the exported file through the existing public application entrypoint.
''')
        return path

    def test_empty_role_body_is_not_a_completed_review(self):
        self.replace("evidence/council-review.md",
                     "No blocking finding for the local export contract.", "")
        self.assertRejected(self.validate(), "RUN-001")

    def test_roles_cannot_all_point_to_another_runs_section(self):
        text = self.council.read_text()
        text, count = re.subn(r"\]\(council-review\.md#run-\d+\)",
                              "](council-review.md#run-001)", text)
        self.assertEqual(7, count)
        self.council.write_text(text)
        self.assertRejected(self.validate(), "RUN-002")

    def test_nested_foreign_run_cannot_supply_an_empty_runs_conclusion(self):
        self.replace("evidence/council-review.md",
                     "No blocking finding for the local export contract.", "")
        self.replace("evidence/council-review.md", "### RUN-002", "#### RUN-002")
        self.assertRejected(self.validate(), "RUN-001")

    def test_own_nested_subheading_remains_part_of_the_runs_conclusion(self):
        self.replace("evidence/council-review.md",
                     "No blocking finding for the local export contract.",
                     "#### Basis for RUN-001\nNo blocking finding for the local export contract.")
        self.assertAccepted(self.validate())

    def test_fenced_example_cannot_replace_the_actual_role_ledger(self):
        self.replace("evidence/council-review.md", "<!-- AC:ROLE_RUNS -->",
                     "```markdown\n<!-- AC:ROLE_RUNS -->")
        self.replace("evidence/council-review.md", '<a id="run-001"></a>',
                     '```\n<a id="run-001"></a>')
        self.assertRejected(self.validate(), "нет завершённого запуска")

    def test_fenced_example_does_not_duplicate_a_real_contract_table(self):
        self.council.write_text(self.council.read_text() + '''
## Format example
````markdown
<!-- AC:ROLE_RUNS -->
| Run | Stage | Role | Actor | Input | Output | Gate | Start | End |
|---|---|---|---|---|---|---|---|---|
```text
This nested fence is part of the example, not the contract.
```
````
''')
        self.assertAccepted(self.validate())

    def test_stale_fail_snapshot_cannot_be_presented_as_current_pass(self):
        self.validation_row("| r0 | 1 | 1 | Prior failure | FAIL |")
        self.assertRejected(self.validate(), "AC:PACKAGE_VALIDATION")

    def test_malformed_validation_row_cannot_be_a_pass(self):
        self.validation_row("| garbage |")
        self.assertRejected(self.validate(), "AC:PACKAGE_VALIDATION")

    def test_pass_snapshot_cannot_report_nonzero_errors(self):
        self.validation_row("| r1 | 2 | 0 | None | PASS |")
        self.assertRejected(self.validate(), "AC:PACKAGE_VALIDATION")

    def test_current_pass_snapshot_can_retain_the_validation_command(self):
        self.validation_row("| revision=r1; python validate_package.py package --level L2 "
                            "--context greenfield --language en --allow-missing-render "
                            "| 0 | 0 | None | PASS |")
        self.assertAccepted(self.validate())

    def test_validation_candidate_allows_pending_result_without_self_certification(self):
        self.validation_row("| {{REVISION_AND_COMMAND}} | {{ERRORS}} | {{GATES}} "
                            "| {{WARNINGS}} | {{PASS_OR_FAIL}} |")
        set_meta(self.council, package_validation_status="PENDING")
        self.assertRejected(self.validate(), "package-validation")
        result = self.validate("--validation-candidate")
        self.assertAccepted(result)
        self.assertIn("Это ещё не handoff readiness", result.stdout)

    def test_candidate_does_not_hide_unfinished_requirements(self):
        self.validation_row("| {{REVISION_AND_COMMAND}} | {{ERRORS}} | {{GATES}} "
                            "| {{WARNINGS}} | {{PASS_OR_FAIL}} |")
        set_meta(self.council, package_validation_status="PENDING")
        path = self.package / "requirements.md"
        path.write_text(path.read_text() + "\n{{UNDECIDED_REQUIREMENT}}\n")
        self.restamp()
        self.assertRejected(self.validate("--validation-candidate"), "requirements.md")

    def test_requirement_link_cannot_point_to_a_different_requirement(self):
        self.replace("requirements.md", "| BR-001 | FR-001 | SCN-001 |",
                     "| BR-001 | [FR-001](#br-001-portable-copy) | SCN-001 |")
        self.restamp()
        self.assertRejected(self.validate(), "FR-001")

    def test_requirement_link_accepts_custom_html_anchor_on_its_definition(self):
        self.replace("requirements.md", "## FR-001: Local CSV export",
                     '<a id="local-export-requirement"></a>\n## FR-001: Local CSV export')
        self.replace("requirements.md", "| BR-001 | FR-001 | SCN-001 |",
                     "| BR-001 | [FR-001](#local-export-requirement) | SCN-001 |")
        self.restamp()
        self.assertAccepted(self.validate())

    def test_task_link_cannot_point_to_another_tasks_card(self):
        self.implementation_tasks()
        self.replace("implementation-plan.md", "[TASK-001 Export](#task-001)",
                     "[TASK-001 Export](#task-002)")
        self.assertRejected(self.validate("--implementation-plan"), "TASK-001")

    def test_task_link_accepts_custom_html_anchor_on_its_card(self):
        self.implementation_tasks(anchor="export-task-card")
        self.assertAccepted(self.validate("--implementation-plan"))

    def test_viable_option_requires_its_id_and_description(self):
        self.replace("evidence/council-review.md", "| OPT-001 | Stream local CSV | VIABLE |",
                     "| | | VIABLE |")
        self.assertRejected(self.validate(), "OPT")

    def test_option_ids_are_unique(self):
        self.replace("evidence/council-review.md", "| OPT-001 | Stream local CSV | VIABLE |",
                     "| OPT-001 | Stream local CSV | VIABLE |\n"
                     "| OPT-001 | Buffer the CSV output | VIABLE |")
        self.assertRejected(self.validate(), "OPT-001")

    def test_unlinked_non_markdown_evidence_is_not_silently_retained(self):
        (self.package / "evidence/observations.json").write_text('{"rows": 12}\n')
        self.assertRejected(self.validate(), "observations.json")

    def test_linked_zip_of_raw_observations_is_allowed(self):
        archive = self.package / "evidence/raw-observations.zip"
        with zipfile.ZipFile(archive, "w") as output:
            output.writestr("observations.json", '{"rows": 12, "exported": 12}\n')
        self.link_evidence(archive.name)
        self.assertAccepted(self.validate())

    def test_linked_full_package_zip_is_not_raw_evidence(self):
        archive = self.package / "evidence/package-snapshot.zip"
        with zipfile.ZipFile(archive, "w") as output:
            for path in self.package.glob("*.md"):
                output.write(path, path.name)
            output.write(self.council, "evidence/council-review.md")
        self.link_evidence(archive.name)
        self.assertRejected(self.validate(), "package-snapshot.zip")

    def test_linked_tar_of_raw_observations_is_allowed(self):
        data = self.package.parent / 'observations.csv'
        data.write_text('title,author\nBook,Writer\n')
        archive = self.package / 'evidence/raw-observations.tar.gz'
        with tarfile.open(archive, 'w:gz') as output:
            output.add(data, arcname='observations.csv')
        self.link_evidence(archive.name)
        self.assertAccepted(self.validate())

    def test_council_copy_cannot_be_disguised_as_an_independent_approval(self):
        copy = self.package / 'evidence/council-review-r1.md'
        copy.write_text(self.council.read_text())
        set_meta(copy, status='APPROVED', approved_by='synthetic-owner', approved_at=STAMP)
        self.link_evidence(copy.name)
        self.assertRejected(self.validate(), copy.name)

    def test_linked_independent_approval_is_allowed_despite_review_filename(self):
        approval = self.package / "evidence/external-review.md"
        approval.write_text(f'''---
architecture_revision: r1
artifact_language: en
artifact: human_decision
status: APPROVED
approved_by: external-review-board
approved_at: {STAMP}
---
# Independent external approval
The external review board approved revision r1 for implementation preparation.
The primary signed decision is held by the decision owner; this artifact records
its approval, not an additional Council role run or package history.
''')
        self.link_evidence(approval.name)
        self.assertAccepted(self.validate())


if __name__ == "__main__":
    unittest.main()
