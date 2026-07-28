---
id: reference.real-time-stream-processing
kind: reference-architecture
version: 1.0.0
status: active
domains:
- data
triggers:
- real
- time
- stream
- processing
quality_attributes: []
related: []
legacy_ids:
- reference-architecture:real-time-stream-processing
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Real-Time Stream Processing

## Problem and intent

- Partition ordered event streams into stateful processors with checkpoints
- watermarks
- replay
- and controlled outputs.

## Mechanism

- Do not adopt streaming without a measurable freshness requirement.

## Fit when

- Continuous processing with bounded event-time latency is a product requirement.

## Avoid when

- Batch processing meets freshness targets.

## Required capabilities

- partition-key
- schema-registry
- checkpoints
- watermark-policy
- replay
- backpressure

## Benefits

- Continuous derived state and scalable partition-aligned processing.

## Costs and liabilities

- Time semantics
- late data
- state recovery
- backpressure
- and operational complexity.

## Failure modes

- processing-time-used-as-event-time
- side-effects-without-idempotency

## Alternatives

- apache-kafka
- apache-pulsar
- managed-stream-processing

## Migration and exit

- batch-to-incremental-stream

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
