# Adopt workflow, knowledge, and deterministic script separation

- Status: accepted
- Date: 2026-07-29
- Owners: repository maintainers
- Scope: public Skills, Knowledge Packs, repository inspection, selection, and artifact schema 1.2
- Supersedes: public knowledge-curator portion of `2026-07-28-adopt-trusted-governance-1.1.md`
- Superseded by: none

## Context

Version 0.2 supplied strong provenance and deterministic gates, but reusable
knowledge remained in broad YAML catalogs and the public Knowledge Curator sat
beside end-user workflows. An audit could load irrelevant material, repository
facts and inference were not a first-class boundary, and new Decisions could
bind catalogs without proving which entries informed the task.

The target implementation requires one global method, project-local context,
and portfolio governance without installing a separate architecture Skill for
every repository.

## Evidence

| Claim | Kind | Source | Observed |
| --- | --- | --- | --- |
| The 0.2 public surface contained nine Skills, including a maintainer workflow. | fact | `skills/` at tag `v0.2.0` | 2026-07-29 |
| The 0.2 knowledge layer contained 128 YAML entries in eight catalogs. | fact | legacy catalogs under `resources/knowledge/` | 2026-07-29 |
| A catalog hash proves catalog identity but not task relevance. | inference | 0.2 Decision and knowledge contracts | 2026-07-29 |
| Repository detection can be deterministic only when it reports observations rather than suitability. | decision-driving inference | inspector threat and false-positive analysis | 2026-07-29 |
| Legacy verification cannot be recreated by a schema transformation. | fact | 1.1 verifier/candidate authority contract | 2026-07-29 |

## Decision

1. Expose exactly eight public end-user workflow Skills.
2. Keep the Knowledge Curator as a maintainer-only Skill.
3. Store new reusable knowledge as Markdown with validated frontmatter under a
   ten-pack manifest.
4. Retain the 0.2 YAML catalogs as read-only compatibility data.
5. Inspect repository facts with deterministic, root-contained scripts that
   make no architecture recommendation.
6. Separate detected facts, declared constraints, and bounded inference in the
   project Profile.
7. Select knowledge per repository, task, Skill, and context budget while
   preserving inclusion and exclusion reasons.
8. Bind schema 1.2 Reviews to exact facts, selection, Rule Packs, critical
   flows, and Finding/evidence fingerprints.
9. Bind schema 1.2 Decisions to selected entry versions and hashes, and Plans
   to Finding fingerprints, knowledge IDs, assumptions, and reversible
   migration evidence.
10. Migrate legacy verified Reviews only as candidates.

## Alternatives considered

- Keep long knowledge lists inside each Skill — rejected because it duplicates
  content and couples workflow routing to knowledge maintenance.
- Load every Knowledge Pack for every task — rejected because irrelevant
  context weakens proportionality and makes decisions harder to reproduce.
- Move deterministic inspection to a hosted service or MCP server — rejected
  because the current requirement is local, offline, auditable, and
  distribution-compatible.
- Replace 0.2 catalogs immediately — rejected because historical Decisions and
  compatibility tests still need their exact bytes.
- Preserve verified status during migration — rejected because transformation
  cannot reproduce independent verifier authority or critical-flow evidence.

## Consequences

- Positive: every new conclusion can distinguish fact, inference, selected
  knowledge, and unknown.
- Positive: Skills stay focused while knowledge grows independently.
- Positive: selection is reproducible, budgeted, and false-positive resistant.
- Positive: legacy trust cannot be silently upgraded.
- Negative: contributors maintain both read-only 0.2 catalogs and canonical
  Markdown entries during the compatibility window.
- Negative: new projects persist two additional inputs: repository facts and a
  knowledge selection.
- Operational: knowledge changes require relationship, freshness, selection,
  and evaluation checks before release.

## Verification

- Validate 205 Markdown entries across ten packs.
- Exercise React/FastAPI/PostgreSQL inclusion and Kafka/Kubernetes/mobile/
  event-sourcing/multi-agent exclusions.
- Reject scope escape, shallow entries, stale entries, unknown relations,
  stale selection hashes, missing critical-flow coverage, and stale Decision
  snapshots.
- Verify legacy Review migration emits candidates and passes the 1.2 contract.
- Run repository validation, project validation, tests, lint, formatting,
  dependency audit, deterministic packaging, checksum, and SBOM generation.

## Revisit when

- legacy 0.2 artifacts can be removed in a major compatibility change;
- aggregate Portfolio Reviews need a generalized 1.2 subject-facts contract;
- a remote knowledge registry or signed content distribution channel has a
  proven consumer, ownership model, and threat model;
- Codex exposes a first-class deterministic pre-Skill context provider.
