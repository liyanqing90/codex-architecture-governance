---
id: style.hexagonal
kind: architecture-style
version: 1.0.0
status: active
domains:
- application
triggers:
- hexagonal
quality_attributes: []
related: []
legacy_ids:
- architecture-style:hexagonal
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Hexagonal Architecture

## Problem and intent

- Keep long-lived domain policy independent of delivery and infrastructure through ports and adapters.

## Mechanism

- Keep long-lived domain policy independent of delivery and infrastructure through ports and adapters.

## Fit when

- Core domain logic is complex and external dependencies need isolation or replacement.

## Avoid when

- The system is short-lived CRUD with no meaningful domain or replacement boundary.

## Required capabilities

- domain-boundary
- adapter-ownership

## Benefits

- Testable domain logic and explicit external boundaries.

## Costs and liabilities

- Unnecessary ports create indirection and empty abstractions.

## Failure modes

- framework-types-in-domain
- one-implementation-interfaces

## Alternatives

- ports-and-adapters
- dependency-inversion

## Migration and exit

- modular-monolith

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
