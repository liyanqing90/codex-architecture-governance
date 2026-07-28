---
id: decision.data-store-selection
kind: decision-guide
version: 1.0.0
status: active
domains:
- decision-process
triggers:
- data
- store
- selection
quality_attributes: []
related: []
legacy_ids:
- decision-guide:data-store-selection
last_reviewed: '2026-07-28'
review_after_days: 180
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Data Store Models
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/data-store-overview
  authority: official
---

# Data Store Selection

## Problem and intent

- Choose the least complex store that satisfies ownership
- integrity
- access
- consistency
- scale
- lifecycle
- recovery
- and operations.

## Mechanism

- Start with the existing relational store when it meets integrity and access needs.
- Add search, vector, graph, stream, cache, or time-series systems only for a measured specialized capability.
- Define authoritative source, replication lag, rebuild, deletion, backup, restore, and exit path for every derived store.
- Compare operational maturity, unit cost, portability, and migration before peak benchmark claims.

## Fit when

- A verified access or quality need may justify a new or changed data store.

## Avoid when

- Technology preference is the only reason to add a store.

## Required capabilities

- data-model
- query-inventory
- consistency-scenarios
- scale-evidence
- operations-owner

## Benefits

- Separates data semantics from brand selection and limits polyglot persistence.

## Costs and liabilities

- Future workload estimates can create false precision.

## Failure modes

- database-per-feature
- no-authoritative-owner
- migration-omitted

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
