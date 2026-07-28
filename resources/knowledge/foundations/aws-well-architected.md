---
id: foundation.aws-well-architected
kind: foundation
version: 1.0.0
status: active
domains:
- cloud-quality-model
triggers:
- aws
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
- quality-model:aws-well-architected
last_reviewed: '2026-07-28'
review_after_days: 180
source_policy: stable-principles-plus-official-docs
sources:
- title: AWS Well-Architected Framework
  url: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
  authority: official
---

# AWS Well-Architected Framework

## Problem and intent

- Review cloud workloads across operational excellence
- security
- reliability
- performance efficiency
- cost optimization
- and sustainability.

## Mechanism

- Review cloud workloads across operational excellence

## Fit when

- AWS workloads or cloud-operating tradeoffs are in scope.

## Avoid when

- Do not substitute cloud guidance for product
- domain
- or team-specific scenarios.

## Required capabilities

- An accountable owner, explicit contracts, tests, and operational evidence.

## Benefits

- Operational questions
- risks
- and improvement guidance grounded in AWS services.

## Costs and liabilities

- AWS context and service assumptions can bias otherwise portable decisions.

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
