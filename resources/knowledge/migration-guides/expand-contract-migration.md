---
id: migration.expand-contract-migration
kind: migration-guide
version: 1.0.0
status: active
domains:
- contract
triggers:
- expand
- contract
- migration
quality_attributes: []
related: []
legacy_ids:
- migration:expand-contract-migration
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Expand and Contract Migration

## Problem and intent

- Add compatible fields or shapes
- migrate all consumers
- then remove the old contract after evidence.

## Mechanism

- Never contract until telemetry proves old-path disuse.

## Fit when

- Mixed versions or persisted data prevent atomic change.

## Avoid when

- All consumers deploy atomically and no data persists.

## Required capabilities

- consumer-inventory
- compatibility-tests
- usage-signals

## Benefits

- Rolling compatibility and reversible expansion.

## Costs and liabilities

- Temporary dual semantics and cleanup debt.

## Failure modes

- same-release-removal
- unknown-consumer

## Alternatives

- Keep the current design and apply a smaller local correction.

## Migration and exit

- expand
- dual-read
- backfill
- migrate-consumers
- verify-zero-use
- contract

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
