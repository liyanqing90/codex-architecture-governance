---
id: reference.cloud-native-service-platform
kind: reference-architecture
version: 1.0.0
status: active
domains:
- platform
triggers:
- cloud
- native
- service
- platform
quality_attributes: []
related: []
legacy_ids:
- reference-architecture:cloud-native-service-platform
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Cloud-Native Service Platform

## Problem and intent

- Provide self-service workload deployment
- identity
- telemetry
- policy
- secrets
- progressive delivery
- and recovery contracts.

## Mechanism

- Build a platform around repeated consumer jobs
- not infrastructure fashion.

## Fit when

- Several teams repeatedly need the same owned operational capabilities.

## Avoid when

- Managed hosting and repository automation satisfy current delivery needs.

## Required capabilities

- platform-product-owner
- service-catalog
- workload-identity
- opentelemetry
- progressive-delivery

## Benefits

- Consistent controls
- reduced service setup cost
- and observable ownership.

## Costs and liabilities

- Platform product ownership
- paved-road limits
- upgrades
- fleet cost
- and abstraction leakage.

## Failure modes

- platform-without-consumer-research
- kubernetes-exposed-as-product

## Alternatives

- kubernetes
- managed-containers
- service-mesh

## Migration and exit

- golden-path-pilot

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
