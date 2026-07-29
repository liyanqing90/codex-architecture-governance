---
id: decision.database-selection
kind: decision-guide
version: 2.0.0
status: active
domains:
- data
triggers:
- database
- sql
- storage
quality_attributes:
- maintainability
related:
- decision.relational-vs-document-vs-graph
- pattern.materialized-view
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: PostgreSQL transaction isolation
  url: https://www.postgresql.org/docs/current/transaction-iso.html
  authority: official
  supports:
  - DB-TRANSACTIONS
- title: PostgreSQL backup and restore
  url: https://www.postgresql.org/docs/current/backup.html
  authority: official
  supports:
  - DB-RECOVERY
maturity: golden
curation:
  method: assisted-reviewed
  reviewer: Codex Architecture Governance review
  reviewed_at: '2026-07-28'
---

# Database Selection

## Problem and intent

Select a persistence engine from owned data invariants, access paths, consistency, recovery, scale, and operational capability.

## Mechanism

Start with the aggregate and invariant boundary, enumerate critical reads and writes, then verify transaction, index, partition, backup, restore, migration, and failure behavior against representative data.

## Options

### Existing general-purpose database

- Fit: It satisfies invariants and access paths with known operations.
- Avoid: A measured workload cannot meet a critical scenario.
- Cost: May require careful indexing or a bounded extension.
- Failure: Convenience schemas hide contention or unbounded queries.
### Purpose-specific database

- Fit: A distinct model or workload has proven requirements the current engine cannot meet.
- Avoid: The choice is based only on data shape or projected scale.
- Cost: New expertise, backup, security, monitoring, and integration.
- Failure: A second authority creates dual writes and recovery ambiguity.
### Polyglot persistence with derived store

- Fit: One authority feeds a rebuildable search, graph, cache, or analytic projection.
- Avoid: The derived store is treated as the only copy without recovery design.
- Cost: Replication lag, reconciliation, lineage, and additional operations.
- Failure: Projection drift serves incomplete or unauthorized data.

## Fit when

At least one named option fits a measured quality scenario and the team can own its
required failure and recovery behavior.

## Avoid when

The choice is driven only by a technology name, hypothetical scale, or a problem
already solved by the current design.

## Required capabilities

Authority and ownership, consistency/invariant scenarios, access-path benchmarks, schema evolution, backup/restore proof, security, data lifecycle, capacity model, and operator skill.

## Benefits

Keeps database choice tied to durable correctness and operations rather than feature checklists.

## Costs and liabilities

Every engine adds a lifecycle, failure model, and staffing obligation; migrations have dual-run and rollback costs.

## Failure modes

Benchmarking toy data, using one database per feature, missing restore tests, cross-store transactions, and selecting for hypothetical scale.

## Alternatives

Compare the current design and the named options—Existing general-purpose database, Purpose-specific database, Polyglot persistence with derived store—against the same
quality scenarios; do not compare feature lists without operating consequences.

## Migration and exit

Build a representative benchmark and restore drill, place the candidate behind a repository interface, backfill with checksums, dual-read for evidence, then cut authority only with rollback and reconciliation.

## Evidence to inspect

Data invariants, query/write distribution, cardinality and growth, contention, retention, residency, backup RPO/RTO, migration history, cost, and operational ownership.

## Evidence that changes the recommendation

Retain the current engine unless a critical measured scenario fails and the candidate demonstrates both workload fit and sustainable operations.

## Quality trade-offs

Model fit and performance trade against transactional scope, portability, operational simplicity, and recovery confidence.

## Claim map

- DB-TRANSACTIONS: Transaction isolation and failure behavior are first-class persistence capabilities.
- DB-RECOVERY: Backup and restore procedures are part of a database's production suitability.

## Volatile facts

Product versions, protocol/library support, service limits, pricing, licensing, and
security advisories must be rechecked in the cited official sources at decision time.
The mechanisms and decision criteria above are maintained separately from those facts.
