---
id: technology.dapr-workflow
kind: technology-profile
version: 1.0.0
status: active
domains:
- durable-workflow
triggers:
- dapr
- workflow
quality_attributes: []
related: []
legacy_ids:
- technology-profile:dapr-workflow
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: Dapr Workflow Overview
  url: https://docs.dapr.io/developing-applications/building-blocks/workflow/workflow-overview/
  authority: official
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project
  decision.
---

# Dapr Workflow

## Problem and intent

- Run durable workflows and activities alongside Dapr building blocks and sidecars.

## Mechanism

- Run durable workflows and activities alongside Dapr building blocks and sidecars.

## Fit when

- A system already benefits from Dapr and needs durable timers
- retries
- state
- and recovery.

## Avoid when

- A queue or database state machine is sufficient or Dapr adoption has no broader value.

## Required capabilities

- dapr-runtime
- workflow-versioning
- idempotent-activities

## Benefits

- Durable orchestration integrated with Dapr runtime capabilities.

## Costs and liabilities

- Sidecar/runtime operations
- workflow determinism
- versioning
- and ecosystem coupling.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

## Alternatives

- temporal
- aws-step-functions
- azure-durable-functions
- google-workflows

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
