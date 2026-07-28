---
id: domain.mobile
kind: domain
version: 1.0.0
status: active
domains:
- domain
triggers:
- mobile
quality_attributes: []
related: []
legacy_ids:
- domain-guidance:mobile
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: stable-principles-plus-official-docs
sources:
- title: OpenAI Practical Guide to Building Agents
  url: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
  authority: official
---

# Mobile and Client Applications

## Problem and intent

- Govern local state
- lifecycle
- weak networks
- synchronization
- migration
- notifications
- privacy
- and energy.

## Mechanism

- Choose server-first
- cache
- or offline-first from explicit offline requirements.

## Fit when

- A mobile or desktop client persists state or performs background work.

## Avoid when

- Only a stateless web presentation is in scope.

## Required capabilities

- mobile-core
- migration-tests

## Benefits

- Connects platform lifecycle with data integrity and reliability.

## Costs and liabilities

- Runtime proof often requires devices and multiple app versions.

## Failure modes

- client-as-authority
- untested-upgrades

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
