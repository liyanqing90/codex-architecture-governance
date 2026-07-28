---
id: reference.cell-based-saas
kind: reference-architecture
version: 1.0.0
status: active
domains:
- high-scale
triggers:
- cell
- based
- saas
quality_attributes: []
related: []
legacy_ids:
- reference-architecture:cell-based-saas
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Cell-Based SaaS

## Problem and intent

- Route tenants into repeatable cells with local services and data so capacity and failure blast radius remain bounded.

## Mechanism

- Introduce cells only after service-level failure containment is insufficient.

## Fit when

- Scale or tenant isolation exceeds what one shared stack can safely provide.

## Avoid when

- Duplicated infrastructure and routing operations exceed demonstrated reliability value.

## Required capabilities

- cell-routing
- tenant-placement
- fleet-automation
- data-partitioning
- cell-slo

## Benefits

- Bounded incidents
- incremental capacity
- and per-cell rollout.

## Costs and liabilities

- Fleet automation
- tenant placement
- cross-cell operations
- balancing
- and cost.

## Failure modes

- cross-cell-writes
- manually-different-cells

## Alternatives

- regional-cells
- tenant-cells

## Migration and exit

- shared-saas-to-cells

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
