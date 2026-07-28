---
id: foundation.compatibility
kind: foundation
version: 1.0.0
status: active
domains:
- iso-25010
triggers:
- compatibility
quality_attributes:
- compatibility
related: []
legacy_ids:
- quality-model:compatibility
last_reviewed: '2026-07-28'
review_after_days: 730
source_policy: stable-principles-plus-official-docs
sources:
- title: ISO/IEC 25010:2023
  url: https://www.iso.org/standard/78176.html
  authority: standard
---

# Compatibility

## Problem and intent

- Protect coexistence and interoperability across components and versions.

## Mechanism

- Protect coexistence and interoperability across components and versions.

## Fit when

- Public APIs
- events
- schemas
- platforms
- or mixed versions interact.

## Avoid when

- Do not preserve unused contracts without identified consumers.

## Required capabilities

- An accountable owner, explicit contracts, tests, and operational evidence.

## Benefits

- Reduces silent consumer breakage.

## Costs and liabilities

- Compatibility windows create migration and test cost.

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

- compatibility

## Volatile facts

- Product versions, support status, compatibility, security advisories, licensing, pricing, and service limits are time-sensitive and must be rechecked.
- Stable mechanism guidance remains separate from current vendor or release information.
