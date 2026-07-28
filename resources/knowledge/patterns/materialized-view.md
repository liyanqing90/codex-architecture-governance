---
id: pattern.materialized-view
kind: pattern
version: 1.0.0
status: active
domains:
- data
triggers:
- materialized
- view
quality_attributes: []
related: []
legacy_ids:
- pattern:materialized-view
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Materialized View

## Problem and intent

- Precompute a read model for expensive queries with explicit rebuild and freshness semantics.

## Mechanism

- Precompute a read model for expensive queries with explicit rebuild and freshness semantics.

## Fit when

- Read shapes differ from writes and measured query cost matters.

## Avoid when

- Direct indexed queries meet targets.

## Required capabilities

- rebuild
- checkpoint
- freshness-signal

## Benefits

- Predictable read latency and query isolation.

## Costs and liabilities

- Staleness
- rebuild
- ordering
- and storage.

## Failure modes

- no-rebuild-path
- unknown-lag

## Alternatives

- cache-aside
- cqrs

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
