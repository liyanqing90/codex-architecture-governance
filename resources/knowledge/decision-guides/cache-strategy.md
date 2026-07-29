---
id: decision.cache-strategy
kind: decision-guide
version: 2.0.0
status: active
domains:
- frontend
- backend-api
- data
triggers:
- cache
- ttl
- invalidation
quality_attributes:
- performance-efficiency
- reliability
related:
- pattern.materialized-view
- decision.data-loading-and-refresh
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cache-Aside pattern
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside
  authority: official
  supports:
  - CACHE-ASIDE
  - CACHE-SAFETY
maturity: golden
curation:
  method: assisted-reviewed
  reviewer: Codex Architecture Governance review
  reviewed_at: '2026-07-28'
---

# Cache Strategy

## Problem and intent

Reduce repeated computation or origin reads without treating a cache as an unowned second source of truth.

## Mechanism

Define the authoritative store first, then choose cache placement, key scope, population, invalidation, TTL, and stampede control for each read model. A cache miss must preserve correctness.

## Options

### Cache-aside

- Fit: Read-heavy data with tolerable bounded staleness.
- Avoid: A miss cannot safely load from the authority.
- Cost: Application-owned invalidation and duplicate cache logic.
- Failure: Write races or external writers serve stale values until expiry.
### Read/write-through

- Fit: A cache product can mediate all relevant reads or writes.
- Avoid: Some writers bypass the cache or product semantics are unclear.
- Cost: Vendor coupling and a larger critical data path.
- Failure: Partial cache/store failure obscures which write committed.
### Precomputed read model

- Fit: Queries are expensive and can consume an explicitly lagging projection.
- Avoid: Strong read-after-write consistency is mandatory.
- Cost: Projection storage, rebuilds, and lag monitoring.
- Failure: A broken projector returns plausible but incomplete results.

## Fit when

At least one named option fits a measured quality scenario and the team can own its
required failure and recovery behavior.

## Avoid when

The choice is driven only by a technology name, hypothetical scale, or a problem
already solved by the current design.

## Required capabilities

Authority declaration, tenant- and permission-safe keys, TTL or version invalidation, stampede suppression, capacity policy, hit/stale metrics, and a bypass path.

## Benefits

Can lower latency and origin load while keeping staleness and consistency observable.

## Costs and liabilities

Consumes memory and operational attention; every invalidation path adds a consistency obligation.

## Failure modes

Cache penetration, thundering herds, hot keys, cross-tenant leakage, unbounded cardinality, and treating a cache outage as an authority outage.

## Alternatives

Compare the current design and the named options—Cache-aside, Read/write-through, Precomputed read model—against the same
quality scenarios; do not compare feature lists without operating consequences.

## Migration and exit

Measure the uncached baseline, cache one idempotent read behind a flag, validate key isolation and stale bounds, then expand only while hit rate and origin relief justify the memory and complexity.

## Evidence to inspect

Query latency distribution, repetition and cardinality, key construction, write paths, invalidation traces, eviction behavior, cache-outage tests, and authorization boundaries.

## Evidence that changes the recommendation

Do not cache when reuse is low, correctness requires current authority reads, or sensitive values cannot be safely partitioned; choose a projection when computation rather than retrieval dominates.

## Quality trade-offs

Latency and origin protection trade against freshness, memory, failure modes, and operational coupling.

## Claim map

- CACHE-ASIDE: Cache-aside loads on misses and requires an explicit consistency strategy.
- CACHE-SAFETY: Sensitive or low-hit data can make caching inappropriate.

## Volatile facts

Product versions, protocol/library support, service limits, pricing, licensing, and
security advisories must be rechecked in the cited official sources at decision time.
The mechanisms and decision criteria above are maintained separately from those facts.
