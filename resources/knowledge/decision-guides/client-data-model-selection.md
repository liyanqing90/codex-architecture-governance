---
id: decision.client-data-model-selection
kind: decision-guide
version: 1.0.0
status: active
domains:
- decision-process
triggers:
- client
- data
- model
- selection
quality_attributes: []
related: []
legacy_ids:
- decision-guide:client-data-model-selection
last_reviewed: '2026-07-28'
review_after_days: 180
source_policy: stable-principles-plus-official-docs
sources:
- title: Android Offline-first Guidance
  url: https://developer.android.com/topic/architecture/data-layer/offline-first
  authority: official
---

# Client Data Model Selection

## Problem and intent

- Choose server-first
- thin-client cache
- or local-first replicas from offline
- authority
- conflict
- migration
- privacy
- and energy requirements.

## Mechanism

- Prefer server-first when connectivity is required and the server is authoritative.
- Add a cache for bounded stale reads and optimistic presentation without offline ownership.
- Choose local-first only when prolonged offline creation or editing is a core capability.
- Require conflict, tombstone, migration, storage, and recovery semantics before local-first adoption.

## Fit when

- A mobile or desktop client needs durable data or weak-network behavior.

## Avoid when

- The client is a stateless presentation.

## Required capabilities

- offline-scenarios
- authority-map
- version-matrix
- privacy-classification

## Benefits

- Prevents accidental distributed data systems in clients.

## Costs and liabilities

- Product assumptions about offline use require field evidence.

## Failure modes

- local-database-means-offline-first
- cache-used-as-authority

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
