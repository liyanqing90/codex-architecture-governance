---
id: foundation.google-cloud-well-architected
kind: foundation
version: 1.0.0
status: active
domains:
- cloud-quality-model
triggers:
- google
- cloud
- well
- architected
quality_attributes:
- reliability
- security
- performance-efficiency
- maintainability
- cost
related: []
legacy_ids:
- quality-model:google-cloud-well-architected
last_reviewed: '2026-07-28'
review_after_days: 180
source_policy: stable-principles-plus-official-docs
sources:
- title: Google Cloud Well-Architected Framework
  url: https://cloud.google.com/architecture/framework
  authority: official
---

# Google Cloud Well-Architected Framework

## Problem and intent

- Review cloud systems across operational excellence
- security
- reliability
- cost optimization
- performance
- and sustainability.

## Mechanism

- Review cloud systems across operational excellence

## Fit when

- Google Cloud workloads or broadly applicable cloud design tradeoffs are in scope.

## Avoid when

- Do not treat a framework checklist as evidence that product scenarios are satisfied.

## Required capabilities

- An accountable owner, explicit contracts, tests, and operational evidence.

## Benefits

- Cross-cutting cloud design principles and operational recommendations.

## Costs and liabilities

- Google Cloud context can bias implementation selection.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

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

- reliability
- security
- performance-efficiency
- maintainability
- cost

## Volatile facts

- Product versions, support status, compatibility, security advisories, licensing, pricing, and service limits are time-sensitive and must be rechecked.
- Stable mechanism guidance remains separate from current vendor or release information.
