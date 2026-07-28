---
id: domain.multi-tenant-saas
kind: domain
version: 1.0.0
status: active
domains:
- domain
triggers:
- multi
- tenant
- saas
quality_attributes: []
related: []
legacy_ids:
- domain-guidance:multi-tenant-saas
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: stable-principles-plus-official-docs
sources:
- title: OpenAI Practical Guide to Building Agents
  url: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
  authority: official
---

# Multi-Tenant SaaS

## Problem and intent

- Govern tenant context
- isolation
- quotas
- noisy neighbors
- migrations
- export
- deletion
- and support authority.

## Mechanism

- Select isolation tier from threat
- scale
- cost
- and operational maturity.

## Fit when

- One service hosts multiple independent organizations.

## Avoid when

- Regulation or operations require dedicated deployments.

## Required capabilities

- tenant-aware-auth
- data-partitioning
- quotas
- audit

## Benefits

- Efficient shared product delivery.

## Costs and liabilities

- Isolation failure has portfolio-wide impact.

## Failure modes

- optional-tenant-filter
- global-admin-bypass

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
