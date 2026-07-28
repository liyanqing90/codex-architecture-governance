---
id: style.web-queue-worker
kind: architecture-style
version: 1.0.0
status: active
domains:
- application
triggers:
- web
- queue
- worker
quality_attributes: []
related: []
legacy_ids:
- architecture-style:web-queue-worker
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Web Queue Worker

## Problem and intent

- Move long or bursty work behind a queue while keeping the interactive boundary simple.

## Mechanism

- Move long or bursty work behind a queue while keeping the interactive boundary simple.

## Fit when

- AI inference
- files
- notifications
- reports
- or crawling exceed request lifetimes.

## Avoid when

- All work is short and synchronous or durable multi-step orchestration is required.

## Required capabilities

- queue-observability
- idempotency
- task-state

## Benefits

- Load smoothing and independent worker scaling.

## Costs and liabilities

- Task state
- retries
- deduplication
- cancellation
- and result ownership become explicit responsibilities.

## Failure modes

- invisible-stuck-jobs
- duplicate-side-effects

## Alternatives

- managed-queue
- broker-worker

## Migration and exit

- durable-workflow

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
