---
id: domain.search-recommendation
kind: domain
version: 1.0.0
status: active
domains:
- domain
triggers:
- search
- recommendation
quality_attributes: []
related: []
legacy_ids:
- domain-guidance:search-recommendation
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: stable-principles-plus-official-docs
sources:
- title: OpenAI Practical Guide to Building Agents
  url: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
  authority: official
---

# Search and Recommendation

## Problem and intent

- Govern source/index consistency
- ranking quality
- freshness
- authorization
- experimentation
- and rollback.

## Mechanism

- Choose search or vector infrastructure from retrieval semantics and scale
- not popularity.

## Fit when

- Users retrieve or rank content through indexes
- embeddings
- or learned models.

## Avoid when

- Direct authoritative queries meet the requirement.

## Required capabilities

- search-recommendation
- evaluation-datasets
- index-reconciliation

## Benefits

- Makes relevance
- freshness
- and access control testable.

## Costs and liabilities

- Offline metrics can diverge from user outcomes.

## Failure modes

- authorization-after-ranking
- no-index-rebuild

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
