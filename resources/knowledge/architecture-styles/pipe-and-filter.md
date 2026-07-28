---
id: style.pipe-and-filter
kind: architecture-style
version: 1.0.0
status: active
domains:
- processing
triggers:
- pipe
- and
- filter
quality_attributes: []
related: []
legacy_ids:
- architecture-style:pipe-and-filter
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Pipe and Filter

## Problem and intent

- Compose independently testable transformation stages through explicit typed inputs
- outputs
- ordering
- and failure semantics.

## Mechanism

- Compose independently testable transformation stages through explicit typed inputs

## Fit when

- Data or media passes through repeatable transformations that can be isolated
- parallelized
- retried
- or replaced.

## Avoid when

- The workflow is stateful business orchestration with cross-step authority and compensation.

## Required capabilities

- stage-contracts
- correlation
- backpressure
- replay

## Benefits

- Composable stages
- incremental scaling
- and localized reasoning.

## Costs and liabilities

- Serialization
- intermediate storage
- ordering
- backpressure
- and end-to-end observability.

## Failure modes

- shared-hidden-state
- unbounded-intermediate-data

## Alternatives

- in-process-pipeline
- queued-pipeline
- stream-processing

## Migration and exit

- extract-transform-stages

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
