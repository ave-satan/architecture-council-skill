---
name: architecture-council
description: "Design substantial L1-L3 features through independent reviews, architecture alternatives, arbitration and human review. Also prepare or update executable implementation tasks and a delivery roadmap from an existing Architecture Package. Use for substantial architecture design or decomposition of its implementation. Do not use for unrelated implementation-only requests, small local changes or ordinary code review."
---

# Architecture Council

Produce a reviewable Architecture Package for one feature. Treat the Council's
result as a design recommendation, never as authorization to implement it.

## Load the protocol

First select the requested mode. For “prepare implementation”, “split this package
into tasks”, “update the implementation roadmap”, or starting/continuing execution
of an existing package, read
[implementation preparation](references/implementation-preparation.md) and the
[package contract](references/package-contract.md). Use the selected existing
package; do not initialize another package or rerun the whole Council. Read other
protocol sections only for unresolved design gates. The rest of this entrypoint
describes architecture design mode.

“Prepare and start” requests preparation followed by implementation within the
explicit scope. Finish preparation, resolve applicable prerequisites, then hand
off to the project's implementation workflow without asking again for the same
authorization. This skill does not itself define a coding workflow or authorize
unrequested deployment, external changes or additional work.
Use the actual user request to determine execution scope; a recommended first
increment is not a restriction on an authorized whole-feature implementation.

Before taking the first project action, read [references/protocol.md](references/protocol.md)
completely. It is the normative workflow and gate definition.

Read [references/decisions.md](references/decisions.md) only when a rule is
ambiguous, challenged, or needs its original rationale. Do not load it by
default.

Use [assets/template-manifest.yaml](assets/template-manifest.yaml) to determine
which artifacts are required for the selected level, context, and roles.
Read [references/package-contract.md](references/package-contract.md) when
initializing, resuming, or validating a package; preserve its machine markers
while translating human-readable text. Treat
files under `assets/feature-package/` as output templates, not as instructions
to load into context all at once.

## Start the run

1. Determine the user's language and keep every user-facing artifact, question,
   review, table heading, diagram label, and explanation in that language.
   Preserve exact code identifiers, paths, commands, API or model names,
   configuration values, and external contracts verbatim. Technical exceptions
   do not permit English connective or descriptive prose: translate ordinary
   wording around the exact term and avoid mixed-language phrases when a clear
   local-language equivalent preserves the meaning.
2. Confirm that the user is asking for architecture design. If they only ask to
   load or prepare the skill, wait for the feature-design command.
3. Establish the feature boundary, business goal, greenfield or brownfield
   context, evidence location, and Architecture Package destination.
4. Classify the change as L0-L3 using the protocol. For L0, explain that the
   Council is unnecessary and use ordinary planning unless the user explicitly
   asks for the Council anyway.
5. Keep the mandatory core for the level/context and add specialist roles
   triggered by the feature's risks. The initializer adds the mandatory core.
6. Create the package with the deterministic initializer. Resolve this skill's
   installed directory first, then run:

   ```bash
   python3 <skill-dir>/scripts/init_feature_package.py --package-root architecture \
     --level L2 \
     --context brownfield \
     --language ru \
     --feature "Синхронизация календаря" \
     --roles domain_architect,implementation_maintainability
   ```

The bundled templates are written in Russian. When the user's language is not
Russian, translate every copied human-readable template and diagram label into
the user's language immediately after initialization and before presenting or
continuing the package. Do not translate technical identifiers or contracts.

New packages use `001 — Синхронизация календаря`: the next number in the project's
shared package directory and a short meaningful title in the user's language.
Let the initializer allocate the number; do not build dated slugs or manually
guess the next number. Use that same numbered name in human-facing links and
summaries. `--slug` is optional technical metadata, not the visible package name.
The default package root is `./architecture`; reuse the project's established
root if different. Continue the same package in place; a continuation does not
allocate another number. Existing unnumbered packages stay usable; do not rename
them without updating their references as a separate scoped change.

Do not overwrite a non-empty target. If a package already exists, inspect it and
continue its current architecture revision instead of reinitializing it.

Before changing an existing package after a material requirement or evidence
change, run the continuation preflight in the package contract and update only
the affected current documents. Use repository history for recovery when it is
available. Never create full package copies, versioned document duplicates,
`.architecture-council-work`, or archives inside the package. If a non-versioned
workspace genuinely needs rollback protection, use one temporary sibling backup
outside the package and remove it after validation.

## Enforce the design-only boundary

