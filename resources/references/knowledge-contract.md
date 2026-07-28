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
