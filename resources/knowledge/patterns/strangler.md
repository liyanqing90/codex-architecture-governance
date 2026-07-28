---
id: pattern.strangler
kind: pattern
version: 1.0.0
status: active
domains:
- migration
triggers:
- strangler
quality_attributes: []
related: []
legacy_ids:
- pattern:strangler
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Strangler Fig

## Problem and intent

- Replace a legacy capability incrementally behind a routing or compatibility boundary.

## Mechanism

- Replace a legacy capability incrementally behind a routing or compatibility boundary.

## Fit when

- A big-bang replacement is too risky and behavior can be partitioned.

## Avoid when

- No stable routing seam exists or dual operation costs exceed migration risk.

## Required capabilities

- traffic-routing
- compatibility-tests
- observability

## Benefits

- Reversible incremental migration.

## Costs and liabilities

- Dual paths
- routing
- data ownership transition
- and prolonged complexity.

## Failure modes

- permanent-dual-path
- unclear-data-owner

## Alternatives

- branch-by-abstraction

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
