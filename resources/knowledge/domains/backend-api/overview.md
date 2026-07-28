---
id: domain.backend-api
kind: domain
version: 1.0.0
status: active
domains:
- domain
triggers:
- backend
- api
quality_attributes: []
related: []
legacy_ids:
- domain-guidance:backend-api
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: stable-principles-plus-official-docs
sources:
- title: OpenAI Practical Guide to Building Agents
  url: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
  authority: official
---

# Backend API Services

## Problem and intent

- Govern public contracts
- resource authorization
- transaction ownership
- overload
- dependency failure
- and compatibility.

## Mechanism

- Select synchronous APIs only when caller deadlines and coupling are acceptable.

## Fit when

- A service exposes HTTP
- RPC
- GraphQL
- webhook
- or other consumer-facing operations.

## Avoid when

- No network contract is in scope.

## Required capabilities

- backend-api
- contract-tests
- rate-limits

## Benefits

- Connects transport behavior with authoritative business boundaries.

## Costs and liabilities

- Requires consumer inventory and runtime traffic evidence.

## Failure modes

- transport-owned-domain
- undocumented-errors

## Alternatives

- Keep the current design and apply a smaller local correction.

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
