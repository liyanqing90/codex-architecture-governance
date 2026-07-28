---
id: domain.web-frontend
kind: domain
version: 1.0.0
status: active
domains:
- domain
triggers:
- web
- frontend
quality_attributes: []
related: []
legacy_ids:
- domain-guidance:web-frontend
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: stable-principles-plus-official-docs
sources:
- title: OpenAI Practical Guide to Building Agents
  url: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
  authority: official
---

# Web Frontend

## Problem and intent

- Govern UI state ownership
- server/client authority
- data fetching
- accessibility
- performance
- security
- and release boundaries.

## Mechanism

- Keep authoritative security and cross-client invariants on a trusted boundary.

## Fit when

- Browser applications contain stateful workflows or business orchestration.

## Avoid when

- Only static content is present.

## Required capabilities

- contract-validation
- performance-budgets
- accessibility

## Benefits

- Prevents duplicated authority and uncontrolled client complexity.

## Costs and liabilities

- Requires rendered
- network
- and accessibility evidence.

## Failure modes

- security-in-client-only
- duplicated-server-state

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
