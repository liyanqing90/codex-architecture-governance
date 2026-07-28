---
id: technology.aws-sqs
kind: technology-profile
version: 1.0.0
status: active
domains:
- managed-queue
triggers:
- aws
- sqs
quality_attributes: []
related: []
legacy_ids:
- technology-profile:aws-sqs
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: Amazon SQS Developer Guide
  url: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html
  authority: official
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project
  decision.
---

# Amazon SQS

## Problem and intent

- Provide managed standard or FIFO message queues with visibility timeouts
- redelivery
- and dead-letter routing.

## Mechanism

- Provide managed standard or FIFO message queues with visibility timeouts

## Fit when

- AWS-hosted workers need durable queues without broker operations.

## Avoid when

- Complex routing
- streaming replay
- or cloud portability dominates.

## Required capabilities

- idempotent-consumers
- queue-observability
- aws-identity

## Benefits

- Managed availability
- scaling
- and queue operations.

## Costs and liabilities

- At-least-once semantics
- visibility tuning
- quotas
- payload limits
- and AWS lock-in.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

## Alternatives

- rabbitmq
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
