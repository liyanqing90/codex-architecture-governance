---
id: migration.server-first-to-offline-first
kind: migration-guide
version: 1.0.0
status: active
domains:
- mobile-data
triggers:
- server
- first
- offline
quality_attributes: []
related: []
legacy_ids:
- migration:server-first-to-offline-first
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Server-First to Offline-First

## Problem and intent

- Introduce a versioned local replica
- durable operation log
- reconciliation protocol
- and conflict policy incrementally.

## Mechanism

- Gate each step with offline
- reconnect
- conflict
- deletion
- and upgrade evidence.

## Fit when

- Offline editing becomes a confirmed core product requirement.

## Avoid when

- Offline display cache meets user needs.

## Required capabilities

- local-schema
- sync-protocol
- conflict-policy
- migration-tests

## Benefits

- Continuous local work and resilient synchronization.

## Costs and liabilities

- Data migration
- conflicts
- tombstones
- battery
- and multi-version servers.

## Failure modes

- implicit-last-write-wins
- no-delete-protocol

## Alternatives

- Keep the current design and apply a smaller local correction.

## Migration and exit

- cache-read
- local-identities
- outbox
- server-idempotency
- conflict-policy
- background-sync

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
