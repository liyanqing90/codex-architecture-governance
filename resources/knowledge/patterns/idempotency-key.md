---
id: pattern.idempotency-key
kind: pattern
version: 1.0.0
status: active
domains:
- reliability
triggers:
- idempotency
- key
quality_attributes: []
related: []
legacy_ids:
- pattern:idempotency-key
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Idempotency Key

## Problem and intent

- Bind repeated client commands to one durable outcome within a declared scope and lifetime.

## Mechanism

- Bind repeated client commands to one durable outcome within a declared scope and lifetime.

## Fit when

- Clients or infrastructure may retry a side-effecting command.

## Avoid when

- The operation is a pure read or has no stable request identity.

## Required capabilities

- durable-key-store
- request-fingerprint

## Benefits

- Prevents duplicate externally visible effects.

## Costs and liabilities

- Key scope
- retention
- payload equivalence
- and concurrent races.

## Failure modes

- key-without-payload-binding
- check-then-act

## Alternatives

- inbox

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
