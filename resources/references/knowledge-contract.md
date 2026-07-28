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

## Entry standard

Every entry states:

- the problem and intent;
- fit and avoid conditions;
- benefits and liabilities;
- required capabilities and warning signals;
- alternatives or migration paths when applicable;
- official or standards sources;
- last review date and maximum review age.

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
python3 ../scripts/architecture_tool.py validate-knowledge
```
