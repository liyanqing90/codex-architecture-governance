---
id: decision.relational-vs-document-vs-graph
kind: decision-guide
version: 2.0.0
status: active
domains:
- data
triggers:
- relational
- document
- graph
quality_attributes:
- maintainability
related:
- decision.database-selection
- pattern.materialized-view
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: PostgreSQL transaction isolation
  url: https://www.postgresql.org/docs/current/transaction-iso.html
  authority: official
  supports:
  - RELATIONAL-ISO
- title: Neo4j database internals and transactions
  url: https://neo4j.com/docs/operations-manual/current/database-internals/
  authority: official
  supports:
  - GRAPH-TX
maturity: golden
curation:
  method: assisted-reviewed
  reviewer: Codex Architecture Governance review
  reviewed_at: '2026-07-28'
---

# Relational vs Document vs Graph Data Model

## Problem and intent

Choose a primary data model from invariants and access paths while avoiding a different authority for every query shape.

## Mechanism

Relational models normalize facts and enforce constraints across rows; document models persist aggregates together; graph models make nodes and relationships the traversal surface. Any secondary model should remain a rebuildable projection unless ownership moves deliberately.

## Options

### Relational

- Fit: Cross-entity constraints, transactions, reporting, and evolving queries matter.
- Avoid: The workload is almost entirely aggregate-local and schema joins dominate cost.
- Cost: Schema migrations and joins require discipline.
- Failure: Missing constraints or unindexed joins erode integrity and latency.
### Document

- Fit: Aggregates are read and written together with bounded document size.
- Avoid: Many-to-many relations and cross-aggregate invariants dominate.
- Cost: Duplication, update fan-out, and application-enforced consistency.
- Failure: Unbounded documents or duplicated facts drift.
### Graph

- Fit: Variable-depth relationship traversal is a core measured operation.
- Avoid: Simple key, aggregate, or set queries cover the product.
- Cost: New query language, operations, projection synchronization, and access control.
- Failure: A graph is introduced for conceptual elegance but ordinary lookups remain primary.

## Fit when

At least one named option fits a measured quality scenario and the team can own its
required failure and recovery behavior.

## Avoid when

The choice is driven only by a technology name, hypothetical scale, or a problem
already solved by the current design.

## Required capabilities

Named aggregates and invariants, representative query corpus, cardinality and growth, transaction scope, index plan, migration/rebuild path, authorization traversal, and operator capability.

## Benefits

Connects model shape to actual correctness and query behavior and permits derived models without confused ownership.

## Costs and liabilities

Specialized models simplify selected paths while making other constraints, joins, or operations harder.

## Failure modes

Choosing from entity diagrams alone, unbounded documents, graph supernodes, duplicated authorities, and application-only constraints without tests.

## Alternatives

Compare the current design and the named options—Relational, Document, Graph—against the same
quality scenarios; do not compare feature lists without operating consequences.

## Migration and exit

Keep one authority, project a bounded read model into the candidate, compare query and recovery behavior, and move authority only after constraints and rollback are proven.

## Evidence to inspect

Invariant map, aggregate size, relationship depth/fan-out, query plans, transaction conflicts, schema-change frequency, restore tests, and authorization rules.

## Evidence that changes the recommendation

Use relational by default for broad transactional needs; document or graph should be justified by dominant aggregate-local or traversal workloads.

## Quality trade-offs

Each model moves complexity among storage shape, query expressiveness, integrity enforcement, duplication, and operations.

## Claim map

- RELATIONAL-ISO: Relational transaction isolation protects concurrent database behavior.
- GRAPH-TX: Graph database operations execute within transactional boundaries.

## Volatile facts

Product versions, protocol/library support, service limits, pricing, licensing, and
security advisories must be rechecked in the cited official sources at decision time.
The mechanisms and decision criteria above are maintained separately from those facts.
