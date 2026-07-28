# Architecture constraints

These constraints define the real decision boundary for this repository.
Maintainers review them with every release that changes a public contract.

## Product and business

- The seven public Skill names and their distinct user goals are compatibility
  contracts. Owner: maintainers. Source: plugin manifest and README. Changing
  them requires a documented migration and an appropriate SemVer release.
- Architecture diagnosis, independent verification, remediation planning, and
  deterministic gating remain separate workflows. Owner: maintainers. Source:
  accepted repository layout decision. This boundary is fixed unless a new
  architecture decision supersedes it.

## Platform and compatibility

- Runtime scripts support Python 3.11 through 3.13 with only PyYAML and
  jsonschema. Owner: maintainers. Source: CI boundary matrix and requirements.
  Review each minor release.
- The plugin keeps Skills as direct children of `skills/` and shared runtime
  contracts under root `resources/`. Owner: maintainers. Source: Codex plugin
  validation. Review when the Codex packaging contract changes.
- Artifact schemas and CLI exit codes are public contracts. Compatible
  additions are preferred; incompatible changes require migration guidance.

## Security, privacy, and compliance

- Runtime behavior requires no network, credentials, telemetry, or external
  service. Adding any of these requires a separate security and privacy review.
- Candidate model findings cannot block a build. Only schema-valid verified
  findings may enter the deterministic quality gate.
- Initialization may create `.architecture/` or `.architecture-portfolio/`
  only at an explicit target and must refuse to overwrite existing state.

## Operations, cost, and team

- Release artifacts contain only an explicit runtime allowlist and carry a
  reproducible SHA-256 checksum. CI and a maintainer verify both before release.
- The repository is maintained through reviewable source, schemas, tests,
  evaluation cases, and decision records; undocumented maintainer-only steps
  are not release prerequisites.

## Explicit non-goals

- This project does not implement an MCP server, hosted service, architecture
  dashboard, or automatic repository discovery.
- It does not accept risk, create waivers, or modify audited product code on a
  user's behalf.
