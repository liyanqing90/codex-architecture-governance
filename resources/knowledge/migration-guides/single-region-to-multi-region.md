---
id: migration.single-region-to-multi-region
kind: migration-guide
version: 1.0.0
status: active
domains:
- resilience
triggers:
- single
- region
- multi
quality_attributes: []
related: []
legacy_ids:
- migration:single-region-to-multi-region
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Single Region to Multi-Region

## Problem and intent

- Add a second region through explicit recovery targets
- data replication
- traffic control
- failover
- and failback.

## Mechanism

- Start active-passive unless concurrent regional writes are a proven requirement.

## Fit when

- Regional outage impact and recovery targets justify cost and consistency tradeoffs.

## Avoid when

- Backup and single-region recovery meet business requirements.

## Required capabilities

- rto-rpo
- replication
- traffic-management
- failover-runbook
- capacity

## Benefits

- Reduced regional recovery time and optional locality.

## Costs and liabilities

- Consistency
- split brain
- capacity
- testing
- data residency
- and doubled operations.

## Failure modes

- active-active-with-global-writes
- untested-failback

## Alternatives

- Keep the current design and apply a smaller local correction.

## Migration and exit

- define-recovery
- restore-secondary
- replicate
- shadow-read
- rehearse-failover
- automate-failback

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
