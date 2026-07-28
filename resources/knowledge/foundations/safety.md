---
id: foundation.safety
kind: foundation
version: 1.0.0
status: active
domains:
- iso-25010
triggers:
- safety
quality_attributes:
- safety
related: []
legacy_ids:
- quality-model:safety
last_reviewed: '2026-07-28'
review_after_days: 730
source_policy: stable-principles-plus-official-docs
sources:
- title: ISO/IEC 25010:2023
  url: https://www.iso.org/standard/78176.html
  authority: standard
---

# Safety

## Problem and intent

- Prevent unacceptable harm to people
- assets
- finances
- or the environment.

## Mechanism

- Prevent unacceptable harm to people

## Fit when

- Actions can create material or irreversible harm.

## Avoid when

- Do not use generic safety language without a hazard and control path.

## Required capabilities

- An accountable owner, explicit contracts, tests, and operational evidence.

## Benefits

- Places deterministic controls at real harm boundaries.

## Costs and liabilities

- May require reduced autonomy and additional approvals.

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

- safety

## Volatile facts

- Product versions, support status, compatibility, security advisories, licensing, pricing, and service limits are time-sensitive and must be rechecked.
- Stable mechanism guidance remains separate from current vendor or release information.
