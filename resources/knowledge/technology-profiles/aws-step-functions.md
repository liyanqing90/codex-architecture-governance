---
id: technology.aws-step-functions
kind: technology-profile
version: 1.0.0
status: active
domains:
- managed-workflow
triggers:
- aws
- step
- functions
quality_attributes: []
related: []
legacy_ids:
- technology-profile:aws-step-functions
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: AWS Step Functions Developer Guide
  url: https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html
  authority: official
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project
  decision.
---

# AWS Step Functions

## Problem and intent

- Orchestrate AWS services and application tasks through managed state machines.

## Mechanism

- Orchestrate AWS services and application tasks through managed state machines.

## Fit when

- AWS-native integrations and managed orchestration outweigh portability and local-runtime needs.

## Avoid when

- Workflow portability
- in-process coding models
- or non-AWS operation is a primary constraint.

## Required capabilities

- aws-operations
- state-machine-versioning
- idempotent-tasks

## Benefits

- Managed availability
- visual state
- service integrations
- retries
- and execution history.

## Costs and liabilities

- State-language constraints
- service quotas
- pricing
- local parity
- and AWS lock-in.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

## Alternatives

- temporal
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
