---
id: decision.single-agent-vs-multi-agent
kind: decision-guide
version: 2.0.0
status: active
domains:
- ai-agent
triggers:
- single-agent
- multi-agent
- handoff
quality_attributes:
- maintainability
related:
- decision.workflow-vs-agent
- foundation.proportional-design
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: OpenAI practical guide to building agents
  url: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
  authority: official
  supports:
  - SINGLE-FIRST
  - MULTI-PATTERNS
maturity: golden
curation:
  method: assisted-reviewed
  reviewer: Codex Architecture Governance review
  reviewed_at: '2026-07-28'
---

# Single-Agent vs Multi-Agent Orchestration

## Problem and intent

Choose one agent loop or multiple specialized agents from evaluation evidence, context/tool boundaries, ownership, and failure isolation.

## Mechanism

A single agent owns the user context and chooses among tools. Multi-agent orchestration introduces typed delegation: a manager invokes specialists or a handoff transfers control, and every boundary constrains context, authority, result schema, and termination.

## Options

### Single agent with tools

- Fit: One instruction hierarchy and context can handle the task reliably.
- Avoid: Tool overlap or instruction complexity causes measured failures.
- Cost: Prompt/tool growth and context management.
- Failure: The agent selects the wrong similar tool or loses critical instructions.
### Manager with specialist tools

- Fit: Specialized tasks need separate context but one controller should retain authority.
- Avoid: Delegation overhead exceeds the task or the manager cannot verify results.
- Cost: Routing, schemas, nested latency/cost, and trace composition.
- Failure: The manager trusts an unsupported specialist answer.
### Peer handoffs

- Fit: Different agents genuinely own separate conversational domains and control may transfer.
- Avoid: A single user-facing authority or strong transaction boundary is required.
- Cost: Handoff state, permission change, return path, and user clarity.
- Failure: Context or authority disappears between peers and no agent owns completion.

## Fit when

At least one named option fits a measured quality scenario and the team can own its
required failure and recovery behavior.

## Avoid when

The choice is driven only by a technology name, hypothetical scale, or a problem
already solved by the current design.

## Required capabilities

Single-agent baseline, labeled routing and task evals, typed delegation, context minimization, tool/permission scopes, hop and budget limits, trace correlation, failure return, and accountable final owner.

## Benefits

Preserves simple orchestration until specialization measurably improves quality or isolation.

## Costs and liabilities

Every agent boundary adds model calls, context transformation, evaluation combinations, and unclear accountability risk.

## Failure modes

Role-play agents without isolation value, delegation loops, contradictory instructions, authority escalation, context leakage, and final answers with no evidence owner.

## Alternatives

Compare the current design and the named options—Single agent with tools, Manager with specialist tools, Peer handoffs—against the same
quality scenarios; do not compare feature lists without operating consequences.

## Migration and exit

Benchmark the single agent first, extract the highest-confusion capability as one typed specialist, shadow its routing, compare quality/cost/latency, and stop if the gain is not material.

## Evidence to inspect

Tool confusion matrix, instruction length, task clusters, context sensitivity, single-agent baseline, routing accuracy, hop count, cost, latency, and failure traces.

## Evidence that changes the recommendation

Keep one agent until evaluation shows a specific specialization or permission boundary that outweighs orchestration cost.

## Quality trade-offs

Specialization and isolation trade against latency, cost, context loss, routing errors, and accountability.

## Claim map

- SINGLE-FIRST: A single agent can gain capability incrementally by adding tools.
- MULTI-PATTERNS: Multi-agent orchestration commonly uses manager or decentralized handoff patterns.

## Volatile facts

Product versions, protocol/library support, service limits, pricing, licensing, and
security advisories must be rechecked in the cited official sources at decision time.
The mechanisms and decision criteria above are maintained separately from those facts.
