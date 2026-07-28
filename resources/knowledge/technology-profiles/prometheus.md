---
id: technology.prometheus
kind: technology-profile
version: 1.0.0
status: active
domains:
- metrics-monitoring
triggers:
- prometheus
quality_attributes: []
related: []
legacy_ids:
- technology-profile:prometheus
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: Prometheus Documentation
  url: https://prometheus.io/docs/introduction/overview/
  authority: official
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project
  decision.
---

# Prometheus

## Problem and intent

- Collect and query labeled time-series metrics for operational monitoring and alerting.

## Mechanism

- Collect and query labeled time-series metrics for operational monitoring and alerting.

## Fit when

- Pull-based service metrics and PromQL-based alerting match the observability platform.

## Avoid when

- It would be used as an authoritative business database or labels cannot be bounded.

## Required capabilities

- metric-governance
- cardinality-budgets
- alert-ownership

## Benefits

- Open ecosystem
- expressive queries
- service discovery
- and alerting integration.

## Costs and liabilities

- Cardinality
- retention
- federation
- long-term storage
- and pull-model constraints.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

## Alternatives

- managed-metrics
- timescaledb

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
