---
id: migration.strangler-migration
kind: migration-guide
version: 1.0.0
status: active
domains:
- system-replacement
triggers:
- strangler
- migration
quality_attributes: []
related: []
legacy_ids:
- migration:strangler-migration
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Strangler Migration

## Problem and intent

- Route bounded slices from legacy to replacement while preserving observable compatibility and rollback.

## Mechanism

- Each slice requires rollback and ownership transfer evidence.

## Fit when

- Behavior can be partitioned behind a routing seam.

## Avoid when

- Data and behavior cannot be separated safely or dual operation is unaffordable.

## Required capabilities

- routing
- contract-tests
- traffic-observability

## Benefits

- Incremental and reversible replacement.

## Costs and liabilities

- Dual routing
- data transition
- and prolonged compatibility.

## Failure modes

- no-removal-gate
- dual-writes-without-owner

## Alternatives

- Keep the current design and apply a smaller local correction.

## Migration and exit

- characterize
- introduce-router
- shadow-read
- migrate-slice
- verify
- retire-slice

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
