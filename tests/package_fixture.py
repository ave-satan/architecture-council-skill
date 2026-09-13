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


def complete_package(package, level="L2", context="greenfield", language="en"):
    package.mkdir(parents=True)
    (package / "adr").mkdir()
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
                "design_maturity": "IMPLEMENTATION_READY", "implementation_start": "NOT_REQUESTED"}
    def document(name, body, **extra):
        path = package / name
        path.parent.mkdir(parents=True, exist_ok=True)
        values = metadata | extra
        path.write_text("---\n" + "\n".join(k + ": " + json.dumps(v) for k,v in values.items()) + "\n---\n\n" + body + "\n")
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
    document("decision-brief.md", "# Decision\nThe Council recommends a local streaming CSV writer. Human review is pending.")
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
    document("evidence/package-validation.md",
             "# Package validation\nThe current architecture package passed the structural review.",
             status="PASS")
    document("feature-classification.md", "# Classification\nThe exported data stays local; no authorization change or irreversible migration.", level=level, context=context, selected_roles=roles)
    if context == "brownfield":
        document("current-system.md", "# Current system\nThe fixture represents user-provided context, with no code claims.\n<!-- AC:CODE_EVIDENCE -->\n| Claim | Path | Revision | Start | End |\n|---|---|---|---|---|", code_evidence_status="NOT_APPLICABLE", code_evidence_reason="Synthetic user-supplied context contains no code claims")
    else:
        document("system-context.md", "# System context\nThe local application and user-selected file form the complete boundary.")
    if level in {"L2", "L3"}:
        document("evidence/preliminary-decision.md", "# Preliminary decision\nThe local streaming option proceeds to refinement.")
    if level == "L3":
        document("evidence/threat-model.md", "# Threat model\nLocal file disclosure is the material threat.")
        document("evidence/migration-rehearsal.md", "# Migration rehearsal\nNo persistent schema migration is required.")
        document("evidence/formal-risk-acceptance.md", "# Risk acceptance\nNo residual critical risk is accepted.")
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
    diagrams = [('target-architecture.md', 'target-container', 'flowchart LR\nDatabase --> CSV'),
                ('target-architecture.md', 'key-flow', 'sequenceDiagram\nUser->>Writer: Export')]
    if context == 'brownfield':
        diagrams.append(('current-system.md', 'current-container', 'flowchart LR\nDatabase --> Application'))
    for name, identifier, body in diagrams:
        path = package / name
        state = 'current' if name == 'current-system.md' else 'target'
        path.write_text(path.read_text() + f'\n```mermaid\n%% ac_id: {identifier}\n%% ac_state: {state}\n%% ac_purpose: Local export\n%% ac_scope: Books\n%% ac_legend: Directed flow\n%% ac_revision: r1\n%% ac_normative: {name}\n{body}\n```\n')
    result=run("record_classification.py",package)
    if result.returncode: raise RuntimeError(result.stderr)
    return roles


