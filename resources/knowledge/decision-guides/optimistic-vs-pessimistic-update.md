---
id: decision.optimistic-vs-pessimistic-update
kind: decision-guide
version: 1.0.0
status: active
domains:
- frontend
- mobile
- data
triggers:
- optimistic
- conflict
- rollback
quality_attributes:
- maintainability
related: []
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Center
  url: https://learn.microsoft.com/en-us/azure/architecture/
  authority: official
---

# Optimistic vs Pessimistic Update

## Problem and intent

Choose feedback timing from conflict probability, effect reversibility, authority, error impact, and compensation UX.

## Mechanism

Apply the mechanism at its owning boundary, keep authority and contracts explicit, and bind the choice to measurable scenarios rather than technology presence.

## Fit when

User-perceived latency matters and writes may be presented before authority confirms them.

## Avoid when

The action is high-impact, irreversible, or conflicts are common.

## Required capabilities

An accountable owner, explicit compatibility and failure semantics, proportional tests, observable outcomes, and an affordable operating model are required.

## Benefits

The choice addresses the stated problem while keeping the reason, protected qualities, and governing evidence reviewable.

## Costs and liabilities

It adds implementation, migration, cognitive, and operational costs that must be compared with keeping the current design.

## Failure modes

It fails when adopted from naming, popularity, or hypothetical scale without ownership, negative-path behavior, and acceptance evidence.

## Alternatives

Keep the current architecture with a local correction, or select the next simpler mechanism that satisfies the same quality scenario.

## Migration and exit

Introduce the new behavior behind a compatible boundary, observe a bounded cohort, preserve rollback, and remove the old path only after consumers and data are verified.

## Evidence to inspect

Inspect the product scenario, owning code and configuration, consumers, persisted contracts, tests, runtime evidence when applicable, team capability, and cost boundary.

## Evidence that changes the recommendation

A simpler option meeting the same measurable outcome, missing operational ownership, incompatible consumers, or contrary runtime evidence changes the recommendation.

## Quality trade-offs

Prioritize maintainability while explicitly recording effects on reliability, security, performance, maintainability, delivery speed, cost, and cognitive load.

## Volatile facts

Versions, support status, compatibility, security advisories, licensing, pricing, and service limits require current official confirmation; they are not timeless architecture facts.
