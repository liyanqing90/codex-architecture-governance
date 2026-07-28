---
id: style.space-based
kind: architecture-style
version: 1.0.0
status: active
domains:
- high-scale
triggers:
- space
- based
quality_attributes: []
related: []
legacy_ids:
- architecture-style:space-based
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Space-Based Architecture

## Problem and intent

- Distribute processing and replicated state across partitions to remove a central database bottleneck.

## Mechanism

- Distribute processing and replicated state across partitions to remove a central database bottleneck.

## Fit when

- Extreme
- elastic
- stateful throughput has proven contention that partition-local processing can resolve.

## Avoid when

- Ordinary database scaling
- caching
- or queueing meets measured targets.

## Required capabilities

- partition-key
- replicated-state
- rebalancing
- reconciliation

## Benefits

- High horizontal throughput and reduced centralized contention.

## Costs and liabilities

- Partitioning
- replication
- query limitations
- consistency
- recovery
- and specialized operations.

## Failure modes

- cross-partition-transactions
- speculative-scale

## Alternatives

- in-memory-data-grid
- partitioned-state-runtime

## Migration and exit

- partition-hot-path

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
