---
id: technology.google-workflows
kind: technology-profile
version: 1.0.0
status: active
domains:
- managed-workflow
triggers:
- google
- workflows
quality_attributes: []
related: []
legacy_ids:
- technology-profile:google-workflows
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: Google Cloud Workflows Overview
  url: https://cloud.google.com/workflows/docs/overview
  authority: official
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project
  decision.
---

# Google Cloud Workflows

## Problem and intent

- Orchestrate Google Cloud services and HTTP APIs with managed workflow executions.

## Mechanism

- Orchestrate Google Cloud services and HTTP APIs with managed workflow executions.

## Fit when

- Google Cloud integrations and low-operations orchestration match the workflow.

## Avoid when

- Long-lived code-centric workers or cloud portability are primary needs.

## Required capabilities

- gcp-operations
- idempotent-services
- workflow-versioning

## Benefits

- Managed execution
- connectors
- retries
- callbacks
- and observability.

## Costs and liabilities

- Workflow language
- quotas
- local experience
- and Google Cloud lock-in.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

## Alternatives

- temporal
- aws-step-functions
- azure-durable-functions

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
