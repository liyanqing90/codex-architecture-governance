---
id: decision.system-style-selection
kind: decision-guide
version: 1.0.0
status: active
domains:
- decision-process
triggers:
- system
- style
- selection
quality_attributes: []
related: []
legacy_ids:
- decision-guide:system-style-selection
last_reviewed: '2026-07-28'
review_after_days: 180
source_policy: stable-principles-plus-official-docs
sources:
- title: AWS Well-Architected Framework
  url: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
  authority: official
- title: Google Cloud Well-Architected Framework
  url: https://cloud.google.com/architecture/framework
  authority: official
- title: Azure Architecture Center
  url: https://learn.microsoft.com/en-us/azure/architecture/
  authority: official
---

# System Architecture Style Selection

## Problem and intent

- Select the least complex architecture that satisfies business scenarios
- quality attributes
- team capability
- cost
- and migration constraints.

## Mechanism

- Always include keep-current with local repair.
- Reject microservices when independent deployment and team autonomy are unproven.
- Reject durable workflow when short idempotent queue work is sufficient.
- Reject event sourcing for ordinary CRUD without temporal or audit value.
- Reject offline-first when server authority plus cache meets the offline requirement.
- Reject multi-agent when a fixed workflow or single agent meets the capability.
- Compare business fit, quality effects, team capability, implementation and operations complexity, migration risk, reversibility, cost, maturity, and lock-in.
- Record why each non-selected option was rejected and what evidence would trigger reconsideration.

## Fit when

- A verified problem requires an architecture or platform decision.

## Avoid when

- No confirmed problem or decision authority exists.

## Required capabilities

- quality-scenarios
- current-architecture-map
- verified-findings
- decision-authority

## Benefits

- Makes alternatives
- tradeoffs
- assumptions
- and revisit triggers explicit.

## Costs and liabilities

- Scores can create false precision if evidence is weak.

## Failure modes

- single-option-recommendation
- technology-first-design
- missing-do-nothing

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
