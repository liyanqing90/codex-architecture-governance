---
id: migration.shared-saas-to-cells
kind: migration-guide
version: 1.0.0
status: active
domains:
- scaling
triggers:
- shared
- saas
- cells
quality_attributes: []
related: []
legacy_ids:
- migration:shared-saas-to-cells
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Shared SaaS to Cells

## Problem and intent

- Introduce repeatable cells and route selected tenants while preserving global control-plane integrity.

## Mechanism

- Prove one repeatable cell before partitioning the tenant base.

## Fit when

- Failure containment or capacity evidence justifies duplicated data planes.

## Avoid when

- Service or database scaling resolves the proven bottleneck.

## Required capabilities

- tenant-placement
- fleet-automation
- cell-routing
- data-movement

## Benefits

- Bounded blast radius and incremental scale.

## Costs and liabilities

- Tenant moves
- routing
- duplicated infrastructure
- global dependencies
- and fleet operations.

## Failure modes

- global-data-plane-dependency
- snowflake-cells

## Alternatives

- Keep the current design and apply a smaller local correction.

## Migration and exit

- define-cell-contract
- automate-empty-cell
- route-pilot-tenants
- rehearse-move
- scale-fleet

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
