# Adopt cross-host workflow equivalence

- Status: accepted
- Date: 2026-08-08
- Owners: repository maintainers
- Scope: plugin distribution, runtime identity, host compatibility, and release evidence
- Supersedes: none
- Superseded by: none

## Context

Hengmu already emits a native Codex archive and an Agent Plugins archive. The
portable archive had a standard root `plugin.json`, Skills, and resources, but
removed `.codex-plugin/plugin.json`. Knowledge Selection reads and hashes that
exact file as a source-identity input. An unpacked portable archive could
prepare a project, inspect facts, and build a profile, then failed at Knowledge
Selection with `FileNotFoundError`.

Separately, agent clients expose different Hook, permission, rules, and
steering mechanisms. Hengmu's current public contract is explicit workflows
and an explicit deterministic Gate; it does not promise session-start scanning,
dangerous-operation interception, or automatic stop-time validation.

## Evidence

| Claim | Kind | Source | Observed |
| --- | --- | --- | --- |
| Agent Plugins v1 standardizes Skills and MCP, while client extensions are client-specific. | external fact | Agent Plugins v1 specification | 2026-08-08 |
| The portable archive omitted the manifest read and hashed by Knowledge Selection. | repository fact | `scripts/package_plugin.py` and `resources/scripts/select_knowledge.py` | 2026-08-08 |
| The extracted portable audit path failed only when it reached Knowledge Selection. | execution evidence | local release-archive reproduction | 2026-08-08 |
| The native manifest is part of existing persisted source identity. | repository fact | selector source contract and history-anchor validation | 2026-08-08 |
| Hengmu Gates run only when explicitly invoked. | accepted product constraint | Skill contracts and architecture constraints | 2026-08-08 |

## Decision

1. Define cross-host consistency as outcome equivalence for Hengmu's public
   Skills, deterministic CLI, schemas, artifact authority, and explicit Gate.
2. Keep `.codex-plugin/plugin.json` as the canonical native and provenance
   identity. Include its exact bytes in both archive formats.
3. Check in a host-neutral root `plugin.json` for Agent Plugins discovery.
   Package it at the portable archive root and reject shared identity drift.
4. Keep Codex-only `agents/openai.yaml` UI metadata out of the portable archive.
5. Smoke test the extracted portable archive through preparation, fact
   inspection, profile construction, and Knowledge Selection in CI and release.
6. Record live client installation evidence separately. Archive completeness
   must not be represented as proof for every IDE version.
7. Treat lifecycle, permission, rules, and steering integrations as optional,
   explicit host adapters. Do not add them to the v1 portable core or install
   them silently.

## Alternatives considered

- Change Knowledge Selection to hash root `plugin.json` in portable packages —
  rejected because it changes a persisted provenance input and would require a
  schema/source-identity migration rather than repairing packaging.
- Copy Codex UI metadata into all clients — rejected because it is not part of
  the Agent Plugins fixed discovery contract and its interpretation is
  client-specific.
- Add SessionStart, pre-tool, and stop Hooks for every named IDE now — rejected
  because these are not one portable contract and would add implicit behavior
  outside Hengmu's current product boundary.
- Claim compatibility from manifest shape alone — rejected because the prior
  package was structurally valid but its primary runtime path failed.

## Compatibility and rollback

This is additive for persisted artifacts and native Codex consumers. The
native archive and selector implementation are unchanged. Portable consumers
gain one hidden runtime/provenance file and a checked-in discovery manifest;
Skill names, schemas, CLI arguments, and exit codes do not change.

Rollback removes the portable source manifest and extracted smoke test and
restores the earlier allowlist. No user artifact migration is required, but
the prior portable package must then be documented as unable to execute
Knowledge Selection.

## Verification

- Assert deterministic native and portable archive bytes and inventories.
- Assert the portable manifest is host-neutral and identity-aligned.
- Run the extracted portable audit path through Knowledge Selection.
- Assert an archive without the provenance manifest fails the smoke test.
- Run repository validation, history-anchor validation, tests, packaging,
  checksum, SBOM, and the repository architecture gate.

## Revisit when

- Agent Plugins standardizes lifecycle or permission extensions;
- a named client requires an adapter for a Hengmu public outcome rather than a
  convenience trigger;
- selector provenance receives an explicitly migrated host-neutral identity
  contract.
