---
id: domain.local-first-application
kind: domain
version: 1.0.0
status: active
domains:
- domain
triggers:
- local
- first
- application
quality_attributes: []
related: []
legacy_ids:
- domain-guidance:local-first-application
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: stable-principles-plus-official-docs
sources:
- title: OpenAI Practical Guide to Building Agents
  url: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
  authority: official
---

# Local-First Applications

## Problem and intent

- Govern replicas
- convergence
- sync
- conflicts
- tombstones
- migrations
- storage
- and device privacy.

## Mechanism

- Require explicit product evidence before accepting local-first complexity.

## Fit when

- Users must create and modify durable state through prolonged disconnection.

## Avoid when

- Server authority plus a display cache satisfies offline requirements.

## Required capabilities

- local-first
- sync-protocol
- migration-matrix

## Benefits

- Continuous local work and user resilience.

## Costs and liabilities

- Distributed data semantics move into every client.

## Failure modes

- implicit-last-write-wins
- missing-delete-sync

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
