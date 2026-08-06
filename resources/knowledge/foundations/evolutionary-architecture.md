---
id: foundation.evolutionary-architecture
kind: foundation
version: 1.0.0
status: active
domains:
- delivery
- cross-cutting
triggers:
- migration
- reversible
- fitness
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

# Evolutionary Architecture

## Problem and intent

Evolve through compatible slices, executable fitness functions, observable checkpoints, and explicit contraction gates.

Use evolution to test a measured capability or quality gap against the
keep-current baseline. Do not treat an emerging technology, upgrade, or
replacement as an architectural destination merely because it is new.

## Mechanism

Apply the mechanism at its owning boundary, keep authority and contracts explicit, and bind the choice to measurable scenarios rather than technology presence.

## Fit when

The target cannot be introduced safely in one atomic deployment.

## Avoid when

A disposable prototype has no persisted or public contract and replacement is cheaper than migration.

## Required capabilities

An accountable owner, a measurable gap and fitness function, explicit
compatibility and failure semantics, migration cost, current official evidence
for volatile claims, a bounded shadow or pilot, rollback and exit evidence,
explicit revisit triggers, proportional tests, observable outcomes, and an
affordable operating model are required.

## Benefits

The choice addresses the stated problem while keeping the reason, protected qualities, and governing evidence reviewable.

## Costs and liabilities

It adds implementation, migration, cognitive, and operational costs that must be compared with keeping the current design.

## Failure modes

It fails when adopted from naming, popularity, hypothetical scale, stale
volatile claims, or an unmeasured promise without ownership, compatible
coexistence, negative-path behavior, shadow/pilot evidence, rollback, and a
contraction gate.

## Alternatives

Keep the current architecture with a local correction, or select the next simpler mechanism that satisfies the same quality scenario.

## Migration and exit

Keep the current implementation available while introducing a compatible
boundary. Observe a bounded shadow or pilot cohort against explicit fitness
functions, preserve rollback and data recovery, and remove the old path only
after consumers, data, operating fit, and exit cost are verified.

## Evidence to inspect

Inspect the product scenario, owning code and configuration, consumers,
persisted contracts, tests, current official sources for volatile claims,
runtime shadow/pilot evidence, team capability, migration/rollback path, and
lock-in/exit cost boundary.

## Evidence that changes the recommendation

A simpler keep-current option meeting the same measurable outcome, missing
operational ownership, incompatible consumers, unaffordable migration or exit,
stale official evidence, an unsuccessful pilot, or contrary runtime evidence
changes the recommendation. A valid evolution outcome is keep-current with a
measurable revisit trigger.

## Quality trade-offs

Prioritize maintainability while explicitly recording effects on reliability, security, performance, maintainability, delivery speed, cost, and cognitive load.

## Volatile facts

Versions, support status, compatibility, security advisories, licensing,
pricing, service limits, roadmaps, and benchmarks require current official
confirmation recorded with publisher, URL, scope, and review date; they are not
timeless architecture facts or proof of project fit.
