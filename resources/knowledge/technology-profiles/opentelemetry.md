---
id: technology.opentelemetry
kind: technology-profile
version: 1.0.0
status: active
domains:
- observability
triggers:
- opentelemetry
quality_attributes: []
related: []
legacy_ids:
- technology-profile:opentelemetry
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: OpenTelemetry Documentation
  url: https://opentelemetry.io/docs/
  authority: official
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project
  decision.
---

# OpenTelemetry

## Problem and intent

- Instrument
- generate
- collect
- and export vendor-neutral traces
- metrics
- and logs.

## Mechanism

- Instrument

## Fit when

- Critical flows cross components or telemetry portability and correlation matter.

## Avoid when

- Instrumentation has no owner
- privacy policy
- or operational backend.

## Required capabilities

- telemetry-owner
- collector-or-backend
- data-governance

## Benefits

- Standard context propagation and portable telemetry.

## Costs and liabilities

- Sampling
- cardinality
- privacy
- collector
- and backend operations.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

## Alternatives

- vendor-native-instrumentation

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
