---
id: reference.web-queue-worker-ai
kind: reference-architecture
version: 1.0.0
status: active
domains:
- application
triggers:
- web
- queue
- worker
quality_attributes: []
related: []
legacy_ids:
- reference-architecture:web-queue-worker-ai
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Web Queue Worker for AI Tasks

## Problem and intent

- Separate interactive requests from bounded asynchronous inference or tool work using durable task identity and idempotent workers.

## Mechanism

- Escalate to durable workflow only when recovery semantics exceed queue and database state.

## Fit when

- Tasks outlive requests but do not require multi-step durable orchestration.

## Avoid when

- Work requires days-long state
- approval
- compensation
- or complex branching.

## Required capabilities

- task-store
- queue
- idempotency-key
- worker-observability

## Benefits

- Low-complexity asynchronous scaling.

## Costs and liabilities

- Task visibility
- result ownership
- cancellation
- and duplicate execution.

## Failure modes

- queue-as-state-store
- hidden-side-effects

## Alternatives

- managed-queue
- broker-worker

## Migration and exit

- queue-to-durable-workflow

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
