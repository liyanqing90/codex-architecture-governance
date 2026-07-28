---
id: reference.multi-tenant-saas
kind: reference-architecture
version: 1.0.0
status: active
domains:
- service
triggers:
- multi
- tenant
- saas
quality_attributes: []
related: []
legacy_ids:
- reference-architecture:multi-tenant-saas
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Multi-Tenant SaaS

## Problem and intent

- Bind tenant identity to authorization
- data partitioning
- background work
- observability
- export
- deletion
- and cost attribution.

## Mechanism

- Choose isolation level from threat
- scale
- and operations evidence.

## Fit when

- One product serves multiple organizations with controlled isolation.

## Avoid when

- Dedicated instances are required by regulation or operational boundaries.

## Required capabilities

- tenant-context
- authorization
- data-isolation
- quotas
- audit

## Benefits

- Shared delivery and efficient platform operations.

## Costs and liabilities

- Isolation failures
- noisy neighbors
- migrations
- and tenant-aware operations.

## Failure modes

- optional-tenant-filter
- shared-admin-authority

## Alternatives

- shared-schema
- schema-per-tenant
- database-per-tenant

## Migration and exit

- single-tenant-to-multi-tenant

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
