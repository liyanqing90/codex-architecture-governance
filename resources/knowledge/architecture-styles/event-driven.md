---
id: style.event-driven
kind: architecture-style
version: 1.0.0
status: active
domains:
- application
triggers:
- event
- driven
quality_attributes: []
related: []
legacy_ids:
- architecture-style:event-driven
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Event-Driven Architecture

## Problem and intent

- Decouple producers and consumers around meaningful state changes and asynchronous processing.

## Mechanism

- Decouple producers and consumers around meaningful state changes and asynchronous processing.

## Fit when

- Multiple independent consumers
- replay
- real-time reactions
- or high-throughput streams are required.

## Avoid when

- Events merely replace understandable local calls or semantics and ownership are unstable.

## Required capabilities

- event-catalog
- idempotent-consumers
- schema-governance
- tracing

## Benefits

- Consumer autonomy
- temporal decoupling
- and scalable fan-out.

## Costs and liabilities

- Duplicates
- ordering
- schema evolution
- replay
- and eventual consistency.

## Failure modes

- generic-events
- missing-consumer-inventory
- dual-writes

## Alternatives

- queue
- pub-sub
- event-log

## Migration and exit

- outbox
- cdc

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
