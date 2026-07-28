---
id: technology.microsoft-agent-framework
kind: technology-profile
version: 1.0.0
status: active
domains:
- agent-orchestration
triggers:
- microsoft
- agent
- framework
quality_attributes: []
related: []
legacy_ids:
- technology-profile:microsoft-agent-framework
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: Agent Framework Orchestrations
  url: https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/
  authority: official
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project
  decision.
---

# Microsoft Agent Framework

## Problem and intent

- Build and orchestrate agents and explicit workflows with typed messages
- checkpoints
- approvals
- and multiple orchestration patterns.

## Mechanism

- Build and orchestrate agents and explicit workflows with typed messages

## Fit when

- Python or .NET applications need explicit agent workflow patterns and Microsoft ecosystem integration.

## Avoid when

- One model call
- one agent
- or a simple deterministic workflow is sufficient.

## Required capabilities

- workflow-ownership
- evaluation
- authorization

## Benefits

- Agent and workflow separation with built-in orchestration patterns.

## Costs and liabilities

- Framework evolution
- runtime semantics
- and orchestration complexity.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

## Alternatives

- openai-agents-sdk
- langgraph
- temporal

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
