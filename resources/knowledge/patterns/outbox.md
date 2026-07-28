---
id: pattern.outbox
kind: pattern
version: 1.0.0
status: active
domains:
- data-messaging
triggers:
- outbox
quality_attributes: []
related: []
legacy_ids:
- pattern:outbox
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Transactional Outbox

## Problem and intent

- Atomically record domain state and messages in one local transaction for later relay.

## Mechanism

- Atomically record domain state and messages in one local transaction for later relay.

## Fit when

- A database commit and external message publication must not diverge.

## Avoid when

- No external publication exists or the transport participates in the same atomic boundary.

## Required capabilities

- idempotent-consumers
- relay-observability

## Benefits

- Prevents lost messages after committed state.

## Costs and liabilities

- Relay lag
- duplicate publication
- cleanup
- and table growth.

## Failure modes

- unbounded-outbox
- non-idempotent-consumers

## Alternatives

- cdc

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
