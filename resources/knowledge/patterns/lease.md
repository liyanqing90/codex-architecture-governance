---
id: pattern.lease
kind: pattern
version: 1.0.0
status: active
domains:
- coordination
triggers:
- lease
quality_attributes: []
related: []
legacy_ids:
- pattern:lease
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Lease

## Problem and intent

- Grant temporary ownership that expires unless renewed.

## Mechanism

- Grant temporary ownership that expires unless renewed.

## Fit when

- Distributed workers need recoverable exclusive responsibility.

## Avoid when

- A local lock or partition ownership already provides the invariant.

## Required capabilities

- fencing-token
- monotonic-time
- expiry-observability

## Benefits

- Ownership can recover after failure.

## Costs and liabilities

- Clock assumptions
- renewal
- fencing
- and split-brain.

## Failure modes

- lease-without-fencing
- work-past-expiry

## Alternatives

- leader-election

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
