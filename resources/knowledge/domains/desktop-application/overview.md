---
id: domain.desktop-application
kind: domain
version: 1.0.0
status: active
domains:
- domain
triggers:
- desktop
- application
quality_attributes: []
related: []
legacy_ids:
- domain-guidance:desktop-application
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: stable-principles-plus-official-docs
sources:
- title: OpenAI Practical Guide to Building Agents
  url: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
  authority: official
---

# Desktop Applications

## Problem and intent

- Govern local state
- updates
- OS integration
- IPC
- multi-instance behavior
- device privacy
- and recovery.

## Mechanism

- Keep privileged helpers minimal and authenticate local callers.

## Fit when

- A native desktop process owns user data or privileged OS interactions.

## Avoid when

- Only a browser application is in scope.

## Required capabilities

- desktop-application
- signed-updates
- upgrade-tests

## Benefits

- Connects application architecture to platform lifecycle.

## Costs and liabilities

- OS versions
- distribution channels
- and update paths expand compatibility.

## Failure modes

- privileged-unauthenticated-ipc
- destructive-update

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
