---
id: technology.apache-pulsar
kind: technology-profile
version: 1.0.0
status: active
domains:
- event-streaming
triggers:
- apache
- pulsar
quality_attributes: []
related: []
legacy_ids:
- technology-profile:apache-pulsar
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: Apache Pulsar Documentation
  url: https://pulsar.apache.org/docs/
  authority: official
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project
  decision.
---

# Apache Pulsar

## Problem and intent

- Provide durable pub-sub and queue semantics with segmented storage
- subscriptions
- retention
- and multi-tenancy.

## Mechanism

- Provide durable pub-sub and queue semantics with segmented storage

## Fit when

- Streaming and messaging coexist and the team can operate or procure the Pulsar platform.

## Avoid when

- A simpler queue or established Kafka ecosystem already meets needs.

## Required capabilities

- platform-operations
- event-governance
- idempotent-consumers

## Benefits

- Flexible subscriptions
- separated compute and storage
- and geo-replication capabilities.

## Costs and liabilities

- Operational topology
- ecosystem maturity tradeoffs
- schema
- partitions
- and cost.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

## Alternatives

- apache-kafka
- rabbitmq

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
