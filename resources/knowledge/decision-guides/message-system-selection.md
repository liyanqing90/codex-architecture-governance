---
id: decision.message-system-selection
kind: decision-guide
version: 2.0.0
status: active
domains:
- distributed-systems
triggers:
- queue
- stream
- pubsub
quality_attributes:
- maintainability
related:
- pattern.outbox
- decision.sync-vs-async
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Competing Consumers pattern
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/competing-consumers
  authority: official
  supports:
  - QUEUE-SEMANTIC
- title: Azure asynchronous messaging options
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/messaging
  authority: official
  supports:
  - MESSAGE-CHOICE
maturity: golden
curation:
  method: assisted-reviewed
  reviewer: Codex Architecture Governance review
  reviewed_at: '2026-07-28'
---

# Message System Selection

## Problem and intent

Choose queue, publish/subscribe, or durable stream semantics from ownership, delivery, ordering, replay, fan-out, and recovery needs.

## Mechanism

A queue assigns work to one consumer group, pub/sub distributes notifications to subscribers, and a stream retains ordered records for independent cursor-based consumption. The application must still define idempotency and business ordering.

## Options

### Work queue

- Fit: Each command should be processed by one scalable consumer pool.
- Avoid: Every subscriber needs an independent copy or replay.
- Cost: Visibility/lease tuning, retries, and dead letters.
- Failure: Poison work loops or visibility expiry causes concurrent effects.
### Publish/subscribe

- Fit: Several consumers react independently to an event.
- Avoid: Consumers need long retention or arbitrary historical replay.
- Cost: Subscription lifecycle, schema compatibility, and fan-out cost.
- Failure: A missing subscription silently loses events.
### Durable event stream

- Fit: Replay, audit, ordered partition history, or many independent consumers are required.
- Avoid: The workload is a simple task queue with no replay value.
- Cost: Partition/key design, retention, consumer lag, and heavier operations.
- Failure: Hot partitions or incorrect offsets cause lag, gaps, or duplication.

## Fit when

At least one named option fits a measured quality scenario and the team can own its
required failure and recovery behavior.

## Avoid when

The choice is driven only by a technology name, hypothetical scale, or a problem
already solved by the current design.

## Required capabilities

Message ownership, schema/version policy, delivery guarantee, idempotent consumers, ordering key, retry and dead-letter policy, retention, backpressure, lag/age monitoring, and access control.

## Benefits

Prevents broker brand selection from substituting for delivery and recovery semantics.

## Costs and liabilities

Durability and fan-out increase storage and operational burden; simple queues limit replay and broadcast.

## Failure modes

Assuming exactly-once business effects, global ordering without partition cost, retry storms, unbounded lag, oversized payloads, and incompatible event changes.

## Alternatives

Compare the current design and the named options—Work queue, Publish/subscribe, Durable event stream—against the same
quality scenarios; do not compare feature lists without operating consequences.

## Migration and exit

Document current producer/consumer semantics, introduce an adapter and versioned envelope, shadow-consume without side effects, compare counts and ordering, then migrate one consumer group at a time.

## Evidence to inspect

Producer and consumer graph, throughput/burst, payload size, ordering scope, replay window, retry distribution, poison rate, lag SLO, and team operations.

## Evidence that changes the recommendation

Prefer a queue for work distribution, pub/sub for live fan-out, and a retained stream only when replay or independent history has measurable value.

## Quality trade-offs

Replay, ordering, delivery isolation, latency, simplicity, and storage cost vary by semantic model.

## Claim map

- QUEUE-SEMANTIC: Competing consumers distribute queued work across a consumer pool.
- MESSAGE-CHOICE: Message brokers and event streaming platforms expose different delivery and retention trade-offs.

## Volatile facts

Product versions, protocol/library support, service limits, pricing, licensing, and
security advisories must be rechecked in the cited official sources at decision time.
The mechanisms and decision criteria above are maintained separately from those facts.
