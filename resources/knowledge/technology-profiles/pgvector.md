---
id: technology.pgvector
kind: technology-profile
version: 1.0.0
status: active
domains:
- vector-retrieval
triggers:
- pgvector
quality_attributes: []
related: []
legacy_ids:
- technology-profile:pgvector
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: pgvector
  url: https://github.com/pgvector/pgvector
  authority: maintainer
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project
  decision.
---

# pgvector

## Problem and intent

- Add vector similarity search and indexes to PostgreSQL alongside relational filtering and transactions.

## Mechanism

- Add vector similarity search and indexes to PostgreSQL alongside relational filtering and transactions.

## Fit when

- Vector scale and latency fit PostgreSQL and combining metadata
- transactions
- and retrieval reduces complexity.

## Avoid when

- Vector scale
- indexing
- isolation
- or serving needs exceed the operational database boundary.

## Required capabilities

- postgresql-operations
- retrieval-evaluation
- index-capacity

## Benefits

- One governed store for metadata and vectors with SQL filtering.

## Costs and liabilities

- Index build
- memory
- recall
- query planning
- write load
- and database contention.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

## Alternatives

- milvus
- managed-vector-service

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
