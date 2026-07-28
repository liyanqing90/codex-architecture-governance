# Adopt a marketplace-ready Plugin → Skills repository layout

- Status: superseded
- Date: 2026-07-28
- Owners: repository maintainers
- Scope: repository, distribution, and Skill ownership boundaries
- Supersedes: none
- Superseded by: `2026-07-28-adopt-trusted-governance-1.1.md`

## Context

The architecture-governance suite contains seven related reusable workflows,
shared schemas, templates, and a deterministic CLI. Keeping the suite only in a
user-global Skill directory makes versioning, contribution, CI, release, and
attribution difficult. Putting repository documentation inside each Skill
would increase prompt cost and violate progressive disclosure.

## Evidence

| Claim | Kind | Source and environment | Observed | Reference | Freshness / redaction |
| --- | --- | --- | --- | --- | --- |
| Codex Skills use progressive disclosure and should keep one focused user goal. | fact | OpenAI Codex manual | 2026-07-28 | `Build skills`, official manual | Fresh local manual cache; no sensitive data. |
| Multiple reusable Skills should be packaged as a Plugin for distribution. | fact | OpenAI Codex manual | 2026-07-28 | `Build skills` and `Package your plugin` | Fresh local manual cache; no sensitive data. |
| Repository guidance belongs in a concise root `AGENTS.md`. | fact | OpenAI Codex manual | 2026-07-28 | `Custom instructions with AGENTS.md` | Fresh local manual cache; no sensitive data. |
| Every direct child under a plugin's `skills/` path is validated as a Skill. | fact | Codex `plugin-creator` validator | 2026-07-28 | `_shared` was rejected for lacking `SKILL.md` | Local official validator; no sensitive data. |
| The existing CLI behavior has executable protection. | fact | migrated suite | 2026-07-28 | `tests/test_architecture_tool.py` | 10 baseline tests passed before migration. |

## Decision

Use three ownership layers:

1. The repository root owns open-source governance, development dependencies,
   CI, release automation, evals, and contributor documentation.
2. `.codex-plugin/plugin.json` owns installable identity and points to
   `skills/`.
3. Each `skills/<name>/` owns exactly one workflow. Root `resources/` owns only
   runtime contracts, schemas, templates, references, and the portable CLI.

Package only runtime files. Keep tests, evals, and repository documentation out
of Skill directories. Preserve the seven public Skill names.

## Alternatives considered

- Keep only a global `~/.codex/skills/architecture` directory — rejected
  because it has no independent release, contribution, or CI boundary.
- Merge all workflows into one architecture Skill — rejected because project,
  AI, mobile, portfolio, verification, planning, and gating have different
  triggers, inputs, and success criteria.
- Duplicate shared schemas and rules into every Skill — rejected because
  contract drift would become likely and prompt context would grow.
- Build an MCP server — deferred because the workflow uses repository evidence
  and deterministic local files; no live external data or controlled remote
  action is required.

## Consequences

- Positive: the suite becomes independently versioned, installable, testable,
  attributable, and contribution-ready.
- Positive: Skill prompts remain concise while deterministic contracts remain
  shared.
- Negative: the Skills are distributed as one plugin because each relies on
  root `resources/`; standalone Skill copying is not supported.
- Negative: schema or CLI changes require coordinated versioning across the
  plugin, templates, tests, and changelog.
- Operational: releases must pass repository validation and deterministic
  package checks before a tag becomes a published artifact.

## Verification

- Validate the plugin with the Codex `plugin-creator` validator.
- Validate all Skills with the Codex `skill-creator` validator.
- Run repository validation, pytest, Ruff lint, Ruff formatting, and
  deterministic package tests.
- Inspect the release ZIP allowlist and SHA-256 checksum.

## Revisit when

- The suite requires live authenticated data or controlled remote actions.
- Codex changes Plugin or Skill packaging contracts.
- A shared resource cannot remain discoverable without coupling Skill
  installation paths.
- Independent release cadences make one plugin an inappropriate distribution
  boundary.
