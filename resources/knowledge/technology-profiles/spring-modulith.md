---
id: technology.spring-modulith
kind: technology-profile
version: 1.0.0
status: active
domains:
- modularity
triggers:
- spring
- modulith
quality_attributes: []
related: []
legacy_ids:
- technology-profile:spring-modulith
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: Spring Modulith Reference
  url: https://docs.spring.io/spring-modulith/reference/index.html
  authority: official
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project
  decision.
---

# Spring Modulith

## Problem and intent

- Discover
- verify
- test
- document
- and observe functional modules in Spring Boot applications.

## Mechanism

- Discover

## Fit when

- A Java Spring Boot modular monolith needs deterministic module boundaries.

## Avoid when

- The project is not Spring Boot or independent service deployment is already required.

## Required capabilities

- spring-boot
- domain-modules

## Benefits

- Module verification
- module tests
- documentation
- events
- and observability.

## Costs and liabilities

- Spring-specific model and adoption constraints.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

## Alternatives

- archunit

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
