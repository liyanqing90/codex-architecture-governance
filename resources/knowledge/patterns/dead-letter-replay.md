---
id: pattern.dead-letter-replay
kind: pattern
version: 1.0.0
status: active
domains:
- messaging
triggers:
- dead
- letter
- replay
quality_attributes: []
related: []
legacy_ids:
- pattern:dead-letter-replay
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Dead Letter and Replay

## Problem and intent

- Quarantine repeatedly failing messages with complete context and provide authorized
- idempotent replay.

## Mechanism

- Quarantine repeatedly failing messages with complete context and provide authorized

## Fit when

- Poison messages must not block progress and operators can repair or classify failures.

## Avoid when

- Dead lettering would silently discard required work without ownership.

## Required capabilities

- failure-classification
- retention
- replay-authorization
- idempotency

## Benefits

- Failure isolation and recoverable operations.

## Costs and liabilities

- Unbounded queues
- stale data
- privacy retention
- replay duplication
- and operational backlog.

## Failure modes

- write-only-dlq
- replay-without-version-binding

## Alternatives

- parking-lot-queue
- terminal-failure-state

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