During a Council run, allow read-only discovery and writes inside the
Architecture Package. Do not modify production code, tests, infrastructure,
data, deployments, or external systems. Do not execute a spike, benchmark,
migration rehearsal, or active security test unless the user separately
authorizes that exact action.

The skill does not broaden the permissions granted by the user's request.

## Orchestrate the Council

Follow the stage order and gates in the protocol:

1. Intake and clarification.
2. Classification and role selection.
3. Brownfield discovery or greenfield context definition.
4. Atomic functional, quality-attribute, constraint, and acceptance requirements.
5. Independent specialist reviews.
6. Solution Space Exploration across relevant mechanism axes.
7. Independent Solution Space Challenge before any preferred candidate is shown.
8. Candidate Architecture plus genuinely viable alternatives selected from the
   mapped solution families.
9. Business-led preliminary arbitration only after the coverage gate passes.
10. Targeted refinement, independent Red Team, final arbitration, package
    validation, and Human Review handoff.

For L2-L3, require a bounded solution-space map and an independent challenger.
Separate user outcomes, environment facts, explicit constraints, preferences and
implementation hypotheses. Preserve original wording and provenance. A mentioned
technology is not automatically mandatory; an explicit requirement needs no magic
keyword. Before deep work, clarify ambiguous constraints that exclude major
families: what need do they protect and which part of the solution do they cover?
Compare conditional interpretations read-only while awaiting clarification; never
silently weaken a prohibition or choose/execute a dependent solution without
confirmation. Do not re-ask settled constraints.

Derive the necessary functions from this task, not a fixed domain-specific list.
Explore whole ready-made solutions, configuration, composition with small adapters,
custom implementation and elimination of unnecessary components. Investigate real
available mechanisms for relevant families, with primary evidence. These are search
lenses, not a quota or permission to install. Give materially different families a
comparable first assessment before deep experiments: fit, reuse, custom work,
critical unknown and cheapest check. A name in the map is not enough. Compare
outcomes and invariants rather than demanding one candidate's internal contract
from every alternative. Revisit the family choice before expensive continuation;
sunk effort is not a reason to persist and rejecting on cost need not prove
technical impossibility. Keep this in the existing Charter and options map.

Before a component limitation becomes a proposed scope restriction, check whether
that component must perform the affected function. Consider useful combinations
of already discovered capabilities and their compatibility costs. Make the decisive
tradeoff explicit: user priority, evidence-based consequence, or reversible author
preference. Do not turn a preferred recovery or operating policy into a requirement.

Use the evidence sufficiency rules in protocol Stage 4, subsection 4.2: documented capabilities,
environment assumptions and future implementation acceptance are different claims.
An unrun integration test is not automatically a design blocker. Before blocking,
name the decision-changing unknown and the smallest dependent scope; continue
available research and conditional design. Preserve genuine no-go gates and never
claim runtime readiness from documentation or an accepted risk.

Use independent agents for the initial specialist conclusions, Solution Space
Challenge, Alternative Architect, Arbiter, and Red Team when agent delegation is
available and allowed. Give the challenger original user statements, requirements with constraint
provenance, and specialist findings, but hide the preferred candidate. Ask it to
challenge the framing itself, unsupported exclusions and restrictions applied
to the whole solution when they concern only one function. Record stable `actor_id`,
role, input revision/hash, section link, and gate result in `evidence/council-review.md`.
For L1 follow the explicit reduced profile in protocol section 3.2: no mandatory
Solution Space Challenge, Preliminary Arbitration, or Red Team. Its Coverage
status is `NOT_APPLICABLE_L1`; an independent final Arbiter remains required.

