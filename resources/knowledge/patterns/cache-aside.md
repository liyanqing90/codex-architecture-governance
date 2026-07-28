---
id: pattern.cache-aside
kind: pattern
version: 1.0.0
status: active
domains:
- data
triggers:
- cache
- aside
quality_attributes: []
related: []
legacy_ids:
- pattern:cache-aside
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Cache Aside

## Problem and intent

- Load data into a cache on demand while retaining an authoritative backing store.

## Mechanism

- Load data into a cache on demand while retaining an authoritative backing store.

## Fit when

- Repeated reads have measurable latency or origin-load impact and bounded staleness is acceptable.

## Avoid when

- Strong freshness is required or the working set has low reuse.

## Required capabilities

- ttl-policy
- invalidation
- observability

## Benefits

- Reduces read latency and origin load.

## Costs and liabilities

- Invalidation
- stampede
- penetration
- and stale data.

## Failure modes

- cache-as-source-of-truth
- unbounded-keys

## Alternatives

- materialized-view

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
