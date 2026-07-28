---
id: reference.offline-first-mobile
kind: reference-architecture
version: 1.0.0
status: active
domains:
- mobile
triggers:
- offline
- first
- mobile
quality_attributes: []
related: []
legacy_ids:
- reference-architecture:offline-first-mobile
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Offline-First Mobile

## Problem and intent

- Use a local authoritative working copy
- durable outbox
- versioned sync protocol
- conflicts
- tombstones
- and background reconciliation.

## Mechanism

- Do not choose offline-first solely for perceived responsiveness.

## Fit when

- Prolonged offline editing is a core user requirement.

## Avoid when

- Server authority plus cache meets offline display needs.

## Required capabilities

- local-database
- migration-tests
- sync-cursor
- outbox
- conflict-policy

## Benefits

- Continuous user work through disconnection.

## Costs and liabilities

- Conflict policy
- multi-device convergence
- deletion
- migration
- and battery cost.

## Failure modes

- silent-last-write-wins
- no-tombstones

## Alternatives

- custom-sync
- managed-sync

## Migration and exit

- server-first-to-offline-first

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
