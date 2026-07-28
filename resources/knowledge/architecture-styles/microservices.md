---
id: style.microservices
kind: architecture-style
version: 1.0.0
status: active
domains:
- application
triggers:
- microservices
quality_attributes: []
related: []
legacy_ids:
- architecture-style:microservices
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Microservices

## Problem and intent

- Align independently owned
- deployed
- scaled
- and isolated services with stable business capabilities.

## Mechanism

- Align independently owned

## Fit when

- Multiple autonomous teams have proven independent release or scaling needs and mature operations.

## Avoid when

- One team owns an unstable domain or distributed operations are immature.

## Required capabilities

- service-ownership
- ci-cd
- tracing
- contract-governance
- eventual-consistency

## Benefits

- Independent deployment
- scaling
- ownership
- and fault containment.

## Costs and liabilities

- Distributed consistency
- observability
- compatibility
- platform
- and on-call cost.

## Failure modes

- shared-database-writers
- coordinated-releases
- chatty-calls

## Alternatives

- containers
- managed-services

## Migration and exit

- cell-based

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
