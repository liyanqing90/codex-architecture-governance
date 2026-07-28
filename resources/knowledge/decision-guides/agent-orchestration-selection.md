---
id: decision.agent-orchestration-selection
kind: decision-guide
version: 1.0.0
status: active
domains:
- decision-process
triggers:
- agent
- orchestration
- selection
quality_attributes: []
related: []
legacy_ids:
- decision-guide:agent-orchestration-selection
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: stable-principles-plus-official-docs
sources:
- title: OpenAI Practical Guide to Building Agents
  url: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
  authority: official
---

# Agent Orchestration Selection

## Problem and intent

- Choose deterministic code
- model call
- fixed workflow
- single agent
- manager
- handoff
- graph
- or durable agent from actual uncertainty and authority needs.

## Mechanism

- Evaluate deterministic code before any model.
- Evaluate a single call before a workflow and a fixed workflow before an agent.
- Require a distinct ownership or context benefit before adding another agent.
- Use durable orchestration only for state that must survive process or human time.
- Keep authorization and irreversible policy deterministic.

## Fit when

- Models may plan
- use tools
- preserve state
- or coordinate specialists.

## Avoid when

- A deterministic implementation already satisfies the task.

## Required capabilities

- task-analysis
- tool-policy
- evaluation
- state-lifecycle
- cost-budget

## Benefits

- Limits autonomy and multi-agent complexity to demonstrated value.

## Costs and liabilities

- Behavioral evidence is model-versioned and time-bound.

## Failure modes

- multi-agent-by-default
- model-owned-policy
- side-effects-without-approval

## Alternatives

- Keep the current design and apply a smaller local correction.

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
