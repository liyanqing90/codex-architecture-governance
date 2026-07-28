---
id: style.serverless
kind: architecture-style
version: 1.0.0
status: active
domains:
- application
triggers:
- serverless
quality_attributes: []
related: []
legacy_ids:
- architecture-style:serverless
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Serverless

## Problem and intent

- Run event-driven
- short-lived workloads with managed scaling and reduced infrastructure operations.

## Mechanism

- Run event-driven

## Fit when

- Traffic is bursty
- tasks are bounded
- and platform constraints are acceptable.

## Avoid when

- Work is continuously high-load
- long-running
- stateful in-process
- or portability is critical.

## Required capabilities

- external-state
- idempotency
- platform-observability

## Benefits

- Managed scaling and low idle operations.

## Costs and liabilities

- Cold starts
- execution limits
- debugging
- cost curves
- and platform lock-in.

## Failure modes

- long-functions
- hidden-retries
- connection-exhaustion

## Alternatives

- cloud-functions
- managed-containers

## Migration and exit

- web-queue-worker

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
