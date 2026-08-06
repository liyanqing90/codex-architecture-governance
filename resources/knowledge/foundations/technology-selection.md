---
id: foundation.technology-selection
kind: foundation
version: 1.0.0
status: active
domains:
- cross-cutting
triggers:
- framework
- platform
- adopt
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

# Technology Selection

## Problem and intent

Select technology from required capabilities, operational ownership, compatibility, exit cost, and current official evidence.

When the candidate is emerging or proposed as an upgrade/replacement, assess
replacement value against a measured current baseline. Novelty, market
attention, a vendor roadmap, or a capability list is not a reason to change.

## Mechanism

Apply the mechanism at its owning boundary, keep authority and contracts explicit, and bind the choice to measurable scenarios rather than technology presence.

## Fit when

A project is considering adding, replacing, or standardizing a framework, store, runtime, or managed service.

## Avoid when

The technology is already an immutable constraint and only compliant use is under review.

## Required capabilities

An accountable owner, a measurable capability or quality gap, explicit
compatibility and failure semantics, migration and exit cost, rollback, current
official evidence for volatile claims, proportional tests, observable shadow
or pilot outcomes, explicit revisit triggers, and an affordable operating
model are required.

## Benefits

The choice addresses the stated problem while keeping the reason, protected qualities, and governing evidence reviewable.

## Costs and liabilities

It adds implementation, migration, cognitive, and operational costs that must be compared with keeping the current design.

## Failure modes

It fails when adopted from naming, popularity, hypothetical scale, stale
volatile claims, or an official capability statement without project-fit
evidence, ownership, negative-path behavior, migration/rollback evidence, or a
bounded shadow/pilot.

## Alternatives

Keep the current architecture with a local correction, or select the next simpler mechanism that satisfies the same quality scenario.

## Migration and exit

Keep the current path as the baseline. If a measured gap survives comparison,
introduce the new behavior behind a compatible boundary, observe a bounded
shadow or pilot cohort, preserve rollback, and remove the old path only after
consumers, data, operating fit, and exit evidence are verified.

## Evidence to inspect

Inspect the product scenario, owning code and configuration, consumers,
persisted contracts, tests, current official sources for volatile claims,
runtime shadow/pilot evidence, team capability, migration/rollback path, lock-in
and exit cost boundary.

## Evidence that changes the recommendation

A simpler keep-current or local option meeting the same measurable outcome,
missing operational ownership, incompatible consumers, unaffordable migration
or exit, stale official evidence, an unsuccessful pilot, or contrary runtime
evidence changes the recommendation. A valid conclusion is to keep current and
revisit on a named trigger.

## Quality trade-offs

Prioritize maintainability while explicitly recording effects on reliability, security, performance, maintainability, delivery speed, cost, and cognitive load.

## Volatile facts

Versions, support status, compatibility, security advisories, licensing,
pricing, service limits, roadmaps, and benchmarks require current official
confirmation recorded with publisher, URL, scope, and review date; they are not
timeless architecture facts or proof of project fit.
