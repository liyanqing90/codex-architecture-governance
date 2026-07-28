---
name: architecture-knowledge-curator
description: Maintains the plugin's architecture quality models, styles, patterns, technology profiles, reference architectures, migration guides, domain guidance, decision rules, machine rule packs, and evidence-provider registry. Use when adding or refreshing architecture knowledge, checking official-source freshness, reviewing framework capability claims, resolving duplicate or contradictory entries, or preparing a release whose decision knowledge may be stale. Does not audit a product or choose a product architecture.
---

# Curate architecture knowledge

Maintain reusable architecture knowledge without turning volatile product
claims into timeless rules.

## Load the contracts

Read:

- `../../../resources/references/knowledge-contract.md`;
- `../../../resources/knowledge/manifest.yaml`;
- `../../../resources/schemas/knowledge-entry.schema.json`;
- `../../../resources/schemas/knowledge-manifest.schema.json`;
- `../../../resources/schemas/rule-pack.schema.json`;
- `../../../resources/schemas/evidence-provider.schema.json`;
- `../../../resources/schemas/evidence-provider-config.schema.json`;
- `../../../resources/schemas/evidence-run.schema.json`;
- `../../../resources/references/evidence-provider-contract.md`;
- only the Markdown entries, Rule Packs, or provider contracts affected by the
  request.

## Classify the change

Classify knowledge before editing:

- stable: quality concepts, architecture styles, patterns, and tradeoffs;
- slow-changing: framework capabilities, operating models, and lock-in;
- fast-changing: versions, support status, compatibility, security advisories,
  pricing, and product lifecycle.

Keep stable knowledge in Markdown/frontmatter entries. Record official-source
URLs and a review window for slow-changing knowledge. Mark technology profiles
as dynamic and verify fast-changing facts from current official sources at use
time; do not freeze them into a Skill.

## Curation workflow

1. Define the decision changed by the proposed entry.
2. Use standards, official documentation, or maintainer documentation as
   sources. Use research only for claims absent from authoritative sources.
3. Follow `../../../docs/knowledge-authoring.md` and record all fourteen
   required body sections plus canonical ID, version, kind, domains, triggers,
   qualities, relationships, sources, source policy, and freshness.
4. Describe what a style, pattern, or technology does not solve.
5. Keep technology and architecture style separate.
6. Reject entries that merely repeat a product name, popularity claim, or
   unbounded best practice.
7. Deduplicate by decision semantics. Preserve different entries when
   similarly named mechanisms have different ownership or failure behavior.
8. Update associated decision rules, reference architecture, migration guide,
   provider, tests, and changelog when behavior changes.

Do not change a Rule Pack solely because a tool can detect a metric. A rule
must protect one invariant at an owning boundary and specify evidence
requirements.

## Validate

Run:

```bash
python3 ../../../resources/scripts/validate_knowledge.py
python3 ../../../scripts/validate_repository.py
```

Report added, changed, removed, or stale entries and their official sources.
Do not audit a repository, select its target architecture, or modify product
code.
