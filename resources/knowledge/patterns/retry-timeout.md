---
id: pattern.retry-timeout
kind: pattern
version: 1.0.0
status: active
domains:
- resilience
triggers:
- retry
- timeout
quality_attributes: []
related: []
legacy_ids:
- pattern:retry-timeout
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Retry with Timeout and Backoff

## Problem and intent

- Bound waiting and retry only transient failures with backoff
- jitter
- and an attempt budget.

## Mechanism

- Bound waiting and retry only transient failures with backoff

## Fit when

- A dependency exposes safe retry semantics and transient failures are expected.

## Avoid when

- The operation is non-idempotent or the failure is permanent or overloaded.

## Required capabilities

- idempotency
- error-classification
- retry-budget

## Benefits

- Recovers bounded transient faults.

## Costs and liabilities

- Can amplify outages and duplicate side effects.

## Failure modes

- nested-retries
- no-deadline
- retry-all-errors

## Alternatives

- degraded-mode
- circuit-breaker

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
