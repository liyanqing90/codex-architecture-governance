---
id: pattern.change-data-capture
kind: pattern
version: 1.0.0
status: active
domains:
- data-integration
triggers:
- change
- data
- capture
quality_attributes: []
related: []
legacy_ids:
- pattern:change-data-capture
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Change Data Capture

## Problem and intent

- Publish committed database changes from a log or change stream.

## Mechanism

- Publish committed database changes from a log or change stream.

## Fit when

- Existing committed changes must feed independent downstream consumers.

## Avoid when

- Business event semantics cannot be derived safely from storage changes.

## Required capabilities

- schema-governance
- checkpoint
- replay

## Benefits

- Avoids application dual writes and supports replay.

## Costs and liabilities

- Schema coupling
- ordering
- backfill
- and operational lag.

## Failure modes

- raw-row-as-domain-event
- no-backfill-plan

## Alternatives

- outbox

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
