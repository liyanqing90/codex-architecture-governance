---
id: reference.durable-agent-workflow
kind: reference-architecture
version: 1.0.0
status: active
domains:
- ai-agent
triggers:
- durable
- agent
- workflow
quality_attributes: []
related: []
legacy_ids:
- reference-architecture:durable-agent-workflow
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Durable Agent Workflow

## Problem and intent

- Combine deterministic workflow state with bounded model decisions
- authorized tools
- checkpoints
- evaluation
- and human approval.

## Mechanism

- Keep deterministic policy outside model judgment.

## Fit when

- Agent work spans time
- failures
- approvals
- resumptions
- or multiple committed side effects.

## Avoid when

- A fixed short workflow or one agent turn is sufficient.

## Required capabilities

- durable-workflow
- tool-policy
- state-schema
- idempotency
- tracing
- evaluations

## Benefits

- Recoverable execution and explicit authority boundaries.

## Costs and liabilities

- Workflow versioning
- replay safety
- state privacy
- and higher operations cost.

## Failure modes

- model-owned-policy
- side-effects-during-replay

## Alternatives

- temporal
- langgraph
- microsoft-agent-framework

## Migration and exit

- queue-to-durable-workflow

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
