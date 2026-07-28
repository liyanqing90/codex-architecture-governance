---
id: style.layered-monolith
kind: architecture-style
version: 1.0.0
status: active
domains:
- application
triggers:
- layered
- monolith
quality_attributes: []
related: []
legacy_ids:
- architecture-style:layered-monolith
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Layered Monolith

## Problem and intent

- Keep deployment and transactions simple while separating presentation
- application
- domain
- and infrastructure concerns.

## Mechanism

- Keep deployment and transactions simple while separating presentation

## Fit when

- One team owns the system and modules do not need independent deployment.

## Avoid when

- Changes repeatedly cross unrelated domains or independent scaling and release are proven requirements.

## Required capabilities

- dependency-direction
- transaction-ownership

## Benefits

- Simple deployment
- debugging
- and transaction boundaries.

## Costs and liabilities

- Horizontal layers can obscure domain ownership.

## Failure modes

- shared-data-access
- cross-domain-change

## Alternatives

- language-packages
- dependency-rules

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
