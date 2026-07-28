---
id: technology.elasticsearch-opensearch
kind: technology-profile
version: 1.0.0
status: active
domains:
- search-engine
triggers:
- elasticsearch
- opensearch
quality_attributes: []
related: []
legacy_ids:
- technology-profile:elasticsearch-opensearch
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: Elasticsearch Reference
  url: https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html
  authority: official
- title: OpenSearch Documentation
  url: https://docs.opensearch.org/latest/
  authority: official
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project
  decision.
---

# Elasticsearch or OpenSearch

## Problem and intent

- Index and query text
- structured fields
- aggregations
- and relevance-oriented read models.

## Mechanism

- Index and query text

## Fit when

- Search
- filtering
- aggregation
- or ranking needs exceed authoritative database query capabilities.

## Avoid when

- It would become the sole uncontrolled source of truth or direct indexed SQL meets targets.

## Required capabilities

- index-pipeline
- rebuild
- authorization-filtering
- cluster-operations

## Benefits

- Full-text search
- flexible retrieval
- aggregations
- and horizontal read scaling.

## Costs and liabilities

- Index consistency
- mappings
- cluster operations
- memory
- rebuild
- security
- and product divergence.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

## Alternatives

- postgresql
- managed-search

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
