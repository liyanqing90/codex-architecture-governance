---
id: style.modular-monolith
kind: architecture-style
version: 1.0.0
status: active
domains:
- application
triggers:
- modular
- monolith
quality_attributes: []
related: []
legacy_ids:
- architecture-style:modular-monolith
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Modular Monolith

## Problem and intent

- Retain one deployment while enforcing domain modules
- public APIs
- and controlled data writers.

## Mechanism

- Retain one deployment while enforcing domain modules

## Fit when

- A small number of teams need strong boundaries without independent deployment.

## Avoid when

- Modules require independent release
- scaling
- fault isolation
- or regulatory separation.

## Required capabilities

- module-ownership
- deterministic-dependency-rules
- module-tests

## Benefits

- Low operational cost with explicit evolution boundaries.

## Costs and liabilities

- Process and failure domain remain shared.

## Failure modes

- cross-module-internals
- shared-table-writers

## Alternatives

- spring-modulith
- archunit
- dependency-cruiser
- import-linter

## Migration and exit

- selective-microservices

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
