---
id: technology.service-mesh
kind: technology-profile
version: 1.0.0
status: active
domains:
- service-networking
triggers:
- service
- mesh
quality_attributes: []
related: []
legacy_ids:
- technology-profile:service-mesh
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: Istio Documentation
  url: https://istio.io/latest/docs/
  authority: official
- title: Linkerd Documentation
  url: https://linkerd.io/2/overview/
  authority: official
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project
  decision.
---

# Service Mesh

## Problem and intent

- Provide workload identity
- mTLS
- traffic policy
- and telemetry through a managed service communication layer.

## Mechanism

- Provide workload identity

## Fit when

- Many independently operated services need consistent east-west security or traffic controls.

## Avoid when

- A small service estate can enforce the same controls through platform-native networking and libraries.

## Required capabilities

- platform-ownership
- workload-identity
- network-observability

## Benefits

- Consistent workload communication policy and telemetry.

## Costs and liabilities

- Data-plane overhead
- control-plane operations
- debugging complexity
- and policy sprawl.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

## Alternatives

- platform-native-service-networking

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
