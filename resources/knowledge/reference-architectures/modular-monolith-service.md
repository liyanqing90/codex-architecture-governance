---
id: reference.modular-monolith-service
kind: reference-architecture
version: 1.0.0
status: active
domains:
- application
triggers:
- modular
- monolith
- service
quality_attributes: []
related: []
legacy_ids:
- reference-architecture:modular-monolith-service
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Modular Monolith Service

## Problem and intent

- Provide one deployment with domain modules
- module-owned writes
- public module APIs
- adapters
- and deterministic dependency tests.

## Mechanism

- Prefer this over microservices until independent deployment value is demonstrated.

## Fit when

- One or a few teams need clear boundaries without independent deployment.

## Avoid when

- Independent release
- fault isolation
- or regulatory separation is required.

## Required capabilities

- module-map
- code-ownership
- dependency-tests
- contract-tests

## Benefits

- Simple operations
- local transactions
- and controlled evolution.

## Costs and liabilities

- Shared process and capacity failure domain.

## Failure modes

- cross-module-writes
- shared-internal-types

## Alternatives

- spring-modulith
- archunit
- dependency-cruiser
- import-linter

## Migration and exit

- layered-monolith-to-modular

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