def complete_compact_package(package, level="L2", context="greenfield", language="en"):
    result = run("init_feature_package.py", package, "--level", level, "--context", context,
                 "--language", language, "--feature", "CSV export", "--revision", "r1")
    if result.returncode:
        raise RuntimeError(result.stderr)
    roles = sorted(["intake_requirements", "domain_architect", "solution_architect",
                    "implementation_maintainability", "arbiter"]
                   + (["solution_space_challenger", "red_team"] if level in {"L2", "L3"} else [])
                   + (["system_discovery"] if context == "brownfield" and level in {"L2", "L3"} else [])
                   + (["security_privacy"] if level == "L3" else []))
    common = {"architecture_revision": "r1", "artifact_language": language}
    def write(name, body, **meta):
        path = package / name; path.parent.mkdir(parents=True, exist_ok=True)
        values = common | meta
        path.write_text("---\n" + "\n".join(k + ": " + json.dumps(v) for k, v in values.items()) + "\n---\n\n" + body + "\n")
    markers = [("summary", "Summary"), ("overview", "Overview"), ("reading", "Reading"),
               ("documents", "Documents"), ("adrs", "ADRs"), ("interpretation", "Interpretation"),
               ("next", "Next"), ("implementation", "Implementation")]
    write("README.md", "# CSV export\n" + "\n".join(f"<!-- AC:README:{key} -->\n{label}." for key, label in markers) + """
<!-- AC:HUMAN_REVIEW -->
| Date / owner | Revision | Decision | Source |
|---|---|---|---|
| Pending | r1 | Awaiting review | Current task |
""",
          package_format="sectioned-v1", council_recommendation="ACCEPTED",
          human_review_status="AWAITING_HUMAN_REVIEW", design_maturity="IMPLEMENTATION_READY",
          implementation_start="NOT_REQUESTED", level=level)
    write("feature-charter.md", """# Charter
<!-- AC:CLASSIFICATION -->
| Level / context | Basis | Roles | Evidence | Gate |
|---|---|---|---|---|
| %s / %s | Local reversible export | %s | Current package | PASS |
## SCN-001: Save CSV
The user exports existing books to a local CSV file.
""" % (level, context, ", ".join(roles)), level=level, context=context,
          selected_roles=roles, classification_basis_sha256="pending")
    write("requirements.md", """# Requirements
## BR-001: Portable copy
The user can read their books outside this application.
## FR-001: Local CSV export
Export title and author with correctly escaped CSV fields.
<!-- AC:TRACEABILITY -->
| Business | Requirement | Scenario | Architecture | Increment | Verification | Signal |
|---|---|---|---|---|---|---|
| BR-001 | BR-001 | SCN-001 | [Design](target-architecture.md) | INC-001 | VER-001 | SIG-001 |
| BR-001 | FR-001 | SCN-001 | [Design](target-architecture.md) | INC-001 | VER-001 | SIG-001 |
""")
    target = """# Target
The local writer streams records to CSV.
```mermaid
%% ac_id: target-container
%% ac_state: target
%% ac_purpose: Local export
%% ac_scope: Books
%% ac_legend: Directed flow
%% ac_revision: r1
%% ac_normative: target-architecture.md
flowchart LR
Database --> CSV
```
```mermaid
%% ac_id: key-flow
%% ac_state: target
%% ac_purpose: Local export
%% ac_scope: Books
%% ac_legend: Directed flow
%% ac_revision: r1
%% ac_normative: target-architecture.md
sequenceDiagram
User->>Writer: Export
```
"""
    write("target-architecture.md", target, status="CANDIDATE")
    write("delivery-plan.md", """# Delivery and verification
## INC-001: Export books
The user receives a valid local CSV file.
<!-- AC:VERIFICATIONS -->
| Verification | Requirements | Method | Environment | Data | Criterion | Signal | Owner |
|---|---|---|---|---|---|---|---|
| VER-001 | BR-001, FR-001 | Public export | Local | Quotes | CSV roundtrip | SIG-001 | Maintainer |
<!-- AC:SIGNALS -->
| Signal | Description | Query | Expected | Threshold | Owner |
|---|---|---|---|---|---|
| SIG-001 | Completion message | User-visible | Success | Failure shown | Maintainer |
""")
    if context == "brownfield":
        write("current-system.md", """# Current
<!-- AC:CODE_EVIDENCE -->
| Claim | Path | Revision | Start | End |
|---|---|---|---|---|
```mermaid
%% ac_id: current-container
%% ac_state: current
%% ac_purpose: Current storage
%% ac_scope: Books
%% ac_legend: Directed flow
%% ac_revision: r1
%% ac_normative: current-system.md
flowchart LR
Database --> Application
```
""", code_evidence_status="NOT_APPLICABLE", code_evidence_reason="Synthetic context has no code claims")
    else:
        write("system-context.md", "# Context\nThe local application and selected file form the boundary.")
    runs, coverage, reviews, sections = [], [], [], []
    for index, role in enumerate(roles, 1):
        run_id, actor = f"RUN-{index:03}", f"actor-{index}"
        link = f"[Review](council-review.md#run-{index:03})"
        runs.append(f"| {run_id} | 3 | {role} | {actor} | r1 | {link} | PASS | {STAMP} | {STAMP} |")
        coverage.append(f"| {role} | {link} | None | N/A | N/A | COMPLETE |")
        reviews.append(f"| {run_id} | {role} | {actor} | r1 | PASS | No blocking finding | {link} |")
        sections.append(f'<a id="run-{index:03}"></a>\n### {run_id}\nNo blocking finding for the local export contract.')
    challenger = next((i for i, role in enumerate(roles, 1) if role == "solution_space_challenger"), None)
    review_body = """# Council review
<!-- AC:ROLE_RUNS -->
| Run | Stage | Role | Actor | Input | Output | Gate | Start | End |
|---|---|---|---|---|---|---|---|---|
%s
<!-- AC:ROLE_COVERAGE -->
| Role | Output | Findings | Response | Re-review | Status |
|---|---|---|---|---|---|
%s
<!-- AC:REVIEWS -->
| Run | Role | Actor | Input | Verdict | Findings | Section |
|---|---|---|---|---|---|---|
%s
%s
<!-- SSC:MAP -->
| Axis | Why | Mechanisms | Requirements |
|---|---|---|---|
| Materialization | Memory bound | Stream or buffer | FR-001 |
<!-- SSC:FAMILIES -->
| Family | Mechanism | Source | Requirements | Unknowns | Status |
|---|---|---|---|---|---|
| SF-001 | Local stream | solution_architect | FR-001 | No material gap | CANDIDATE_FAMILY |
<!-- SSC:CHALLENGE -->
Independent challenge completed where required.
<!-- SSC:GATE -->
Coverage is sufficient for the selected level.
<!-- AC:OPTIONS -->
| Option | Description | Feasibility |
|---|---|---|
| OPT-001 | Stream local CSV | VIABLE |
<!-- AC:WAIVERS -->
| ID | Actor | Roles | Revision | Approved by | Approved at | Evidence |
|---|---|---|---|---|---|---|
<!-- AC:PACKAGE_VALIDATION -->
| Snapshot | Errors | Gates | Warnings | Status |
|---|---|---|---|---|
| r1 | 0 | 0 | None | PASS |
""" % ("\n".join(runs), "\n".join(coverage), "\n".join(reviews), "\n".join(sections))
    extra = {"selected_roles": roles, "council_recommendation": "ACCEPTED",
             "solution_space_coverage": "PASS" if challenger else "NOT_APPLICABLE_L1",
             "missed_solution_family_status": "NONE" if challenger else "NOT_APPLICABLE_L1",
             "coverage_challenger_run_id": f"RUN-{challenger:03}" if challenger else "N/A",
             "coverage_challenger_actor_id": f"actor-{challenger}" if challenger else "N/A",
             "coverage_input_revision": "r1" if challenger else "N/A",
             "package_validation_status": "PASS"}
    write("evidence/council-review.md", review_body, **extra)
    result = run("record_classification.py", package)
    if result.returncode:
        raise RuntimeError(result.stderr)
    return roles
