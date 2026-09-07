---
name: architecture-council
description: "Design substantial L1-L3 features in greenfield or brownfield projects through requirements clarification, independent specialist reviews, viable architecture alternatives, business-led arbitration, Red Team, human review, and a design-only implementation handoff. Use when the user asks to architect or design a large, risky, cross-component, security-sensitive, performance-sensitive, or hard-to-reverse feature. Do not use for implementation-only requests, small local changes, or ordinary code review."
---

# Architecture Council

Produce a reviewable Architecture Package for one feature. Treat the Council's
result as a design recommendation, never as authorization to implement it.

## Load the protocol

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
   review, diagram label, and explanation in that language. Preserve code,
   paths, commands, API names, and external contracts verbatim.
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

For a development or dry-run session, enable diagnostic logging only when the
user explicitly asks for verbose diagnostics. Add `--verbose` to the initializer.
The default remains `NORMAL`.

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
root if different. Keep revisions inside the same package; a continuation does
not allocate another number. Existing unnumbered packages stay usable; do not
rename them without updating their references as a separate scoped change.

Do not overwrite a non-empty target. If a package already exists, inspect it and
continue its current architecture revision instead of reinitializing it.

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
Map relevant axes such as control plane, data plane, transport, topology,
synchronization, rendezvous, fallback, and external dependencies. Do not expand
the complete Cartesian product; record materially distinct families and an
evidence- or requirement-backed reason for excluding a relevant family.

Use independent agents for the initial specialist conclusions, Solution Space
Challenge, Alternative Architect, Arbiter, and Red Team when agent delegation is
available and allowed. Give the challenger requirements, constraints, and
specialist findings, but hide the preferred candidate. Record stable `actor_id`,
role, input revision/hash, output, and gate result in `process-ledger.md`.
For L1 follow the explicit reduced profile in protocol section 3.2: no mandatory
Solution Space Challenge, Preliminary Arbitration, or Red Team. Its Coverage
status is `NOT_APPLICABLE_L1`; an independent final Arbiter remains required.

When `diagnostics_mode` is `VERBOSE`, only the Council Orchestrator appends
observable events by running:

```bash
python3 <skill-dir>/scripts/log_event.py <package-directory> \
  --event role_completed \
  --status PASS \
  --stage 3 \
  --actor-id actor-2 \
  --role security_privacy \
  --run-id RUN-SEC-01 \
  --input-revision architecture-v1 \
  --artifact evidence/specialist-reviews/security-privacy.md \
  --summary "Security review завершён; два finding переданы на refinement."
```

Log stage and role boundaries, gate outcomes, clarification/user-input events,
revisions, returns, failures, recoveries, validation, and handoff readiness.
Never log chain-of-thought or hidden reasoning, raw prompts, secrets,
credentials, tokens, environment variables, unnecessary personal data, full
source code, or full tool output. Use concise summaries, IDs, hashes, and
artifact references. Subagents must not append concurrently. Before Human
Review, complete `evidence/verbose-review.md` from the observable log.

For each dispatched role, record `role_started` and `role_completed` separately
with the same `run_id`, actual actor, role, and exact input revision/hash from
the ledger. Record completion before the next dispatch. If registration is late,
keep `timestamp` as registration time; use `--occurred-at` with `--timing-basis`
only for an evidenced event time. Never invent a start time from first output.
On continuation, follow the revision and logging procedure in
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

Use a single default human reading surface: `decision-brief.md`. Aim for
250–450 words (about one page), shorter for a blocked evidence decision.
State the goal and recommendation, the decisive tradeoff/nearest alternative,
all material blockers or risks with consequences, what is actually verified,
and the concrete decision now needed. Do not omit a material condition to fit
the target length; group related details and link their evidence.
Use plain language in the body; keep machine statuses and IDs in metadata or
linked technical documents unless they help the decision. A diagram is optional
when it explains the decision more clearly than prose.

Keep README as a short navigation index, not another decision summary. Keep
`human-review.md` as the agent-maintained record of the user's actual answer,
not a form the user must read or fill out. Full requirements, expert reviews,
traceability and normative decisions remain available for agents and targeted
technical review. Do not make them a mandatory reading route for the owner.
Apply these rules on continuation too: refresh the current brief, preserve
revision-linked decisions/history, and explain only material changes in chat.

- Keep requirements atomic and preserve the full chain: source -> requirement ->
  architecture/ADR -> delivery increment -> verification -> production signal.
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

Add `--verbose` when `diagnostics_mode: VERBOSE`.

Use `--phase draft` for an incomplete or BLOCKED package; its success is not
readiness for handoff. A documented waiver produces a warning, not fake
independence. If log projection diverges, use `log_event.py PACKAGE
--rebuild-markdown` without appending the event again.

Resolve validation errors. Record warnings and actual evidence gaps honestly in
`evidence/package-validation.md`. Native editor rendering of inline Mermaid is
the assumed display path, not an additional verification task for the user.

## Keep continuation bounded

Before a series of experiments, set one branch budget in the existing evidence
plan: decision affected, sufficient evidence, total time/attempts including tools
and reviews, and stop/switch criteria. Reassess value before repairing the harness
or adding another experiment; a new subtask does not reset the budget. Follow
protocol section 10 and preserve existing authorization within its scope.
Compare conditional scenarios while requirements are open; do not block useful
comparison to make the user choose a mechanism prematurely.

Keep final-decision.md as the current decision summary with scope, applicable
review links and the next gate. After material input changes, update affected
normative documents and classification together; explicitly supersede obsolete
claims. Preserve useful evidence instead of restarting the whole package.
Keep verbose-review.md as a compact current retrospective (about 300–600 words),
not a second event log. Archive a prior summary only at a meaningful checkpoint;
do not copy it on every turn. Reuse immutable inputs by revision/hash, saving
unrecoverable mutable inputs once. Do not duplicate frozen copies or repeatedly
recount the full inventory. Validate changed artifacts during work and run the
full applicable check before handoff; repeat only for new changes or concerns.
For each new Markdown evidence file, preserve revision/language metadata and
clickable references at creation. Keep package-validation.md as one dated current
result with phase, input snapshot, structural errors, open gates and warnings;
link prior results instead of appending an endless history.

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

Default to one link to the current decision brief and the one relevant decision
or next action, normally within 150 words. Explain status in ordinary language;
do not recite every metadata field or list every possible action. Link extra
documents only when requested or necessary for that decision. The user may
answer in chat; record their answer and source yourself without inventing approval.

An approved revision can still be reviewed elsewhere. Any material change to
requirements, architecture, or evidence creates a new revision and returns the
package to Human Review. `implementation-handoff.md` is an instruction for a
future implementation run, not permission to begin one.

## Package navigation

Every reference to another package document must be a clickable relative Markdown
link with a descriptive label, including prose, tables, briefs, ADRs and evidence.
Resolve paths from the referring document (`../requirements.md` inside evidence).
Link specific requirements, findings and sections to existing anchors; add stable
explicit anchors when needed. Plain filenames, backticked paths and bare IDs do
not replace navigation links. Keep machine-readable fields, JSONL and code syntax
unchanged; provide navigation in the surrounding Markdown. Link only artifacts
that exist in the selected package profile; describe absent optional artifacts as
not applicable. Check local link targets and anchors before handoff.
