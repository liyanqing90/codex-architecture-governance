---
id: domain.financial-trading
kind: domain
version: 1.0.0
status: active
domains:
- domain
triggers:
- financial
- trading
quality_attributes: []
related: []
legacy_ids:
- domain-guidance:financial-trading
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: stable-principles-plus-official-docs
sources:
- title: OpenAI Practical Guide to Building Agents
  url: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
  authority: official
---

# Financial Trading Systems

## Problem and intent

- Govern market-data provenance
- pre-trade limits
- order state
- strategy isolation
- reconciliation
- and audit.

## Mechanism

- Models may inform decisions but cannot own authoritative risk limits.

## Fit when

- The system submits
- manages
- simulates
- or recommends financially consequential orders.

## Avoid when

- No financial position or execution side effect is possible.

## Required capabilities

- financial-trading
- deterministic-risk
- reconciliation

## Benefits

- Places deterministic risk controls before irreversible action.

## Costs and liabilities

- Requires venue-specific
- regulatory
- and operational validation.

## Failure modes

- model-direct-to-order
- stale-position-state

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
