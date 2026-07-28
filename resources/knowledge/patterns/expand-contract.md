---
id: pattern.expand-contract
kind: pattern
version: 1.0.0
status: active
domains:
- migration
triggers:
- expand
- contract
quality_attributes: []
related: []
legacy_ids:
- pattern:expand-contract
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Expand and Contract

## Problem and intent

- Introduce a compatible contract
- migrate producers and consumers
- then remove the old shape.

## Mechanism

- Introduce a compatible contract

## Fit when

- Schemas
- APIs
- or persisted data must change across mixed versions.

## Avoid when

- There is one atomic deployment with no persisted compatibility.

## Required capabilities

- consumer-inventory
- compatibility-tests
- removal-gate

## Benefits

- Supports rolling and reversible migration.

## Costs and liabilities

- Temporary dual semantics and cleanup discipline.

## Failure modes

- same-release-contraction
- unknown-consumers

## Alternatives

- versioned-contract

## Migration and exit

- Introduce the mechanism behind a compatible boundary, verify it, then remove the old path.

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
