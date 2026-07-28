---
id: pattern.leader-election
kind: pattern
version: 1.0.0
status: active
domains:
- coordination
triggers:
- leader
- election
quality_attributes: []
related: []
legacy_ids:
- pattern:leader-election
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Leader Election

## Problem and intent

- Select one active coordinator for work that cannot safely run concurrently.

## Mechanism

- Select one active coordinator for work that cannot safely run concurrently.

## Fit when

- A distributed singleton responsibility is unavoidable and failover is required.

## Avoid when

- Work can be partitioned
- made idempotent
- or delegated to a managed scheduler.

## Required capabilities

- consensus-or-lease
- fencing-token
- health-observation

## Benefits

- Controlled singleton execution with failover.

## Costs and liabilities

- Split brain
- fencing
- election availability
- and coordinator bottleneck.

## Failure modes

- leader-without-fencing
- global-leader-for-partitionable-work

## Alternatives

- lease
- partition-ownership

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
