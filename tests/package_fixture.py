"""Small completed synthetic CSV design, built through the public initializer."""
import json
import re
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"
STAMP = "2026-09-06T00:00:00Z"


def run(script, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)], text=True, capture_output=True)


def set_meta(path, **values):
    text = path.read_text()
    for key, value in values.items():
        line = key + ": " + json.dumps(value, ensure_ascii=False)
        pattern = r"^" + key + r":.*$"
        if re.search(pattern, text, re.M):
            text = re.sub(pattern, lambda _: line, text, count=1, flags=re.M)
        else:
            text = text.replace("---\n", "---\n" + line + "\n", 1)
    path.write_text(text)


def complete_package(package, level="L2", context="greenfield", language="en", verbose=True):
    args = [package, "--level", level, "--context", context, "--language", language,
            "--feature", "CSV export", "--slug", "csv-export", "--revision", "r1"]
    if verbose:
        args.append("--verbose")
    result = run("init_feature_package.py", *args)
    if result.returncode:
        raise RuntimeError(result.stderr)
    # These roles are the normative profiles, not imported from implementation.
    roles = ["intake_requirements", "domain_architect", "solution_architect", "implementation_maintainability", "arbiter"]
    if level in {"L2", "L3"}:
        roles += ["solution_space_challenger", "red_team"]
        if context == "brownfield":
            roles += ["system_discovery"]
    if level == "L3":
        roles += ["security_privacy"]
    metadata = {"feature": "CSV export", "architecture_revision": "r1", "artifact_language": language,
                "human_review_status": "AWAITING_HUMAN_REVIEW", "council_recommendation": "ACCEPTED",
                "design_maturity": "IMPLEMENTATION_READY", "implementation_start": "NOT_REQUESTED",
                "diagnostics_mode": "VERBOSE" if verbose else "NORMAL"}
    def document(name, body, **extra):
        path = package / name
        path.parent.mkdir(parents=True, exist_ok=True)
        values = metadata | extra
        path.write_text("---\n" + "\n".join(k + ": " + json.dumps(v) for k,v in values.items()) + "\n---\n\n" + body + "\n")
    for path in sorted(package.rglob("*.md")):
        if ".template." in path.name or path.name.endswith("-template.md"):
            path.unlink()
        elif path.name != "process-log.md":
            document(str(path.relative_to(package)), "# Review record\n\nLocal CSV export preserves the existing book records.")
    document("README.md", "# CSV export\n" + "\n".join(
        f"<!-- AC:README:{key} -->\n## {title}\n{body}\n" for key,title,body in [
            ("summary","In five minutes","Export personal books as CSV."),
            ("overview","Architecture","[Design](target-architecture.md)."),
            ("reading","Reading routes","[Requirements](requirements.md)."),
            ("documents","Documents","[Delivery](delivery-plan.md)."),
            ("adrs","Decisions","A single local writer is sufficient."),
            ("interpretation","Interpretation","The current architecture is authoritative."),
            ("next","Next actions","Review the proposed revision."),
            ("implementation","Implementation boundary","Implementation is not authorized.")]), level=level)
    document("feature-charter.md", "# Export books\n\n## SCN-001: Save a local CSV\nThe user exports existing books and receives a local CSV file.")
    document("requirements.md", """# Requirements
## BR-001: Portable copy
- Priority: MUST
- Approval: approved
The user can read their books outside this application.
## FR-001: Local CSV export
- Priority: MUST
- Approval: approved
Export title and author with correctly escaped CSV fields.
## Traceability
<!-- AC:TRACEABILITY -->
| Business | Requirement | Scenario | Architecture | Increment | Verification | Signal |
|---|---|---|---|---|---|---|
| BR-001 | BR-001 | SCN-001 | [Design](target-architecture.md) | INC-001 | VER-001 | SIG-001 |
| BR-001 | FR-001 | SCN-001 | [Design](target-architecture.md) | INC-001 | VER-001 | SIG-001 |
""")
    document("target-architecture.md", "# Target\n\n## Export\nA local CSV writer streams title and author from SQLite to the user-selected file.", status="CANDIDATE")
    document("delivery-plan.md", "# Delivery\n\n## INC-001: Export books\nImplements BR-001 and FR-001. User receives a valid local CSV file; validate escaped fields before release.")
    document("verification-plan.md", """# Verification
<!-- AC:VERIFICATIONS -->
| Verification | Requirements | Method | Environment | Data | Criterion | Signal | Owner |
|---|---|---|---|---|---|---|---|
| VER-001 | BR-001, FR-001 | Public export | Local | Quotes and newlines | CSV roundtrip | SIG-001 | Maintainer |
<!-- AC:SIGNALS -->
| Signal | Description | Query | Expected | Threshold | Owner |
|---|---|---|---|---|---|
| SIG-001 | Export completion message | User-visible | Success | Failure shown | Maintainer |
""")
    document("human-review.md", "# Human review\nAwaiting the user's review of this design revision.", status="AWAITING_HUMAN_REVIEW")
    document("feature-classification.md", "# Classification\nThe exported data stays local; no authorization change or irreversible migration.", level=level, context=context, selected_roles=roles)
    if context == "brownfield":
        document("current-system.md", "# Current system\nThe fixture represents user-provided context, with no code claims.\n<!-- AC:CODE_EVIDENCE -->\n| Claim | Path | Revision | Start | End |\n|---|---|---|---|---|", code_evidence_status="NOT_APPLICABLE", code_evidence_reason="Synthetic user-supplied context contains no code claims")
    output_map = {"intake_requirements":"requirements.md", "solution_architect":"target-architecture.md",
                  "arbiter":"evidence/arbiter-review.md", "domain_architect":"evidence/specialist-reviews/domain-architecture.md",
                  "implementation_maintainability":"evidence/specialist-reviews/implementation-maintainability.md",
                  "solution_space_challenger":"evidence/architecture-options.md", "red_team":"evidence/red-team-review.md",
                  "security_privacy":"evidence/specialist-reviews/security-privacy.md", "system_discovery":"current-system.md"}
    runs,coverage=[],[]
    for i,role in enumerate(roles,1):
        output=output_map[role]
        if not (package/output).exists():
            document(output,"# Independent review\nNo blocking objection to the local export contract.")
        set_meta(package/output,run_id=f"RUN-{i:03}",actor_id=f"actor-{i}",input_revision="r1")
        runs.append(f"| RUN-{i:03} | 3 | {role} | actor-{i} | r1 | [{role}]({output}) | PASS | {STAMP} | {STAMP} |")
        coverage.append(f"| {role} | [{role}]({output}) | No findings | N/A | N/A | COMPLETE |")
    document("process-ledger.md", "# Process\n<!-- AC:ROLE_RUNS -->\n| Run | Stage | Role | Actor | Input | Output | Gate | Start | End |\n|---|---|---|---|---|---|---|---|---|\n"+"\n".join(runs)+"\n\n<!-- AC:ROLE_COVERAGE -->\n| Role | Output | Findings | Response | Re-review | Status |\n|---|---|---|---|---|---|\n"+"\n".join(coverage)+"\n\n<!-- AC:WAIVERS -->\n| ID | Actor | Roles | Revision | Approved by | Approved at | Evidence |\n|---|---|---|---|---|---|---|",selected_roles=roles)
    if level != "L1":
        i=roles.index("solution_space_challenger")+1
        document("evidence/architecture-options.md", """# Options
<!-- SSC:MAP -->
| Axis | Why | Mechanisms | Requirements |
|---|---|---|---|
| Materialization | Memory bound | Stream or buffer | FR-001 |
<!-- SSC:FAMILIES -->
| Family | Mechanism | Source | Requirements | Unknowns | Status |
|---|---|---|---|---|---|
| SF-001 | Local streaming writer | solution_architect | FR-001 | No unknowns | CANDIDATE_FAMILY |
<!-- SSC:CHALLENGE -->
The independent challenger checked streaming and buffered implementations.
<!-- SSC:GATE -->
PASS: requirements admit a simple local stream; no omitted transport is relevant.
<!-- AC:OPTIONS -->
| Option | Description | Feasibility |
|---|---|---|
| OPT-001 | Stream local CSV | VIABLE |
""",solution_space_coverage="PASS",missed_solution_family_status="NONE",coverage_challenger_run_id=f"RUN-{i:03}",coverage_challenger_actor_id=f"actor-{i}",coverage_input_revision="r1")
    for path in package.glob("diagrams/**/*.mmd"):
        path.write_text("%% ac_state: target\n%% ac_purpose: Local export\n%% ac_scope: Books\n%% ac_legend: Directed flow\n%% ac_revision: r1\n%% ac_normative: ../../target-architecture.md\nflowchart LR\nDatabase --> CSV\n")
    if verbose and language == "en":
        path = package / "evidence/process-log.md"
        text = path.read_text()
        start = text.index("# Временная шкала")
        end = text.index("| # | Timestamp")
        path.write_text(text[:start] + "# Process timeline\n\nObservable events only.\n\n" + text[end:])
    result=run("record_classification.py",package)
    if result.returncode: raise RuntimeError(result.stderr)
    return roles
