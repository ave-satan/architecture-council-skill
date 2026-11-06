---
name: architecture-council
description: "Design features at the right depth: a compact specification for a small feature in an existing project, or an Architecture Package with independent reviews for substantial or high-risk changes. Clarify requirements, cover use cases and data models, and fit solutions to the project. Also prepare implementation tasks from an existing design. Not for implementation-only requests or ordinary code review."
---

# Architecture Council

Design one feature at the depth its impact requires. Choose the mode before
loading its workflow; a lightweight specification is not a reduced Council
package and must not inherit its roles, gates or document set.

## Select the mode

- **Lightweight design:** a bounded feature in an existing project that fits its
  established architecture and can be introduced and reversed locally. Read
  [lightweight design](references/lightweight-design.md) only. Use it by default
  for requests such as “спроектируй небольшую фичу”, “встрой в существующий проект”
  or “подготовь компактную спецификацию”, when the impact supports that choice.
  Local API, UI or data-model additions do not by themselves require Council.
- **Council design:** a new project, substantial architectural choice, cross-domain
  change, material uncertainty about system-wide behavior, or high-impact/
  hard-to-reverse work. Read [Council design](references/council-design.md) and
  follow its protocol. An explicit request for independent Council review also
  selects this mode.
- **Prepare or continue implementation:** inspect the selected existing design.
  For a lightweight specification, follow the continuation section of
  [lightweight design](references/lightweight-design.md); do not convert it into
  a Council package just to plan tasks. For an Architecture Package, read
  [implementation preparation](references/implementation-preparation.md) and
  [package contract](references/package-contract.md). Reuse the existing artifact,
  not a new package or a repeat Council.

Do not select by lines of code or the word “small” alone. A material change to
money movement, authorization boundaries, regulated/organizationally critical
sensitive-data processing, critical public contracts, or data-loss/recovery
guarantees requires Council risk classification. Merely using an existing
authorization rule or data category is not such a change. For an unclear boundary,
inspect the affected project slice first; ask about consequential missing intent,
not facts discoverable in code. Explain a necessary change of mode briefly.

Do not downgrade an existing Council package with unresolved gates to bypass them.
A separate small extension may use a lightweight spec linked to that package
when its decisions and obligations remain intact. Ordinary implementation-only
edits need the project's coding workflow, not a design exercise.

## Shared boundaries

### Writing style: ASD-STE100

Apply ASD-STE100-style technical writing in every mode. This applies to all
agent-authored artifacts, documentation, reviews, questions, delegation prompts,
inter-agent messages and handoffs, including intermediate outputs.
Keep the language selected by the existing language rules below. Do not switch
to English to satisfy the style rule. For other languages, adapt the clarity
principles; do not claim formal ASD-STE100 compliance. For English, use its
writing rules and controlled vocabulary where applicable. This compact policy
is not a replacement for the [official standard](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf)
or evidence of full compliance.

- Use short, complete sentences with one topic. Give one action per instruction.
- Use direct verbs and active voice. Name the actor when responsibility matters.
- Use one consistent term for each concept. Explain unfamiliar technical terms.
- State conditions, actions and results explicitly. Avoid ambiguous references.
- Remove idioms, metaphors, filler and unnecessary synonyms. Do not remove
  necessary words, qualifications, risks or evidence to make the text shorter.
- Separate instructions from descriptions. Use ordered steps for a sequence.
- Preserve exact identifiers, commands, schemas, machine markers and quotations.
  Apply the style to the surrounding prose, not to external contracts or raw logs.

Include this policy and the selected language in every delegated assignment,
including nested delegation. Before sending a message or handing off a document,
check its clarity and terminology. Correct the text in place; do not create a
style report, approval gate or additional artifact. On continuation, apply the
policy to new and revised text without rewriting unrelated historical records.

### Language and authority

- Keep ordinary prose, questions, headings, table and diagram labels in the user's
  language. Preserve exact identifiers, paths, API/model names and technical terms
  where needed, not surrounding English prose.
- A design request permits relevant read-only discovery and design-document writes,
  not changes to application code, tests, data, infrastructure or external systems.
  Experiments with side effects need applicable explicit authorization.
- Design readiness or approval is not implementation authorization. If the user
  already requests design **and** implementation, finish the necessary design,
  then continue through the project's implementation workflow within that scope
  without asking for the same permission again. A recommended first increment
  does not narrow authorized whole-feature work.
- Keep current documents in place, use descriptive relative Markdown links and
  existing anchors inside them, and keep history in Git rather than duplicate
  archives or event logs. Do not overwrite unrelated work.
- If the user only asks to load the skill, wait for an actual design request.
