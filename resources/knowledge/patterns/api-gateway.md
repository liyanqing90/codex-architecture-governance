---
id: pattern.api-gateway
kind: pattern
version: 1.0.0
status: active
domains:
- integration
triggers:
- api
- gateway
quality_attributes: []
related: []
legacy_ids:
- pattern:api-gateway
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# API Gateway

## Problem and intent

- Provide a governed external ingress for routing
- authentication integration
- throttling
- protocol adaptation
- and observability.

## Mechanism

- Provide a governed external ingress for routing

## Fit when

- Multiple services need consistent edge policy or client-facing composition.

## Avoid when

- One service already provides a coherent boundary or the gateway would own domain policy.

## Required capabilities

- high-availability
- configuration-governance
- trace-propagation

## Benefits

- Central edge controls and stable client entry point.

## Costs and liabilities

- Bottleneck
- failure domain
- policy coupling
- and hidden orchestration.

## Failure modes

- business-logic-in-gateway
- gateway-shared-database

## Alternatives

- backend-for-frontend
- direct-service-ingress

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
