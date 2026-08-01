# Add a stable Hengmu routing entry

- Status: accepted
- Date: 2026-08-01
- Owners: repository maintainers
- Scope: public Skill discovery, invocation, routing, and compatibility
- Supersedes: public-surface count in `2026-07-29-adopt-workflow-knowledge-script-separation.md`
- Superseded by: none

## Context

Hengmu exposes eight deliberately separate workflow Skills. Their separation
protects authority transitions between candidate audit, independent
verification, solution decision, remediation planning, and deterministic
gating. It also makes the installed command surface difficult to discover and
requires users to remember internal workflow names.

The desired interaction is one memorable public name that can show available
capabilities and route a natural-language goal without merging the underlying
contracts.

## Evidence

| Claim | Kind | Source | Observed |
| --- | --- | --- | --- |
| The installed plugin has eight focused workflow names. | fact | `skills/` and `scripts/validate_repository.py` at `37a403d` | 2026-08-01 |
| The focused names encode distinct lifecycle and authority boundaries. | fact | accepted workflow-separation and context-precision decisions | 2026-08-01 |
| A user who cannot recall a focused name cannot reliably invoke it directly. | user requirement | implementation request | 2026-08-01 |
| A routing-only Skill can improve discovery without owning workflow conclusions. | decision-driving inference | Skill contract analysis | 2026-08-01 |

## Decision

1. Add `hengmu` as the stable public entry point.
2. Accept both explicit commands and natural-language goals.
3. When invoked without a task, show the full menu and up to three contextual
   recommendations without starting work or creating repository state.
4. Route to exactly one focused Skill, read that Skill completely, and let it
   own the task.
5. Keep all eight focused Skill names directly invocable indefinitely unless a
   separately approved breaking migration replaces them.
6. Keep the entry point free of audit, verification, decision, planning, gate,
   schema, or policy logic.

## Alternatives considered

- Rename every Skill with a `hengmu-` prefix — rejected because users would
  still need to remember multiple names and existing automation would require a
  migration.
- Merge all workflows into one large Skill — rejected because it would collapse
  authority boundaries and increase irrelevant activated context.
- Document the existing names more prominently — rejected because documentation
  does not provide an in-product discovery path.
- Add only fixed subcommands — rejected because natural-language routing lets
  the user remember only `$hengmu`.

## Compatibility and rollback

This change is additive. Existing focused invocations and artifact contracts
remain unchanged. The new entry becomes a public compatibility contract when
released and therefore requires an appropriate minor version under the
project's pre-1.0 policy.

Rollback before release removes `skills/hengmu/`, its five routing cases, and
its documentation. Rollback after release must preserve the entry or provide a
documented breaking migration; no persisted project data needs conversion.

## Verification

- Validate the entry with the official Skill validator.
- Require one direct, indirect, incomplete, negative, and edge routing case.
- Assert that all eight focused `SKILL.md` paths are present in the router.
- Assert that direct focused invocation bypasses the router.
- Run repository validation, tests, lint, formatting, deterministic packaging,
  and the repository architecture gate.

## Revisit when

- Codex provides native nested Skill command discovery or completion;
- routing forward tests show material ambiguity between two workflows;
- a focused workflow is intentionally replaced through a breaking migration.
