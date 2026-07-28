---
id: pattern.cqrs-event-sourcing
kind: pattern
version: 1.0.0
status: active
domains:
- data
triggers:
- cqrs
- event
- sourcing
quality_attributes: []
related: []
legacy_ids:
- pattern:cqrs-event-sourcing
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# CQRS and Event Sourcing

## Problem and intent

- Separate read and write models and preserve a versioned event history when both have demonstrated domain value.

## Mechanism

- Separate read and write models and preserve a versioned event history when both have demonstrated domain value.

## Fit when

- Read/write models diverge materially and audit
- temporal reconstruction
- or replay is a core requirement.

## Avoid when

- The system is ordinary CRUD or the team lacks event evolution capability.

## Required capabilities

- event-governance
- projection-rebuild
- idempotency

## Benefits

- Purpose-built reads and complete change history.

## Costs and liabilities

- Event versioning
- projections
- eventual consistency
- replay
- and high cognitive cost.

## Failure modes

- events-as-row-deltas
- no-replay-tests

## Alternatives

- transactional-model
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
