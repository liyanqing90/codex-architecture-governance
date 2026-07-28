---
id: technology.archunit
kind: technology-profile
version: 1.0.0
status: active
domains:
- architecture-testing
triggers:
- archunit
quality_attributes: []
related: []
legacy_ids:
- technology-profile:archunit
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: ArchUnit User Guide
  url: https://www.archunit.org/userguide/html/000_Index.html
  authority: official
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project
  decision.
---

# ArchUnit

## Problem and intent

- Test Java package
- layer
- dependency
- cycle
- and API rules deterministically.

## Mechanism

- Test Java package

## Fit when

- Java bytecode boundaries can express architecture invariants.

## Avoid when

- Runtime ownership or behavior cannot be inferred from dependencies.

## Required capabilities

- java-tests

## Benefits

- Executable architecture constraints in ordinary tests.

## Costs and liabilities

- Static rules cannot prove runtime semantics.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

## Alternatives

- spring-modulith

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
