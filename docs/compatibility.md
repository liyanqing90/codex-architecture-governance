# Compatibility

## Supported runtime boundary

The portable CLI supports CPython 3.11–3.13 with the exact packages and hashes
in `requirements-runtime.lock`. CI runs repository validation, tests, lint,
formatting, packaging, and checksum verification on:

| Operating system | Python 3.11 | Python 3.13 |
| --- | --- | --- |
| Ubuntu | CI | CI |
| macOS | CI | CI |
| Windows | CI | CI |

`requirements.txt` contains supported dependency ranges. The lock is the
reproducible installation boundary used by CI and release packaging.

## Codex and plugin surface

The repository validates:

- plugin manifest and runtime layout with the official plugin validator;
- every Skill with the official Skill validator;
- routing metadata and five activation/boundary cases per Skill;
- deterministic archive contents independent of local marketplace state.

Automated CI cannot launch every Codex desktop, CLI, or ChatGPT plugin surface.
Before a release, maintainers should install the built ZIP or local marketplace
entry in at least one current Codex surface and record the application version,
surface, operating system, and observed routing result. This manual evidence is
time-bound and must not be represented as universal compatibility.

## Artifact compatibility

- Schema `1.0` is readable history in 0.3.
- Trusted schema `1.1` remains enforceable for 0.2 compatibility.
- Schema `1.2` is the current project, AI-agent, mobile, Decision, and Plan
  contract. It binds repository facts, selected Markdown knowledge, critical
  flows, evidence and Finding fingerprints, assumptions, and migrations.
- Aggregate Portfolio Reviews continue to use the trusted `1.1` portfolio
  contract in 0.3; per-project facts and selections are hash-bound evidence.
- The 128 YAML knowledge entries remain read-only compatibility data. New
  Decisions use the 205 Markdown entries registered by the ten-pack manifest.
- Repository-local Rule Packs are supported under `.architecture/rules/` and
  must use Rule Pack schema `1.1`; organization packs cannot shadow bundled IDs.
- Evidence Provider commands are project configuration, not portable defaults.
  A provider is ready only when its executable and project markers exist on
  the current operating system.
- JSON, SARIF 2.1.0, and JUnit XML provider outputs receive structural
  validation. Text output is captured and hashed but remains lower-assurance
  evidence.
- CLI success, policy failure, and invalid-input exit codes remain `0`, `1`,
  and `2`.
- Public Skill names are compatibility contracts.
- The public surface contains eight Skills. The Knowledge Curator moved to
  `maintainer/skills/` and is no longer a routed plugin workflow.
- Breaking schema, CLI, or Skill-name changes require a major release after
  `1.0.0`; during `0.x`, they require explicit migration guidance and a minor
  release at minimum.

See [the 0.3 migration guide](migrating-to-0.3.md). The
[0.2 migration guide](migrating-to-0.2.md) remains available for older
artifacts.