For each completed role, add one `AC:ROLE_RUNS` row with its stable `run_id`,
actual actor, role, exact input revision/hash, output, gate result and real
start/completion timestamps. Do not infer timestamps or duplicate the same run
in coverage or review tables. On continuation, keep only runs supporting the
current revision, rerun affected roles, and follow
[package-contract.md](references/package-contract.md#продолжение-прогона).

Never let one actor combine:

- Solution Architect and Alternative Architect;
- Solution Architect and Solution Space Challenger;
- architecture authorship or any specialist role with Red Team;
- author, specialist, Solution Space Challenger, Alternative Architect, or Red Team with Arbiter.

If concurrent agent slots are unavailable, run a fresh independent actor later
rather than merging incompatible roles. If independence cannot be established,
mark the gate `BLOCKED` or record a revision-scoped human waiver using `AC:WAIVERS`; never manufacture
evidence of independence.

Agents provide evidence and recommendations. They do not vote. The Arbiter maps
trade-offs to the business goal and mandatory requirements, asks conflicting
roles for targeted responses when useful, and escalates business choices or risk
acceptance to a human.

For L2-L3, do not ask the user to choose between technical approaches until
Solution Space Coverage is `PASS`. For L1 use `NOT_APPLICABLE_L1` and state
the rationale and limits of the compact comparison. A requirement or authority clarification may happen earlier,
but mark it `NOT_APPLICABLE_REQUIREMENT_CLARIFICATION` instead of presenting it
as a complete architecture choice.

When the user or Red Team proposes a materially distinct, potentially viable
family that was derivable from existing requirements and was neither mapped nor
excluded with evidence, record `MISSED_SOLUTION_FAMILY` with its real source.
Set the coverage gate to `REWORK`, supersede the dependent preliminary decision,
run targeted specialist and independent challenge passes, then arbitrate again.
Treat an option enabled only by a new requirement, permission, or private fact as
an input change rather than falsely labeling it a search failure.

## Maintain package quality

Use the root `README.md` as the single current decision, default human reading
surface, and compact package index. Aim for 200–350 words for its decision
content, shorter for a blocked evidence decision; keep navigation brief and
separate from the decision sections.
State the goal and recommendation, the decisive tradeoff/nearest alternative,
all material blockers or risks with consequences, what is actually verified,
and the concrete decision now needed. Do not omit a material condition to fit
the target length; group related details and link their evidence.
Use plain language in the body; keep machine statuses and IDs in metadata or
linked technical documents unless they help the decision. A diagram is optional
when it explains the decision more clearly than prose.

Keep the `AC:HUMAN_REVIEW` section in README as the record of the user's actual
answer, not a form the user must fill out. Requirements, reviews and traceability
remain available through a basic document navigation block for targeted technical
review. Do not repeat their content in README or make them a mandatory reading
route for the owner. Do not create `decision-brief.md` in new packages. When a
sectioned package is revised, merge any current legacy brief into README and
remove the duplicate after updating links; untouched legacy packages remain valid.
Apply these rules on continuation too: refresh the current README and explain
only material changes in chat. Git history preserves superseded prose; retain a
superseded ADR only when the current decision explicitly depends on it.

- Write each fact, rationale, risk and status once in its canonical document;
  elsewhere use a descriptive link. Prefer dense tables and bounded lists over
  repeated prose. Delete empty headings and inapplicable scaffold.
- Do not create a file merely because a function is independently validated.
  Validate stable sections by marker, metadata and provenance. Split a section
  into a file only for a different lifecycle/owner, a large raw result, or external handoff.
- Keep requirements atomic and preserve the full chain: source -> requirement ->
  architecture/ADR -> delivery increment -> verification -> production signal.
- When the feature introduces or changes persisted, exchanged, cached, or derived
  data, include a bounded reviewable data model in `target-architecture.md`.
  Cover the affected entities, value objects or messages; important fields and
  types/optionality; identifiers, uniqueness and indexes; relationships and
  cardinality; ownership, invariants and states; sensitivity, retention and
  schema evolution where relevant. Add an inline Mermaid data diagram: use
  `erDiagram` for entities and cardinalities, or `classDiagram` when DTOs,
  messages, value objects, or document structures are the clearer model. Keep a
  compact table beside it for types, nullability, indexes, constraints, retention,
  and evolution details that the diagram cannot express precisely. Match detail
  to design maturity and mark unknowns instead of inventing fields. If there is
  no data-model change, state that briefly and link the relevant current model;
  no new diagram is required. Do not create a separate model file by default.
- Keep current state, target state, and evolution path separate.
- Distinguish facts, inferences, assumptions, recommendations, and unknowns.
- Give every unresolved risk, assumption, condition, or blocker an owner and a
  verification or decision path.
- Put Mermaid diagrams inline in fenced `mermaid` blocks in the relevant Markdown
  document. Keep diagram metadata and architecture revision inside the block.
  Research-only illustrations in evidence may use `%% ac_kind: research`; they
  cannot replace normative diagrams (see package contract).
  Assume the user's editor renders Mermaid through its plugin; do not require
  separate .mmd files, SVG/PNG export, screenshots, or a renderer installation.
  Lack of preview in this session is not a gate or evidence gap. Report actual
  syntax/content problems if found; do not claim a visual check you did not do.
- Never turn `NO-GO`, `BLOCKED`, or `REWORK_REQUIRED` into a conditional pass.
- Do not treat two variants inside one unchallenged technical frame as adequate
  solution-space coverage.

After discovery, new requirements/facts, or a changed candidate, recheck the
classification, hard triggers, roles, and required evidence. Update the package
profile if needed; never blindly refresh the digest. After that review and the
last edit to Charter, Requirements, or Context/Dossier, run:

```bash
python3 <skill-dir>/scripts/record_classification.py <package-directory>
```

Before Human Review, run:

```bash
python3 <skill-dir>/scripts/validate_package.py <package-directory> \
  --level L2 \
  --context brownfield \
  --language ru \
  --roles domain_architect,implementation_maintainability
```

Use `--phase draft` for an incomplete or BLOCKED package; its success is not
readiness for handoff. A documented waiver produces a warning, not fake
independence.

Resolve validation errors. Record warnings and actual evidence gaps in the
`AC:PACKAGE_VALIDATION` section of Council Review. Native editor rendering of inline Mermaid is
the assumed display path, not an additional verification task for the user.

## Keep continuation bounded

Before a series of experiments, set one branch budget in the existing evidence
plan: decision affected, sufficient evidence, total time/attempts including tools
and reviews, and stop/switch criteria. Reassess value before repairing the harness
or adding another experiment; a new subtask does not reset the budget. Follow
protocol section 10 and preserve existing authorization within its scope.
Compare conditional scenarios while requirements are open; do not block useful
comparison to make the user choose a mechanism prematurely.

Before device execution, group independent checks sharing setup into one bounded
session: prepare a hypothesis/case matrix, install once, reuse granted permissions
within their scope, run isolated cases, then clean up once. This is the
orchestrator's responsibility, not something the user must request. Use separate
sessions when an earlier result determines the next experiment or isolation,
safety or authorization requires it; explain the dependency. Define per-case
outcomes and reset, case-local failures versus session-wide stop conditions,
and a total session limit before starting. A failed case should not cancel
independent cases unless isolation, safety or trustworthy measurement is lost.
Batching does not authorize additional cases or require simultaneous execution.
Keep the runner proportional: group existing commands where possible rather
than building a general test framework for one short experiment.

Keep README as the current decision, basic package navigation, and next gate.
Keep risks and assumptions in requirements.md, and the current-to-target path,
rollout and rollback in delivery-plan.md. After material input changes, update
affected normative documents and classification together and remove obsolete
prose from the current package. Keep one current section per role in Council
Review; repository history, not versioned files in `evidence/`, preserves older
iterations. Separate evidence is allowed only for a large raw result, an
unrecoverable external input, or an independently approved record that the
current decision links directly. Never store package archives, backup copies,
`revision-impact.md`, versioned Council Reviews, or unlinked scratch reviews in
`evidence/`. Validate changed artifacts during work and run the full applicable
check before handoff; repeat only for new changes or concerns.

## Finish the design run

End with a concise, self-contained summary in the user's language that states:

- the Council recommendation and design maturity;
- the exact package path and architecture revision;
- blockers, conditions, and evidence gaps;
- that `human_review_status` is `AWAITING_HUMAN_REVIEW` unless a human has
  explicitly reviewed this revision;
- that `implementation_start` remains `NOT_REQUESTED`;
- the concrete decision or next action relevant now; implementation still
  requires its own explicit command after architecture approval.

Default to one link to the current decision and the one relevant decision or
next action, normally within 120 words. Explain status in ordinary language;
do not recite every metadata field or list every possible action. Link extra
documents only when requested or necessary for that decision. The user may
answer in chat; record their answer and source yourself without inventing approval.

An approved revision can still be reviewed elsewhere. Any material change to
requirements, architecture, or evidence creates a new revision and returns the
package to Human Review. Create `implementation-plan.md` only when implementation
preparation is requested; it is a plan/instruction, not permission to begin work.

## Package navigation

Every reference to another package document must be a clickable relative Markdown
link with a descriptive label, including prose, tables, briefs, ADRs and evidence.
Resolve paths from the referring document (`../requirements.md` inside evidence).
Link specific requirements, findings and sections to existing anchors; add stable
explicit anchors when needed. Plain filenames, backticked paths and bare IDs do
not replace navigation links. Keep machine-readable fields and code syntax
unchanged; provide navigation in the surrounding Markdown. Link only artifacts
that exist in the selected package profile; describe absent optional artifacts as
not applicable. Check local link targets and anchors before handoff.
