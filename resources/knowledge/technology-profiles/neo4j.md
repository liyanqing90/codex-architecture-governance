---
id: technology.neo4j
kind: technology-profile
version: 1.0.0
status: active
domains:
- graph-database
triggers:
- neo4j
quality_attributes: []
related: []
legacy_ids:
- technology-profile:neo4j
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: Neo4j Documentation
  url: https://neo4j.com/docs/
  authority: official
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project
  decision.
---

# Neo4j

## Problem and intent

- Persist and query connected data through graph traversal and declarative graph queries.

## Mechanism

- Persist and query connected data through graph traversal and declarative graph queries.

## Fit when

- Relationship traversal is central and cannot be served acceptably by relational or index projections.

## Avoid when

- The graph is merely a visualization or ordinary joins satisfy measured queries.

## Required capabilities

- graph-modeling
- query-governance
- backup-restore

## Benefits

- Expressive graph traversal and relationship-centric modeling.

## Costs and liabilities

- Specialized model
- query language
- clustering
- migration
- and ecosystem lock-in.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

## Alternatives

- postgresql
- materialized-view

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
