---
id: domain.cloud-native-platform
kind: domain
version: 1.0.0
status: active
domains:
- domain
triggers:
- cloud
- native
- platform
quality_attributes: []
related: []
legacy_ids:
- domain-guidance:cloud-native-platform
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: stable-principles-plus-official-docs
sources:
- title: OpenAI Practical Guide to Building Agents
  url: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
  authority: official
---

# Cloud-Native Platforms

## Problem and intent

- Govern workload ownership
- identity
- failure domains
- progressive delivery
- drift
- capacity
- cost
- and platform contracts.

## Mechanism

- Build a platform only around repeated
- owned consumer needs.

## Fit when

- Many cloud workloads share deployment and operational capabilities.

## Avoid when

- Managed application hosting meets needs without a platform layer.

## Required capabilities

- cloud-native-platform
- workload-catalog
- platform-slo

## Benefits

- Consistent operational control and self-service delivery.

## Costs and liabilities

- Platform ownership and abstraction can exceed product value.

## Failure modes

- platform-without-consumers
- kubernetes-as-architecture

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
