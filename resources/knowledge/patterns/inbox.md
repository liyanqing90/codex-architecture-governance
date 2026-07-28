---
id: pattern.inbox
kind: pattern
version: 1.0.0
status: active
domains:
- data-messaging
triggers:
- inbox
quality_attributes: []
related: []
legacy_ids:
- pattern:inbox
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Consumer Inbox

## Problem and intent

- Record processed message identities within the consumer transaction to suppress duplicate effects.

## Mechanism

- Record processed message identities within the consumer transaction to suppress duplicate effects.

## Fit when

- At-least-once delivery can repeat commands or events.

## Avoid when

- Operations are naturally idempotent and duplicate processing is harmless.

## Required capabilities

- stable-message-identity
- cleanup-policy

## Benefits

- Protects side effects from duplicate delivery.

## Costs and liabilities

- Identity scope
- retention
- storage
- and concurrency controls.

## Failure modes

- global-id-collisions
- check-then-act-race

## Alternatives

- idempotency-key

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
