---
id: reference.retrieval-augmented-agent
kind: reference-architecture
version: 1.0.0
status: active
domains:
- ai-agent
triggers:
- retrieval
- augmented
- agent
quality_attributes: []
related: []
legacy_ids:
- reference-architecture:retrieval-augmented-agent
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Retrieval-Augmented Agent

## Problem and intent

- Combine governed source ingestion and retrieval with bounded agent reasoning
- citations
- tool authorization
- and evaluation.

## Mechanism

- Retrieval improves access to evidence but does not make generated claims true.

## Fit when

- Agent decisions require changing private knowledge with provenance.

## Avoid when

- Static prompt context or deterministic search and presentation meets the need.

## Required capabilities

- source-governance
- chunk-lineage
- retrieval-evaluation
- authorization-filtering
- tool-policy

## Benefits

- Fresh grounded context and inspectable source attribution.

## Costs and liabilities

- Ingestion trust
- authorization filtering
- staleness
- retrieval quality
- prompt injection
- and cost.

## Failure modes

- retrieval-bypasses-acl
- citation-not-bound-to-claim

## Alternatives

- postgresql
- pgvector
- elasticsearch-opensearch
- milvus

## Migration and exit

- search-to-governed-retrieval

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
