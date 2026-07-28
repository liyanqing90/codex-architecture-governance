---
id: pattern.branch-by-abstraction
kind: pattern
version: 1.0.0
status: active
domains:
- migration
triggers:
- branch
- abstraction
quality_attributes: []
related: []
legacy_ids:
- pattern:branch-by-abstraction
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Branch by Abstraction

## Problem and intent

- Introduce a stable seam so old and new implementations can coexist while callers migrate incrementally.

## Mechanism

- Introduce a stable seam so old and new implementations can coexist while callers migrate incrementally.

## Fit when

- A large internal replacement cannot safely land atomically.

## Avoid when

- The abstraction has no durable ownership boundary or a direct small replacement is safer.

## Required capabilities

- characterization-tests
- routing
- equivalence-observation
- removal-gate

## Benefits

- Incremental rollout
- comparison
- and rollback.

## Costs and liabilities

- Temporary dual paths
- abstraction leakage
- cleanup
- and divergent semantics.

## Failure modes

- permanent-dual-implementation
- seam-at-wrong-boundary

## Alternatives

- strangler
- feature-flag

## Migration and exit

- Introduce the mechanism behind a compatible boundary, verify it, then remove the old path.

## Evidence to inspect

- Trace the owning boundary, direct configuration or code, affected consumers, failure path, tests, and current operational evidence.
- For technology capabilities, confirm volatile behavior from the cited official source at decision time.

## Evidence that changes the recommendation

- A simpler option meeting the same measurable quality scenario should replace this recommendation.
- Missing ownership, compatibility, recovery, cost, or operational capability invalidates adoption until resolved.

## Quality trade-offs

- Balance business fit, reliability, maintainability, cost, and cognitive load.

## Volatile facts

- Product versions, support status, compatibility, security advisories, licensing, pricing, and service limits are time-sensitive and must be rechecked.
- Stable mechanism guidance remains separate from current vendor or release information.
