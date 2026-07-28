---
id: style.durable-workflow
kind: architecture-style
version: 1.0.0
status: active
domains:
- application
triggers:
- durable
- workflow
quality_attributes: []
related: []
legacy_ids:
- architecture-style:durable-workflow
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Durable Workflow

## Problem and intent

- Persist multi-step execution
- timers
- retries
- compensation
- approvals
- and recovery across process failure.

## Mechanism

- Persist multi-step execution

## Fit when

- Work lasts beyond a process lifetime or must pause
- resume
- cancel
- and recover.

## Avoid when

- A short idempotent job plus queue and database status is sufficient.

## Required capabilities

- workflow-versioning
- idempotent-activities
- observability

## Benefits

- Explicit recoverable state and long-running orchestration.

## Costs and liabilities

- Workflow determinism
- versioning
- history growth
- and runtime operations.

## Failure modes

- side-effects-in-replay
- unbounded-history

## Alternatives

- temporal
- dapr-workflow
- cloud-workflow

## Migration and exit

- queue-to-workflow

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
