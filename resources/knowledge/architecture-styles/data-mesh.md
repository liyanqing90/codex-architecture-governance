---
id: style.data-mesh
kind: architecture-style
version: 1.0.0
status: active
domains:
- organization-data
triggers:
- data
- mesh
quality_attributes: []
related: []
legacy_ids:
- architecture-style:data-mesh
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Data Mesh

## Problem and intent

- Distribute analytical data ownership to domains while governing interoperable data products through a self-service platform.

## Mechanism

- Distribute analytical data ownership to domains while governing interoperable data products through a self-service platform.

## Fit when

- Many autonomous domains create and consume analytical data and centralized ownership is the proven bottleneck.

## Avoid when

- A small organization or centralized platform can meet needs without duplicated governance.

## Required capabilities

- domain-ownership
- data-product-contracts
- self-service-platform
- federated-governance

## Benefits

- Domain accountability
- scalable ownership
- and product-oriented data contracts.

## Costs and liabilities

- Federated governance
- platform investment
- duplicated skills
- interoperability
- and organization change.

## Failure modes

- mesh-as-tool-purchase
- products-without-consumers

## Alternatives

- federated-data-products

## Migration and exit

- pilot-domain-data-product

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
