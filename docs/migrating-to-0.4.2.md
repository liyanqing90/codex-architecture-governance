# Migrating to 0.4.2 contract changes

This guide covers the post-0.4.0 context-precision changes. It is intentionally
additive: previously accepted Reviews, Decisions, Plans, and benchmark results
remain historical records and are not rewritten to make a newer interpretation
look older or more trusted.

## Rebuild repository facts instead of editing history

New inspections emit repository-facts schema `1.1`. Every observed language,
framework, storage engine, interface, or infrastructure fact has one role:

```text
runtime | production | test | benchmark-fixture | example |
documentation | generated | vendor
```

Only `runtime` and `production` facts can infer a product type, domain,
Technology Profile, specialist review, or Rule Pack. Other roles remain
observable for auditability but do not route product architecture. Generated,
vendor, and third-party directory trees are pruned before inspection; generated
files outside those trees remain observable as `generated`.

`required_knowledge_domains` may therefore be empty for a repository with no
contributing product facts. This is intentional: the invoked Skill still loads
its required architecture foundations, but no product Domain Pack is inferred
from fixtures or generic repository presence.

For files that survive traversal, path classification is deterministic:
vendor, generated, benchmark fixture, test, example, documentation, runtime,
then production. Development-only
`package.json` dependencies and Python dev groups do not become product facts;
`requirements-dev*.txt` and `requirements-test*.txt` are test-role evidence.

Do not edit a SHA-bound historical facts/Profile/selection chain in place. To
replace a fixture-polluted inference such as `domain.mobile`, create a fresh
chain and a new review at the current commit:

```bash
python3 resources/scripts/architecture_tool.py inspect-repository \
  --repo . --output .architecture/repository-facts-current.yaml
python3 resources/scripts/architecture_tool.py build-profile \
  --facts .architecture/repository-facts-current.yaml \
  --output .architecture/profile-current.yaml
python3 resources/scripts/architecture_tool.py select-knowledge \
  --facts .architecture/repository-facts-current.yaml \
  --profile .architecture/profile-current.yaml \
  --task "Current architecture audit" \
  --skill project-architecture-audit \
  --output .architecture/knowledge-selection-current.yaml
```

Bind those new inputs in a new candidate and independently verified Review.
Schema `1.0` facts remain readable and intentionally retain their former
all-facts-contribute behavior for compatibility.

## Use bounded Knowledge selections

New selections use schema `1.2` and record every selected entry's `kind` and
`maturity`, a total budget, and a budget for all ten Knowledge kinds. Set a
tighter cap without changing unrelated kinds:

```bash
python3 resources/scripts/architecture_tool.py select-knowledge \
  --facts .architecture/repository-facts-current.yaml \
  --profile .architecture/profile-current.yaml \
  --task "Choose a target architecture" \
  --skill architecture-solution-advisor \
  --kind-budget foundation=4 \
  --kind-budget domain=3 \
  --kind-budget decision-guide=3 \
  --max-entries 14 \
  --output .architecture/decision-knowledge-selection.yaml
```

The Solution Advisor defaults discretionary context to Golden Knowledge.
Standard entries require an exact, recorded exception: a required Skill
contract, explicit include, maintainer mode, or a detected/profile-required
technology or domain with no declared Golden replacement. A shared task token
or broad domain match is not a replacement test. `--maintainer` is for
curation/maintenance workflows, not ordinary decision work.

Schema `1.0` and `1.1` selections remain readable. Schema `1.2` selections
with their complete recorded inputs can be deterministically replayed with:

```bash
python3 resources/scripts/architecture_tool.py validate-knowledge-selection \
  .architecture/decision-knowledge-selection.yaml \
  --facts .architecture/repository-facts-current.yaml \
  --profile .architecture/profile-current.yaml
```

## Run the A/B/C benchmark deliberately

Behavior benchmark schema `1.5` adds three declared treatments: `base`,
`full`, and `compressed`. Base receives no Skill, Reference, or Knowledge
content. Full uses the public Skill and declared References. Compressed uses a
small workflow-specific prompt. Full and Compressed use exactly the same
workflow-required Knowledge, so this is an end-to-end package ablation rather
than a claim about prompt text alone.

Every 1.5 command must contain both `{condition}` and `{context_manifest}`.
The run records a corpus-level declared-input proxy:

- Skill metadata/body and Reference/Knowledge/tool-description Unicode code
  points;
- unique fixture-tree bytes;
- hashes and paths of every declared input.

It is not model token usage, per-trial cost, or proof that a model read every
byte. Token, cost, and tool-call totals remain JSON `null` unless the invoked
surface emits that telemetry. Existing 1.4 run artifacts and score reports are
preserved as historical evidence.

## Declare the operating tier without weakening a gate

Gate policy schema `1.2` adds `product_mode: advisory|governed|enforced`.
Schema `1.1` policies remain trusted during the compatibility window. The mode
is descriptive: an explicit gate invocation has identical policy semantics in
all three labels. See [governance modes](governance-modes.md) for when each
mode is appropriate.

For an optional high-risk trajectory record, copy the governance-run template
under `.architecture/runs/` and validate it with
`validate-governance-run`. It is expressly informational and never becomes
gate evidence.

## Validate the migration

```bash
python3 scripts/validate_repository.py
python3 resources/scripts/architecture_tool.py validate-project .
python3 resources/scripts/architecture_tool.py validate-knowledge
python3 -m pytest
```

Do not replace an old accepted artifact merely to erase a historical defect.
The corrective fact chain, review, and decision must stand on their own
current evidence and verification.
