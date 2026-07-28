---
id: technology.azure-durable-functions
kind: technology-profile
version: 1.0.0
status: active
domains:
- managed-workflow
triggers:
- azure
- durable
- functions
quality_attributes: []
related: []
legacy_ids:
- technology-profile:azure-durable-functions
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: Durable Functions Overview
  url: https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview
  authority: official
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project
  decision.
---

# Azure Durable Functions

## Problem and intent

- Build stateful serverless orchestrations
- entities
- and activity workflows on Azure Functions.

## Mechanism

- Build stateful serverless orchestrations

## Fit when

- Azure Functions is already appropriate and code-first durable orchestration is required.

## Avoid when

- Work is short and stateless or portability beyond Azure is required.

## Required capabilities

- azure-functions
- deterministic-orchestrators
- idempotent-activities

## Benefits

- Managed checkpoints
- retries
- timers
- fan-out
- and external events.

## Costs and liabilities

- Deterministic orchestrator constraints
- storage/runtime coupling
- versioning
- and Azure lock-in.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

## Alternatives

- temporal
- aws-step-functions
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
