---
id: technology.dapr
kind: technology-profile
version: 1.0.0
status: active
domains:
- distributed-runtime
triggers:
- dapr
quality_attributes: []
related: []
legacy_ids:
- technology-profile:dapr
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: Dapr Building Blocks
  url: https://docs.dapr.io/concepts/building-blocks-concept/
  authority: official
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project
  decision.
---

# Dapr

## Problem and intent

- Expose distributed application building blocks through HTTP or gRPC APIs and pluggable components.

## Mechanism

- Expose distributed application building blocks through HTTP or gRPC APIs and pluggable components.

## Fit when

- Multiple applications benefit from consistent invocation
- pub-sub
- state
- workflow
- actor
- secret
- or configuration APIs.

## Avoid when

- A small system does not justify sidecar and runtime operations.

## Required capabilities

- distributed-operations
- sidecar-observability

## Benefits

- Portable building-block APIs and component abstraction.

## Costs and liabilities

- Sidecar latency
- runtime operations
- component semantics
- and version compatibility.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

## Alternatives

- native-cloud-services
- application-libraries

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
