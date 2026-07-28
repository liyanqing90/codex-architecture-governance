---
id: pattern.circuit-breaker
kind: pattern
version: 1.0.0
status: active
domains:
- resilience
triggers:
- circuit
- breaker
quality_attributes: []
related: []
legacy_ids:
- pattern:circuit-breaker
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Circuit Breaker

## Problem and intent

- Stop repeated calls to a failing dependency and probe recovery deliberately.

## Mechanism

- Stop repeated calls to a failing dependency and probe recovery deliberately.

## Fit when

- Persistent dependency failure consumes capacity or amplifies latency.

## Avoid when

- Simple timeout and bounded retry already contain the failure.

## Required capabilities

- timeouts
- metrics
- degraded-mode

## Benefits

- Reduces cascading failure and resource exhaustion.

## Costs and liabilities

- Threshold tuning
- half-open behavior
- and shared state.

## Failure modes

- breaker-without-timeout
- global-breaker-for-unrelated-traffic

## Alternatives

- timeout
- bulkhead

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
