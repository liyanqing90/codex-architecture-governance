---
id: technology.temporal
kind: technology-profile
version: 1.0.0
status: active
domains:
- durable-workflow
triggers:
- temporal
quality_attributes: []
related: []
legacy_ids:
- technology-profile:temporal
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: Temporal Documentation
  url: https://docs.temporal.io/
  authority: official
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project
  decision.
---

# Temporal

## Problem and intent

- Provide durable execution for long-running workflows
- activities
- timers
- retries
- signals
- and recovery.

## Mechanism

- Provide durable execution for long-running workflows

## Fit when

- Multi-step work must resume reliably across crashes and long waits.

## Avoid when

- A queue plus database status machine is sufficient.

## Required capabilities

- workflow-versioning
- idempotent-activities

## Benefits

- Durable orchestration and failure recovery.

## Costs and liabilities

- Workflow determinism
- versioning
- event history
- worker
- and service operations.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

## Alternatives

- dapr-workflow
- cloud-workflows

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
