---
id: domain.identity
kind: domain
version: 1.0.0
status: active
domains:
- domain
triggers:
- identity
quality_attributes: []
related: []
legacy_ids:
- domain-guidance:identity
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: stable-principles-plus-official-docs
sources:
- title: OpenAI Practical Guide to Building Agents
  url: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
  authority: official
---

# Identity and Authorization

## Problem and intent

- Govern principals
- authentication
- authorization
- sessions
- delegation
- audit
- recovery
- and tenant isolation.

## Mechanism

- Centralize semantics only when trust
- lifecycle
- and availability requirements align.

## Fit when

- Any protected resource or cross-system identity exists.

## Avoid when

- No identity or protected operation is present.

## Required capabilities

- threat-model
- audit
- least-privilege

## Benefits

- Clarifies trust and authority boundaries.

## Costs and liabilities

- Key lifecycle
- policy complexity
- and recovery risk.

## Failure modes

- role-string-sprawl
- client-only-authorization

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
