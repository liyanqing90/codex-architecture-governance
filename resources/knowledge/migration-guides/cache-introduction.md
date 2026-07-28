---
id: migration.cache-introduction
kind: migration-guide
version: 1.0.0
status: active
domains:
- performance
triggers:
- cache
- introduction
quality_attributes: []
related: []
legacy_ids:
- migration:cache-introduction
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Introduce Cache Safely

## Problem and intent

- Add a measured cache with explicit keys
- consistency
- invalidation
- expiry
- stampede control
- and bypass.

## Mechanism

- Retain a correct uncached path and prove the cache changes the measured bottleneck.

## Fit when

- Observed repeated reads or dependency cost exceeds targets.

## Avoid when

- Indexes
- query changes
- or capacity fixes resolve the problem more simply.

## Required capabilities

- load-baseline
- cache-key-contract
- invalidation
- telemetry

## Benefits

- Reduced latency and backend load.

## Costs and liabilities

- Staleness
- memory cost
- invalidation
- cold starts
- and new failure modes.

## Failure modes

- cache-as-authority
- infinite-ttl

## Alternatives

- Keep the current design and apply a smaller local correction.

## Migration and exit

- measure
- cache-shadow-read
- compare
- enable-cohorts
- protect-stampede
- define-bypass

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
