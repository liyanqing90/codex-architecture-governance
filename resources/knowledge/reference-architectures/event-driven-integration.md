---
id: reference.event-driven-integration
kind: reference-architecture
version: 1.0.0
status: active
domains:
- integration
triggers:
- event
- driven
- integration
quality_attributes: []
related: []
legacy_ids:
- reference-architecture:event-driven-integration
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Event-Driven Integration

## Problem and intent

- Publish owned integration events through an outbox and schema contract to idempotent
- independently operated consumers.

## Mechanism

- Publish business-meaningful facts
- not internal table changes.

## Fit when

- Multiple consumers need temporal decoupling
- replay
- or independent processing.

## Avoid when

- A direct synchronous call gives clearer ownership and acceptable coupling.

## Required capabilities

- outbox
- schema-registry
- idempotent-consumers
- correlation
- replay-operations

## Benefits

- Consumer autonomy
- reliable publication
- replay
- and independent scaling.

## Costs and liabilities

- Eventual consistency
- duplicates
- ordering
- schema evolution
- and incident reconstruction.

## Failure modes

- events-as-rpc
- unknown-consumers

## Alternatives

- apache-kafka
- apache-pulsar
- managed-pubsub

## Migration and exit

- sync-to-event-integration

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
