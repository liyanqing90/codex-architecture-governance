# Target architecture implementation matrix

This matrix maps
`codex-architecture-governance-target-architecture-implementation.md` to
version 0.3 source and executable evidence.

## Implementation status

| Phase | Required outcome | Implementation | Evidence |
| --- | --- | --- | --- |
| 0 | Preserve trust and open-source baseline | 0.2 schemas and catalogs remain readable; release, security, governance, CI, locks, SBOM, and attestation paths remain intact | compatibility tests and repository validator |
| 1 | Define target boundaries | Eight public Skills, maintainer-only curator, deterministic scripts, ten Knowledge Packs, and project-local facts/selection | target architecture and accepted ADR |
| 2 | Establish content contracts | Manifest, Markdown/frontmatter entry schema, sources, freshness, relationships, volatile-fact policy, and authoring guide | `validate_knowledge.py` and knowledge tests |
| 3 | Acquire repository knowledge | Root-contained deterministic inspector for languages, frameworks, storage, interfaces, infrastructure, manifests, migrations, APIs, CI, and deployment | inspector tests, including scope escape |
| 4 | Build project context | Profile builder keeps detected, declared, and inferred inputs separate and derives reviews, packs, qualities, and domains | Profile schema and CLI tests |
| 5 | Select relevant knowledge | Skill/task/fact/Profile scoring, explicit includes/excludes, negative request handling, context budget, reasons, and complete exclusion ledger | selector regression and selection schema |
| 6 | Strengthen artifacts | Review/Finding/Decision/Plan 1.2 hashes, fingerprints, facts, selected knowledge, critical flows, assumptions, migration, rollback, and acceptance bindings | tamper and compatibility tests |
| 7 | Migrate safely | Legacy Review migration always downgrades conclusions to candidates and refuses overwrite | migration regression test and 0.3 guide |
| 8 | Upgrade workflows | All eight public Skills load facts and task-scoped knowledge at the appropriate boundary; verifier and gate enforce coverage | Skill static validation and 40 routing cases |
| 9 | Evaluate behavior | Separate routing, selection, decision, false-positive, and artifact-validity corpora plus ten adversarial fixtures and a model-agnostic harness | evaluation docs, test corpora, benchmark scorer |
| 10 | Release and govern | Versioned changelog, ADR, migration guide, compatibility policy, release checklist, deterministic ZIP, checksum, SPDX SBOM, and GitHub workflows | local release gate and tagged workflow |

## Delivered deterministic commands

```text
architecture_tool.py inspect-repository
architecture_tool.py build-profile
architecture_tool.py select-knowledge
architecture_tool.py validate-coverage
architecture_tool.py fingerprint-artifact
resources/scripts/validate_knowledge.py
resources/scripts/migrate_artifacts.py
```

The standalone scripts are also directly executable so a repository can call
one bounded function without entering the larger CLI command surface.

## Delivered artifact chain

```text
repository-facts.yaml
  └── profile.yaml
      └── knowledge-selection.yaml
          ├── knowledge-context.yaml
          └── Review 1.2
              └── Architecture Decision 1.2
                  └── Remediation Plan 1.2
                      └── quality gate and release evidence
```

Every arrow is validated by identity, exact SHA-256, semantic fingerprint, or
complete coverage. A generated plan is not completion evidence, and a migrated
verified label is not current verification.

## External evidence boundary

The repository does not fabricate a model-quality score. It implements the
corpus, fixtures, forward-test harness, metadata contract, and deterministic
scorer. A published model result requires an actual identified model, Codex
surface, version, date, and preserved run artifact. The deterministic 0.3
release report covers repository contracts and selectors only.
