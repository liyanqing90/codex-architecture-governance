---
id: migration.queue-to-durable-workflow
kind: migration-guide
version: 1.0.0
status: active
domains:
- orchestration
triggers:
- queue
- durable
- workflow
quality_attributes: []
related: []
legacy_ids:
- migration:queue-to-durable-workflow
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Queue to Durable Workflow

## Problem and intent

- Move task state
- timers
- retries
- approvals
- and recovery into an explicit durable workflow.

## Mechanism

- Migrate new tasks first; drain legacy tasks without converting in-flight histories.

## Fit when

- Queue plus status rows cannot reliably express or recover multi-step work.

## Avoid when

- A single idempotent worker remains sufficient.

## Required capabilities

- idempotent-activities
- workflow-versioning
- correlation

## Benefits

- Explicit workflow state and resumption.

## Costs and liabilities

- Runtime adoption
- determinism
- worker versioning
- and history migration.

## Failure modes

- side-effects-in-workflow-code
- unversioned-state

## Alternatives

- Keep the current design and apply a smaller local correction.

## Migration and exit

- model-state
- wrap-activities
- mirror-status
- route-new-tasks
- drain-old-queue

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
