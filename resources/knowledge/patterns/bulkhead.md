---
id: pattern.bulkhead
kind: pattern
version: 1.0.0
status: active
domains:
- resilience
triggers:
- bulkhead
quality_attributes: []
related: []
legacy_ids:
- pattern:bulkhead
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Bulkhead

## Problem and intent

- Partition concurrency
- connections
- queues
- or capacity to contain failure.

## Mechanism

- Partition concurrency

## Fit when

- One workload can exhaust shared resources used by critical flows.

## Avoid when

- Workloads share identical priority and isolated pools would waste scarce capacity.

## Required capabilities

- workload-classification
- capacity-observability

## Benefits

- Bounds blast radius and preserves critical capacity.

## Costs and liabilities

- Capacity fragmentation and tuning complexity.

## Failure modes

- unbounded-default-pool
- static-partitions-without-data

## Alternatives

- backpressure
- rate-limit

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
