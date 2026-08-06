# Architecture knowledge contract

Knowledge supports decisions; it does not predetermine them.

## Knowledge classes

- Stable: quality concepts, styles, patterns, and tradeoffs.
- Slow-changing: framework capabilities, operating requirements, alternatives,
  and lock-in.
- Fast-changing: versions, support status, compatibility, advisories, pricing,
  and product lifecycle.

Persist stable and slow-changing knowledge with sources and freshness. Verify
fast-changing facts from current official sources when used.

Canonical knowledge is Markdown with validated YAML frontmatter and is
registered by `../knowledge/manifest.yaml`. The ten semantic packs keep
foundations, domains, decision guides, architecture styles, patterns,
technology profiles, reference architectures, migration guides,
anti-patterns, and case studies distinct. Legacy YAML catalogs are read-only
compatibility inputs.

## Compact context and source disclosure

The generated `knowledge-context.yaml` is a model-facing, validated compact
projection of the full Knowledge Selection. Its ordered entries carry the
canonical ID, path, entry hash, priority, and selection reasons; the full
Selection remains the provenance lock and must remain readable for scripts,
Reviews, and Gates. A compact projection may guide routing without loading the
selected Markdown entries or the complete exclusion ledger.

Use progressive disclosure: stable operational rules first, project-stable
Profile and constraints second, run-specific facts and Selection third, and
full source evidence on demand. Read a complete Knowledge entry after verifying
its recorded hash when a claim drives a candidate, an ambiguity cannot be
resolved from the projection, a volatile fact is used, or an explicit trade-off
requires the entry's mechanism and failure sections. Never treat the projection
as evidence for a candidate-driving claim.

## Entry standard

Every entry states:

- canonical ID, kind, semantic version, domains, triggers, qualities, and
  related canonical IDs;
- the problem and intent, mechanism, fit and avoid conditions;
- required capabilities, benefits, costs, and failure modes;
- alternatives, migration, exit, and evidence that changes the recommendation;
- quality trade-offs and explicitly volatile facts;
- official or standards sources, source policy, last review date, and maximum
  review age.

State what the mechanism does not solve. Keep architecture styles separate from
implementation technologies. Do not encode popularity, a vendor claim, or a
metric threshold as architecture truth.

Rule Packs protect one invariant at one owning boundary and specify evidence
requirements. Evidence Provider records describe deterministic or runtime
evidence surfaces and are executed only through explicit project
configuration. A validated run binds command/executable/configuration and
output hashes, but the result does not automatically establish severity or
impact. See `evidence-provider-contract.md`.

Run:

```bash
python3 ../scripts/validate_knowledge.py
```
