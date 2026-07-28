---
id: pattern.saga
kind: pattern
version: 1.0.0
status: active
domains:
- data-messaging
triggers:
- saga
quality_attributes: []
related: []
legacy_ids:
- pattern:saga
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Saga

## Problem and intent

- Coordinate a long business transaction through local commits and compensating actions.

## Mechanism

- Coordinate a long business transaction through local commits and compensating actions.

## Fit when

- Multiple autonomous data owners must participate without a distributed transaction.

## Avoid when

- A single database transaction can protect the invariant.

## Required capabilities

- durable-state
- idempotent-steps
- compensation-ownership

## Benefits

- Explicit partial-failure and compensation workflow.

## Costs and liabilities

- Compensation is business-specific and cannot always restore prior reality.

## Failure modes

- implicit-compensation
- missing-terminal-states

## Alternatives

- single-transaction
- durable-workflow

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
