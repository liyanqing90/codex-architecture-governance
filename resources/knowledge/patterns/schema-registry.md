---
id: pattern.schema-registry
kind: pattern
version: 1.0.0
status: active
domains:
- messaging
triggers:
- schema
- registry
quality_attributes: []
related: []
legacy_ids:
- pattern:schema-registry
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Schema Registry

## Problem and intent

- Govern versioned message schemas
- compatibility rules
- producers
- consumers
- and serialization identifiers.

## Mechanism

- Govern versioned message schemas

## Fit when

- Independent producers and consumers exchange durable or replayable records.

## Avoid when

- One atomic deployment owns a private transient message.

## Required capabilities

- consumer-inventory
- compatibility-policy
- ownership

## Benefits

- Machine compatibility checks and discoverable contract history.

## Costs and liabilities

- Registry availability
- policy selection
- generated-code coupling
- and semantic gaps.

## Failure modes

- structural-only-compatibility
- unmanaged-subject-names

## Alternatives

- repository-contracts

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
