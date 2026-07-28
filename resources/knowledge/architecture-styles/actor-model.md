---
id: style.actor-model
kind: architecture-style
version: 1.0.0
status: active
domains:
- application
triggers:
- actor
- model
quality_attributes: []
related: []
legacy_ids:
- architecture-style:actor-model
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Actor Model

## Problem and intent

- Encapsulate identity
- state
- and serialized behavior for many concurrent entities.

## Mechanism

- Encapsulate identity

## Fit when

- Sessions
- devices
- rooms
- orders
- or other identity-bound state require per-entity serialization.

## Avoid when

- Work is stateless
- dominated by blocking operations
- or requires broad cross-entity queries.

## Required capabilities

- actor-identity
- lifecycle
- state-store

## Benefits

- Natural concurrency isolation and state ownership.

## Costs and liabilities

- Actor granularity
- lifecycle
- distributed queries
- placement
- and persistence complexity.

## Failure modes

- cross-actor-transactions
- blocking-actors

## Alternatives

- dapr-actors
- actor-runtime

## Migration and exit

- event-driven

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
