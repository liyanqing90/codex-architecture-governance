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

## Artifact compatibility and the 1.0 release

- Schema `1.0` is readable history in 0.3.
- Trusted schema `1.1` remains enforceable for 0.2 compatibility.
- Brief schema `1.0` remains the readable legacy open Greenfield contract. Brief
  schema `1.1` makes the current mode explicit: `open` has no architecture
  constraints, while `constrained` records required, preferred, and prohibited
  inputs. It is new in the single 1.0 release.
- Architecture Decision artifacts through `1.3` remain parseable and
  migratable (including
  remediation `1.1`/`1.2` and legacy open Greenfield `1.3`). Decision schema
  `1.4` is the current Brief 1.1 target contract for both open and constrained
  modes; it binds the Brief, target architecture, constraint assessments,
  source evidence, and Knowledge.
- Remediation Plan artifacts through `1.2` remain readable. Plan schema `1.3`
  adds the accepted Greenfield target path: it binds Brief/Decision directly,
  keeps Finding lists empty, and maps work to target units, flows, and
  constraints.
- Knowledge selection schema `1.1` adds context priority and preserves `1.0`
  selection readability.
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
- The public surface contains the stable `hengmu` routing entry and eight
  focused workflow Skills. Existing focused names remain directly invocable.
  The Knowledge Curator lives under `maintainer/skills/` and is not an
  end-user plugin workflow.
- The new Brief `1.1`, Decision `1.4`, and Plan `1.3` target-design contracts
  ship together in Hengmu `1.0.0`; legacy artifact paths remain parseable and
  migratable. No new target-design contract is released partially.
- Breaking schema, CLI, or Skill-name changes require a major release after
  `1.0.0`; during `0.x`, they require explicit migration guidance and a minor
  release at minimum. The stable router and all eight focused Skill names do not
  change in 1.0.

### Coexistence and migration

Old readers may continue to consume Brief 1.0 and artifacts through Decision
1.3/Plan 1.2. A 1.0 reader must preserve those paths and must not silently
reinterpret a legacy open Brief as a constrained Brief. To use constraints,
create a new Brief 1.1, challenge and assess every constraint, create a Decision
1.4, and obtain acceptance; do not mutate the old Brief or promote its prose.

Parseability and migration support do not preserve an artifact's former trust
status. A historical chain may be read without satisfying current Knowledge,
source-identity, freshness, or independent-verification policy. Before an old
artifact becomes accepted input to a current Gate, rerun the applicable
independent verification and bind current provenance; never promote a legacy
verification status by migration alone.

For accepted Greenfield work, create a new Plan 1.3 bound to the exact Brief and
Decision. For remediation, retain the existing Review/Finding bindings and Plan
1.2 path. Rollback is artifact-level: keep the old accepted chain, reject or
supersede the new proposal, and remove no legacy artifact. See
[migrating to 1.0](migrating-to-1.0.md) for the operational sequence.

See [the 0.4 migration guide](migrating-to-0.4.md) and
[the 0.3 migration guide](migrating-to-0.3.md). The
[0.2 migration guide](migrating-to-0.2.md) remains available for older
artifacts.
