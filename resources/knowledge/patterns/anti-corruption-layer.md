---
id: pattern.anti-corruption-layer
kind: pattern
version: 1.0.0
status: active
domains:
- integration
triggers:
- anti
- corruption
- layer
quality_attributes: []
related: []
legacy_ids:
- pattern:anti-corruption-layer
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Anti-Corruption Layer

## Problem and intent

- Translate an external or legacy model into a bounded internal model.

## Mechanism

- Translate an external or legacy model into a bounded internal model.

## Fit when

- External semantics would otherwise leak into core policy.

## Avoid when

- Models already align and translation would only rename fields.

## Required capabilities

- contract-owner
- translation-tests

## Benefits

- Protects domain language and change boundaries.

## Costs and liabilities

- Mapping
- error handling
- and semantic drift.

## Failure modes

- pass-through-layer
- hidden-lossy-mapping

## Alternatives

- direct-integration

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
