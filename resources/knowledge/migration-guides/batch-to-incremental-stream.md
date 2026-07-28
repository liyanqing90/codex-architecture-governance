---
id: migration.batch-to-incremental-stream
kind: migration-guide
version: 1.0.0
status: active
domains:
- data
triggers:
- batch
- incremental
- stream
quality_attributes: []
related: []
legacy_ids:
- migration:batch-to-incremental-stream
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Batch to Incremental Stream

## Problem and intent

- Introduce incremental events
- checkpoints
- and reconciliation beside an authoritative batch output.

## Mechanism

- Run stream and batch in comparison until discrepancy is bounded and owned.

## Fit when

- Measured freshness requirements cannot be met by optimized batch schedules.

## Avoid when

- Batch remains within the product freshness target.

## Required capabilities

- event-log
- checkpoints
- reconciliation
- watermark-policy

## Benefits

- Lower data latency with comparison against a known baseline.

## Costs and liabilities

- Dual computation
- event-time semantics
- state recovery
- and divergence.

## Failure modes

- stream-without-replay
- no-batch-reconciliation

## Alternatives

- Keep the current design and apply a smaller local correction.

## Migration and exit

- emit-changes
- build-shadow-stream
- reconcile
- switch-readers
- retain-recovery-job

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
