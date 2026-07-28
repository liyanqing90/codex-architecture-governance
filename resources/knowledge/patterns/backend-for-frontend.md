---
id: pattern.backend-for-frontend
kind: pattern
version: 1.0.0
status: active
domains:
- integration
triggers:
- backend
- for
- frontend
quality_attributes: []
related: []
legacy_ids:
- pattern:backend-for-frontend
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Backend for Frontend

## Problem and intent

- Provide client-specific aggregation and adaptation while keeping authoritative rules in owned services.

## Mechanism

- Provide client-specific aggregation and adaptation while keeping authoritative rules in owned services.

## Fit when

- Clients have materially different interaction and data-shaping needs.

## Avoid when

- One API serves all clients without harmful coupling.

## Required capabilities

- client-ownership
- contract-governance

## Benefits

- Client autonomy and fewer chatty calls.

## Costs and liabilities

- Duplicated orchestration and additional operational surface.

## Failure modes

- business-authority-in-bff
- duplicated-core-rules

## Alternatives

- api-gateway

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
