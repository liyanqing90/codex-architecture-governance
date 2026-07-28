---
id: decision.integration-style-selection
kind: decision-guide
version: 1.0.0
status: active
domains:
- decision-process
triggers:
- integration
- style
- selection
quality_attributes: []
related: []
legacy_ids:
- decision-guide:integration-style-selection
last_reviewed: '2026-07-28'
review_after_days: 180
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Messaging Services
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/messaging
  authority: official
---

# Integration Style Selection

## Problem and intent

- Choose direct API
- queue
- pub-sub event
- stream
- webhook
- or workflow from coupling
- latency
- fan-out
- replay
- ordering
- and failure requirements.

## Mechanism

- Prefer a direct API when the caller requires an immediate result and temporal coupling is acceptable.
- Prefer a queue for one owned asynchronous work outcome.
- Prefer pub-sub events for independently owned consumers reacting to a fact.
- Prefer a durable workflow for multi-step state, timers, approvals, compensation, or recovery.
- Require idempotency, correlation, schema evolution, and replay ownership for asynchronous choices.

## Fit when

- A cross-boundary interaction requires a durable contract.

## Avoid when

- An in-process owned call is sufficient.

## Required capabilities

- consumer-inventory
- deadline-scenarios
- failure-semantics
- delivery-semantics

## Benefits

- Prevents event-driven complexity and synchronous coupling from being chosen by habit.

## Costs and liabilities

- Hybrid systems still require explicit semantic boundaries.

## Failure modes

- events-as-rpc
- queues-as-workflow-state
- retries-without-idempotency

## Alternatives

- Keep the current design and apply a smaller local correction.

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
