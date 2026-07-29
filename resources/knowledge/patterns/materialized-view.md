---
id: pattern.materialized-view
kind: pattern
version: 2.0.0
status: active
domains:
- data
triggers:
- materialized
- view
quality_attributes: []
related:
- decision.cache-strategy
- decision.database-selection
legacy_ids:
- pattern:materialized-view
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Materialized View pattern
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/materialized-view
  authority: official
  supports:
  - MV-PRECOMPUTE
  - MV-CONSISTENCY
maturity: golden
curation:
  method: assisted-reviewed
  reviewer: Codex Architecture Governance review
  reviewed_at: '2026-07-28'
---

# Materialized View

## Problem and intent

Serve expensive joins, aggregates, search, graph traversal, or dashboard reads without moving write authority into a query-specific structure.

## Mechanism

Define the projection schema and source checkpoint, build snapshots or consume changes idempotently, publish a completed generation atomically, and expose lag and reconciliation results.

## Operating model

A projector derives a query-optimized representation from authoritative records or events. The view stores its source position or generation, can be rebuilt, and is served only within an explicit freshness and completeness contract.

## Fit when

A stable high-value query cannot meet latency/load targets directly and bounded projection lag is acceptable.

## Avoid when

The authoritative query already meets its scenario, strong read-after-write is mandatory, or no owner can rebuild and reconcile the view.

## Required capabilities

Source authority, deterministic transform, idempotent update, checkpoint, backfill/rebuild, atomic generation switch, deletion handling, freshness SLO, reconciliation, and authorization-safe fields.

## Benefits

Improves read latency and isolates read load while allowing data shape to match the consuming query.

## Costs and liabilities

Duplicates data, introduces lag, consumes storage/compute, and requires schema coordination and rebuild operations.

## Failure modes

Projector skips or reorders changes, rebuild mixes generations, deleted or permission-revoked data remains visible, and clients treat stale data as authoritative.

## Alternatives

Add or change an index, optimize the authoritative query, cache the final response, or use an on-demand aggregate for low-frequency reads.

## Migration and exit

Capture baseline query cost, backfill a versioned projection with counts/checksums, shadow-read and compare, switch a bounded cohort, then retain rebuild and fallback procedures.

## Evidence to inspect

Query plan and latency, source change volume, acceptable staleness, projection lag, checkpoint durability, reconciliation mismatches, rebuild time, access-control changes, and storage cost.

## Evidence that changes the recommendation

Prefer indexing or cache-aside for simpler repeated reads; choose a materialized view when a distinct query model and rebuildable lag are justified.

## Quality trade-offs

Read speed and workload isolation trade against consistency lag, duplicated storage, rebuild complexity, and another observable pipeline.

## Claim map

- MV-PRECOMPUTE: A materialized view precomputes data suited to query needs.
- MV-CONSISTENCY: The view requires a refresh/update strategy and can lag its sources.

## Volatile facts

Runtime versions, limits, compatibility, security advisories, pricing, and licensing
must be confirmed from the cited official source at decision time. The stable operating
mechanism remains distinct from those current facts.
