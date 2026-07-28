---
id: migration.layered-monolith-to-modular
kind: migration-guide
version: 1.0.0
status: active
domains:
- code-boundary
triggers:
- layered
- monolith
- modular
quality_attributes: []
related: []
legacy_ids:
- migration:layered-monolith-to-modular
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Layered Monolith to Modular Monolith

## Problem and intent

- Introduce module ownership and public APIs before changing deployment.

## Mechanism

- Stop before service extraction unless independent deployment value is proven.

## Fit when

- Change coupling is proven but one deployment remains appropriate.

## Avoid when

- Domain boundaries and ownership cannot yet be identified.

## Required capabilities

- module-map
- characterization-tests

## Benefits

- Reduces coupling with low operational change.

## Costs and liabilities

- Temporary adapters and boundary-test adoption.

## Failure modes

- directory-only-modules
- shared-writers

## Alternatives

- Keep the current design and apply a smaller local correction.

## Migration and exit

- inventory-dependencies
- define-apis
- enforce-boundaries
- migrate-writers
- remove-backdoors

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
