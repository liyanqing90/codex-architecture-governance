---
id: decision.optimistic-vs-pessimistic-update
kind: decision-guide
version: 2.0.0
status: active
domains:
- frontend
- mobile
- data
triggers:
- optimistic
- conflict
- rollback
quality_attributes:
- maintainability
related:
- decision.state-management
- decision.local-first-vs-server-first
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: MDN conditional requests
  url: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Conditional_requests
  authority: official
  supports:
  - HTTP-CONDITION
- title: React useOptimistic
  url: https://react.dev/reference/react/useOptimistic
  authority: official
  supports:
  - OPTIMISTIC-STATE
maturity: golden
curation:
  method: assisted-reviewed
  reviewer: Codex Architecture Governance review
  reviewed_at: '2026-07-28'
---

# Optimistic vs Pessimistic Update

## Problem and intent

Choose how a client represents a mutation before authority confirms it and how concurrent conflict is detected and repaired.

## Mechanism

Optimistic UI applies a reversible local projection tagged to a mutation ID; pessimistic UI waits for authority. Both need an authoritative concurrency condition such as version, ETag, or lock and a defined conflict outcome.

## Options

### Optimistic projection

- Fit: Success is common, the action is reversible, and fast feedback matters.
- Avoid: Failure is frequent, irreversible, regulated, or difficult to explain.
- Cost: Rollback/rebase logic and temporary identity mapping.
- Failure: Late failure rolls back newer intent or duplicates a retried effect.
### Pessimistic confirmation

- Fit: The authoritative result or scarce resource must be known first.
- Avoid: Network latency would make frequent low-risk actions unusable.
- Cost: Visible wait states and lower interaction throughput.
- Failure: Disabled UI hides timeout uncertainty or duplicate submissions.
### Optimistic concurrency with explicit conflict

- Fit: Multiple writers edit versioned resources and conflicts can be presented.
- Avoid: No meaningful merge or user resolution exists.
- Cost: Version checks, conflict payloads, merge UX, and retry discipline.
- Failure: Last-write-wins silently discards another actor's change.

## Fit when

At least one named option fits a measured quality scenario and the team can own its
required failure and recovery behavior.

## Avoid when

The choice is driven only by a technology name, hypothetical scale, or a problem
already solved by the current design.

## Required capabilities

Mutation identity, authority version/ETag, idempotency, reversible patch or re-fetch path, temporary IDs, conflict UX, retry limits, and tests for out-of-order completion.

## Benefits

Balances interaction latency with explicit correctness and conflict behavior.

## Costs and liabilities

Optimism increases client state complexity; pessimism increases perceived latency and blocking.

## Failure modes

Rollback overwrites later edits, duplicate commands, stale version checks, inaccessible failure feedback, and optimistic handling of irreversible money or permission effects.

## Alternatives

Compare the current design and the named options—Optimistic projection, Pessimistic confirmation, Optimistic concurrency with explicit conflict—against the same
quality scenarios; do not compare feature lists without operating consequences.

## Migration and exit

Add server concurrency conditions first, introduce a mutation state model, enable optimism for one reversible action, inject conflicts and failures, and keep pessimistic fallback for high-risk cases.

## Evidence to inspect

Mutation success/failure rate, latency, reversibility, concurrency frequency, server version checks, idempotency behavior, user impact, and race tests.

## Evidence that changes the recommendation

Choose optimism only when rollback and conflict semantics are safer than making the user wait; high-risk irreversible effects generally require confirmation.

## Quality trade-offs

Responsiveness trades against client complexity, rollback risk, and the clarity of authoritative completion.

## Claim map

- HTTP-CONDITION: HTTP conditional requests support version-based lost-update prevention.
- OPTIMISTIC-STATE: Optimistic UI needs a pending state and explicit failure handling.

## Volatile facts

Product versions, protocol/library support, service limits, pricing, licensing, and
security advisories must be rechecked in the cited official sources at decision time.
The mechanisms and decision criteria above are maintained separately from those facts.
