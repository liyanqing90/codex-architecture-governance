---
id: technology.dependency-cruiser
kind: technology-profile
version: 1.0.0
status: active
domains:
- architecture-testing
triggers:
- dependency
- cruiser
quality_attributes: []
related: []
legacy_ids:
- technology-profile:dependency-cruiser
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: dependency-cruiser
  url: https://github.com/sverweij/dependency-cruiser
  authority: maintainer
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project
  decision.
---

# dependency-cruiser

## Problem and intent

- Validate JavaScript and TypeScript dependency rules
- cycles
- and forbidden boundaries.

## Mechanism

- Validate JavaScript and TypeScript dependency rules

## Fit when

- JS or TS module paths express meaningful architecture boundaries.

## Avoid when

- Runtime contracts and data ownership are the actual concern.

## Required capabilities

- node-project

## Benefits

- Fast deterministic dependency evidence.

## Costs and liabilities

- Configuration can drift from intended domain ownership.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

## Alternatives

- nx-boundaries

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
