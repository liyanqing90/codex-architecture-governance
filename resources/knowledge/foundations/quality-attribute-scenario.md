---
id: foundation.quality-attribute-scenario
kind: foundation
version: 1.0.0
status: active
domains:
- evaluation-method
triggers:
- quality
- attribute
- scenario
quality_attributes:
- all
related: []
legacy_ids:
- quality-model:quality-attribute-scenario
last_reviewed: '2026-07-28'
review_after_days: 730
source_policy: stable-principles-plus-official-docs
sources:
- title: SEI Quality Attribute Workshop
  url: https://www.sei.cmu.edu/our-work/software-architecture/quality-attribute-workshop/
  authority: research
---

# Quality Attribute Scenario

## Problem and intent

- Turn a quality concern into a source
- stimulus
- environment
- target
- response
- and measurable response measure.

## Mechanism

- Turn a quality concern into a source

## Fit when

- An architecture quality must be compared
- verified
- or gated.

## Avoid when

- A vague adjective has no operational consequence or decision owner.

## Required capabilities

- An accountable owner, explicit contracts, tests, and operational evidence.

## Benefits

- Creates testable decision criteria and exposes conflicting assumptions.

## Costs and liabilities

- Poorly chosen stimuli or measures create false confidence.

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

- all

## Volatile facts

- Product versions, support status, compatibility, security advisories, licensing, pricing, and service limits are time-sensitive and must be rechecked.
- Stable mechanism guidance remains separate from current vendor or release information.
