---
id: pattern.feature-flag
kind: pattern
version: 1.0.0
status: active
domains:
- delivery
triggers:
- feature
- flag
quality_attributes: []
related: []
legacy_ids:
- pattern:feature-flag
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Feature Flag

## Problem and intent

- Separate deployment from exposure and provide bounded rollback or cohort control.

## Mechanism

- Separate deployment from exposure and provide bounded rollback or cohort control.

## Fit when

- Incremental rollout or rapid containment materially reduces risk.

## Avoid when

- The flag cannot isolate the change or will become permanent configuration.

## Required capabilities

- flag-owner
- expiry
- telemetry

## Benefits

- Controlled exposure and fast behavioral rollback.

## Costs and liabilities

- State combinations
- cleanup
- and inconsistent user experience.

## Failure modes

- permanent-flag
- untested-combinations

## Alternatives

- canary-deployment

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
