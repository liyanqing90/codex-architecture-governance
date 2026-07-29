---
id: pattern.outbox
kind: pattern
version: 2.0.0
status: active
domains:
- data-messaging
triggers:
- outbox
quality_attributes: []
related:
- decision.message-system-selection
- style.durable-workflow
legacy_ids:
- pattern:outbox
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Transactional Outbox sample
  url: https://learn.microsoft.com/en-us/samples/azure-samples/cosmos-db-design-patterns/transactional-outbox/
  authority: official
  supports:
  - OUTBOX-ATOMIC
  - OUTBOX-DELIVERY
maturity: golden
curation:
  method: assisted-reviewed
  reviewer: Codex Architecture Governance review
  reviewed_at: '2026-07-28'
---

# Transactional Outbox

## Problem and intent

Prevent a committed domain change and its external message from diverging because two independent writes cannot be made atomic.

## Mechanism

Insert an immutable event envelope beside the aggregate update, commit both, relay only committed rows, retry publication, and record or infer progress without deleting evidence before retention and replay needs are met.

## Operating model

The domain update and an outbox record commit in one local database transaction. A separate relay claims committed outbox rows and publishes them at least once; consumers deduplicate by stable message or business key.

## Fit when

One service owns both the state change and an event/command that must eventually reach an external broker or consumer.

## Avoid when

There is no external publication, the operation is already one atomic broker transaction, or change-data capture reliably provides the required event semantics.

## Required capabilities

Single local transaction, immutable event ID, partition/order key, relay lease, bounded retry, idempotent consumers, lag/oldest-row metrics, retention, replay, and schema compatibility.

## Benefits

Eliminates lost events between database commit and broker publish while allowing relay recovery after crashes.

## Costs and liabilities

Publication is eventually consistent and may duplicate; the table, relay, retention, and consumer idempotency require operations.

## Failure modes

Writing the outbox outside the aggregate transaction, marking published before broker acknowledgement, concurrent relays breaking order, unbounded table growth, and consumers assuming exactly once.

## Alternatives

Use database change-data capture when the log contains sufficient business semantics, broker-native transactions inside one supported boundary, or keep the operation local.

## Migration and exit

Add the outbox table and envelope, dual-observe current direct publication and relay counts without double effects, inject crashes after commit and publish, then remove direct publication after reconciliation is clean.

## Evidence to inspect

Transaction boundary, direct broker writes, crash window, relay claim/update logic, oldest unrelayed row, duplicate rate, consumer dedupe, ordering scope, and cleanup/replay tests.

## Evidence that changes the recommendation

Do not introduce an outbox when no dual write exists; choose CDC when it offers owned event transformation and equivalent recovery with less application code.

## Quality trade-offs

Reliability of state-to-message handoff trades against lag, duplicates, storage, and relay complexity.

## Claim map

- OUTBOX-ATOMIC: State and event are recorded atomically in one local transaction.
- OUTBOX-DELIVERY: The relay is replayable and consumers must tolerate at-least-once delivery.

## Volatile facts

Runtime versions, limits, compatibility, security advisories, pricing, and licensing
must be confirmed from the cited official source at decision time. The stable operating
mechanism remains distinct from those current facts.
