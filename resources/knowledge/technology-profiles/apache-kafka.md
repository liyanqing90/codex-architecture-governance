---
id: technology.apache-kafka
kind: technology-profile
version: 1.0.0
status: active
domains:
- event-streaming
triggers:
- apache
- kafka
quality_attributes: []
related: []
legacy_ids:
- technology-profile:apache-kafka
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: Apache Kafka Documentation
  url: https://kafka.apache.org/documentation/
  authority: official
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project
  decision.
---

# Apache Kafka

## Problem and intent

- Provide partitioned durable event logs with consumer offsets
- retention
- replay
- and stream processing integrations.

## Mechanism

- Provide partitioned durable event logs with consumer offsets

## Fit when

- Multiple independent consumers
- replay
- ordering by key
- and sustained event throughput are core needs.

## Avoid when

- A simple work queue or direct API meets the requirement.

## Required capabilities

- event-governance
- partition-key
- idempotent-consumers
- platform-operations

## Benefits

- Durable replayable logs
- consumer autonomy
- and scalable partitioned throughput.

## Costs and liabilities

- Partition design
- schema governance
- lag
- cluster operations
- rebalancing
- and semantic complexity.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

## Alternatives

- apache-pulsar
- rabbitmq
- aws-sqs

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
