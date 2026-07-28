---
id: pattern.read-replica
kind: pattern
version: 1.0.0
status: active
domains:
- data
triggers:
- read
- replica
quality_attributes: []
related: []
legacy_ids:
- pattern:read-replica
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Read Replica

## Problem and intent

- Serve eligible reads from replicated database copies to reduce primary load or improve locality.

## Mechanism

- Serve eligible reads from replicated database copies to reduce primary load or improve locality.

## Fit when

- Read pressure dominates and bounded replication lag is acceptable for identified queries.

## Avoid when

- Read-after-write consistency is required or query/index optimization solves the bottleneck.

## Required capabilities

- lag-observation
- consistency-routing
- failover-runbook

## Benefits

- Read capacity
- locality
- and optional recovery copies.

## Costs and liabilities

- Staleness
- failover semantics
- routing
- consistency surprises
- and cost.

## Failure modes

- unbounded-stale-reads
- replicas-as-backups-only

## Alternatives

- cache-aside
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
