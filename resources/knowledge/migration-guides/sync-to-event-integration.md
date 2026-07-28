---
id: migration.sync-to-event-integration
kind: migration-guide
version: 1.0.0
status: active
domains:
- integration
triggers:
- sync
- event
- integration
quality_attributes: []
related: []
legacy_ids:
- migration:sync-to-event-integration
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Synchronous API to Event Integration

## Problem and intent

- Introduce owned events and idempotent consumers without breaking the existing synchronous contract.

## Mechanism

- Keep the synchronous path until event outcome and recovery are observable.

## Fit when

- Independent consumers or failure decoupling are proven needs.

## Avoid when

- The caller still needs an immediate authoritative result.

## Required capabilities

- outbox
- event-contract
- idempotent-consumer
- correlation

## Benefits

- Incremental temporal decoupling and consumer autonomy.

## Costs and liabilities

- Dual paths
- eventual consistency
- duplicate effects
- and operational transition.

## Failure modes

- event-as-hidden-command
- synchronous-and-event-double-effect

## Alternatives

- Keep the current design and apply a smaller local correction.

## Migration and exit

- characterize-api
- publish-shadow-event
- validate-consumer
- switch-owned-flow
- remove-old-call

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
