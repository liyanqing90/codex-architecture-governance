---
id: pattern.compensating-transaction
kind: pattern
version: 1.0.0
status: active
domains:
- reliability
triggers:
- compensating
- transaction
quality_attributes: []
related: []
legacy_ids:
- pattern:compensating-transaction
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Compensating Transaction

## Problem and intent

- Apply domain-specific actions that reduce or reverse the effects of previously committed steps.

## Mechanism

- Apply domain-specific actions that reduce or reverse the effects of previously committed steps.

## Fit when

- A long-running operation crosses irreversible local commits and failure must be repaired.

## Avoid when

- A local atomic transaction can protect the invariant or reality cannot meaningfully be reversed.

## Required capabilities

- durable-state
- idempotent-compensation
- escalation

## Benefits

- Explicit recovery for partial business completion.

## Costs and liabilities

- Compensation can fail
- is not equivalent to rollback
- and needs audit and reconciliation.

## Failure modes

- generic-undo
- silent-compensation-failure

## Alternatives

- saga
- manual-reconciliation

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
