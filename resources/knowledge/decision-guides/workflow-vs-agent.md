---
id: decision.workflow-vs-agent
kind: decision-guide
version: 2.0.0
status: active
domains:
- ai-agent
triggers:
- workflow
- agent
- deterministic
quality_attributes:
- maintainability
related:
- decision.single-agent-vs-multi-agent
- style.durable-workflow
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: OpenAI practical guide to building agents
  url: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
  authority: official
  supports:
  - AGENT-DEFINITION
  - AGENT-FIT
maturity: golden
curation:
  method: assisted-reviewed
  reviewer: Codex Architecture Governance review
  reviewed_at: '2026-07-28'
---

# Deterministic Workflow vs Agent

## Problem and intent

Decide which steps remain explicit software control flow and where model-directed tool selection is justified by ambiguity.

## Mechanism

A workflow owns a known state machine and may call models inside bounded steps. An agent lets a model choose the next action from tools and instructions until an exit condition, with budgets, guardrails, evidence, and human control around the loop.

## Options

### Deterministic workflow

- Fit: Steps, branching, and acceptance rules can be specified and tested.
- Avoid: Unstructured context makes enumerated rules unmaintainable.
- Cost: Rule and workflow maintenance as cases evolve.
- Failure: A rigid flow accumulates exceptions and manual handoffs.
### Workflow with bounded model steps

- Fit: Interpretation or generation is fuzzy but process authority is known.
- Avoid: The model must discover and execute an open-ended plan.
- Cost: Structured outputs, evaluation data, and fallback handling.
- Failure: Model output silently controls a later high-impact step.
### Tool-using agent

- Fit: The task requires contextual planning across variable tools and can be safely bounded.
- Avoid: A deterministic flow meets the need or mistakes have irreversible impact.
- Cost: Evaluation, tool security, loop limits, recovery, cost, latency, and approval UX.
- Failure: Prompt injection or looping drives unauthorized or untraceable actions.

## Fit when

At least one named option fits a measured quality scenario and the team can own its
required failure and recovery behavior.

## Avoid when

The choice is driven only by a technology name, hypothetical scale, or a problem
already solved by the current design.

## Required capabilities

Task success metric, tool allowlist and least privilege, structured state, step/latency/cost budgets, evidence trail, injection defenses, recovery, evaluation set, and approval for consequential actions.

## Benefits

Uses model autonomy only where ambiguity creates real value while retaining deterministic control elsewhere.

## Costs and liabilities

Agents add nondeterminism, evaluation and security work, latency, cost, and harder incident reconstruction.

## Failure modes

Agent used as a queue or state machine, prompt-injected tool calls, unbounded loops, hidden context loss, fabricated completion, and no human recovery path.

## Alternatives

Compare the current design and the named options—Deterministic workflow, Workflow with bounded model steps, Tool-using agent—against the same
quality scenarios; do not compare feature lists without operating consequences.

## Migration and exit

Implement the deterministic happy path, isolate one ambiguous decision behind structured output, compare it with a labeled evaluation set, and grant tools incrementally with shadow or approval mode.

## Evidence to inspect

Exception rate, rule maintenance burden, unstructured inputs, action reversibility, tool permissions, eval pass rate, trace completeness, loop distribution, latency, and cost.

## Evidence that changes the recommendation

Prefer workflows whenever explicit rules are adequate; introduce an agent only after a bounded model step proves insufficient.

## Quality trade-offs

Adaptability trades against predictability, auditability, security surface, latency, and operating cost.

## Claim map

- AGENT-DEFINITION: An agent uses a model to manage workflow execution and choose tools within guardrails.
- AGENT-FIT: Agents are best suited to complex judgment, difficult rules, or unstructured information.

## Volatile facts

Product versions, protocol/library support, service limits, pricing, licensing, and
security advisories must be rechecked in the cited official sources at decision time.
The mechanisms and decision criteria above are maintained separately from those facts.
