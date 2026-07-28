# Migrating to 0.3

Version 0.3 adds the facts → Profile → knowledge selection → artifact binding
chain and reduces the public Skill surface from nine to eight.

## Public Skill change

`architecture-knowledge-curator` is no longer a public plugin Skill. Its source
is under `maintainer/skills/architecture-knowledge-curator/`. Product audits,
verification, decisions, planning, and gates keep their public names.

If automation directly invoked the curator as a public Skill, move that
workflow to repository-maintenance automation and update its resource paths.

## Existing project configuration

Create deterministic facts without overwriting the rest of `.architecture`:

```bash
python3 resources/scripts/architecture_tool.py inspect-repository \
  --repo /path/to/project \
  --output /path/to/project/.architecture/repository-facts.yaml
```

Add the facts path and SHA-256, required knowledge domains, and separated
Profile sources to `.architecture/profile.yaml`. Compare any inferred fields
with real product constraints before treating them as declared context.

Create a task-specific selection:

```bash
python3 resources/scripts/architecture_tool.py select-knowledge \
  --facts /path/to/project/.architecture/repository-facts.yaml \
  --profile /path/to/project/.architecture/profile.yaml \
  --task "Current architecture audit" \
  --skill project-architecture-audit \
  --output /path/to/project/.architecture/knowledge-selection.yaml
```

## Artifact versions

- Schema `1.0` remains readable history.
- Trusted schema `1.1` remains supported for 0.2 compatibility.
- New project, AI-agent, and mobile Reviews should use `1.2`.
- New Decisions and Plans should use `1.2`.
- Aggregate Portfolio Reviews retain the `1.1` portfolio contract in 0.3.

Do not edit a legacy verified Review's version label in place.

## Safe Review migration

Use the migration command:

```bash
python3 resources/scripts/migrate_artifacts.py \
  --project /path/to/project \
  --review .architecture/reviews/legacy-verified.yaml \
  --facts .architecture/repository-facts.yaml \
  --knowledge-selection .architecture/knowledge-selection.yaml \
  --output .architecture/reviews/migrated-candidates.yaml
```

The output is always a candidate Review. Confirmed/rejected status, independent
verification, and critical-flow assessment are deliberately not copied as
current trust. Run `architecture-finding-verifier` against the migrated
candidate before gating.

## Decision and Plan migration

Regenerate a Decision from the 1.2 template after a trusted 1.2 Review exists.
Bind the exact knowledge selection and per-entry versions and hashes. Do not
translate a 0.2 catalog hash into a fabricated Markdown entry hash.

Regenerate a Plan after the Decision is accepted. Each item must bind exact
Finding fingerprints, selected knowledge IDs, assumptions, reversible
migration slices, rollback, stop conditions, and acceptance evidence.

## Validation

```bash
python3 resources/scripts/architecture_tool.py validate-project /path/to/project
python3 resources/scripts/architecture_tool.py validate-review \
  /path/to/review.yaml --project /path/to/project
python3 resources/scripts/architecture_tool.py validate-coverage \
  --project /path/to/project --review /path/to/review.yaml
```

Hash mismatches are migration failures, not fields to update blindly. Rebuild
the owning artifact from current evidence.
