---
id: style.offline-first
kind: architecture-style
version: 1.0.0
status: active
domains:
- application
triggers:
- offline
- first
quality_attributes: []
related: []
legacy_ids:
- architecture-style:offline-first
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Offline-First

## Problem and intent

- Make a local replica usable and writable without connectivity
- then reconcile with remote peers.

## Mechanism

- Make a local replica usable and writable without connectivity

## Fit when

- Offline editing is a core product requirement and prolonged disconnection is expected.

## Avoid when

- Online service authority with a display cache satisfies the product.

## Required capabilities

- local-database
- change-tracking
- outbox
- conflict-policy

## Benefits

- Resilient interaction and user-controlled local continuity.

## Costs and liabilities

- Conflict resolution
- tombstones
- sync cursors
- migration
- and multi-device convergence.

## Failure modes

- last-write-wins-without-policy
- missing-deletion-semantics

## Alternatives

- local-first-sync
- custom-sync

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
