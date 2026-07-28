---
id: technology.rabbitmq
kind: technology-profile
version: 1.0.0
status: active
domains:
- message-broker
triggers:
- rabbitmq
quality_attributes: []
related: []
legacy_ids:
- technology-profile:rabbitmq
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: RabbitMQ Documentation
  url: https://www.rabbitmq.com/docs
  authority: official
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project
  decision.
---

# RabbitMQ

## Problem and intent

- Route and deliver queued messages with acknowledgements
- exchanges
- consumer control
- and broker-managed durability.

## Mechanism

- Route and deliver queued messages with acknowledgements

## Fit when

- Work queues or flexible routing matter more than long-term replayable logs.

## Avoid when

- A managed queue is sufficient or retained high-throughput event replay is central.

## Required capabilities

- broker-operations
- idempotent-consumers
- topology-governance

## Benefits

- Rich routing
- delivery controls
- and mature work-queue semantics.

## Costs and liabilities

- Cluster operations
- queue topology
- ordering
- backpressure
- redelivery
- and storage limits.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

## Alternatives

- aws-sqs
- kafka

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
