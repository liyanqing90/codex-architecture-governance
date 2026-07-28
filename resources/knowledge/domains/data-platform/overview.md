---
id: domain.data-platform
kind: domain
version: 1.0.0
status: active
domains:
- domain
triggers:
- data
- platform
quality_attributes: []
related: []
legacy_ids:
- domain-guidance:data-platform
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: stable-principles-plus-official-docs
sources:
- title: OpenAI Practical Guide to Building Agents
  url: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
  authority: official
---

# Data Platform

## Problem and intent

- Govern ownership
- schemas
- lineage
- freshness
- quality
- replay
- retention
- and analytical versus operational boundaries.

## Mechanism

- Select stores from access
- consistency
- volume
- retention
- and operations evidence.

## Fit when

- Pipelines
- warehouses
- lakes
- streams
- indexes
- or derived datasets support decisions.

## Avoid when

- A single operational database has no analytical consumers.

## Required capabilities

- catalog
- lineage
- quality-checks
- retention

## Benefits

- Makes data products and lineage accountable.

## Costs and liabilities

- Backfills
- schema evolution
- privacy
- and cost governance.

## Failure modes

- unknown-owner
- silent-schema-drift

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
