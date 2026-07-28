---
id: style.cell-based
kind: architecture-style
version: 1.0.0
status: active
domains:
- application
triggers:
- cell
- based
quality_attributes: []
related: []
legacy_ids:
- architecture-style:cell-based
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Cell-Based Architecture

## Problem and intent

- Partition workloads into repeatable cells with bounded blast radius and independent capacity.

## Mechanism

- Partition workloads into repeatable cells with bounded blast radius and independent capacity.

## Fit when

- Large scale or tenant isolation requires failure containment beyond service boundaries.

## Avoid when

- Scale and operational maturity do not justify duplicated stacks and routing.

## Required capabilities

- cell-routing
- automation
- data-partitioning
- fleet-observability

## Benefits

- Bounded failures
- incremental scale
- and tenant isolation.

## Costs and liabilities

- Routing
- duplicated infrastructure
- balancing
- and cross-cell operations.

## Failure modes

- cross-cell-writes
- manual-cell-operations

## Alternatives

- regional-cells
- tenant-cells

## Migration and exit

- microservices

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
