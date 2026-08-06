---
id: domain.ai-agent
kind: domain
version: 1.1.0
status: active
domains:
- domain
triggers:
- agent
quality_attributes: []
related: []
legacy_ids:
- domain-guidance:ai-agent
last_reviewed: '2026-08-06'
review_after_days: 90
source_policy: stable-principles-plus-official-docs
sources:
- title: OpenAI Practical Guide to Building Agents
  url: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
  authority: official
---

# AI Agent Systems

## Problem and intent

- Govern probabilistic boundaries
- context
- memory
- tools
- recovery
- evaluation
- cost
- and human authority.

## Mechanism

- Prefer deterministic code
- then model call
- fixed workflow
- single agent
- and only then multi-agent.

## Context and data discipline

- Inventory every context source, its necessity, authority, scope, freshness,
  sensitivity, transformation, retention, and disposal before treating it as
  eligible for assembly.
- Separate stable policy, contracts, and instructions from volatile user,
  retrieval, task-state, and provider context. Keep ordering deterministic and
  scope cache keys and invalidation to the same authorization and provenance
  boundary.
- Bound context budgets and compression so authority, provenance, and required
  recency survive; otherwise fail closed and record what was lost.
- Minimize sensitive and personal data independently at prompt, retrieval,
  memory, and trace boundaries. Prefer scoped references or redacted fields to
  copying raw content, and define retention and deletion for each surface.

## Evidence and change decisions

- Bind behavioral evidence to exact model/runtime, prompt, tool policy and
  schema, retriever/index/ranking configuration, context treatment, evaluation
  data, environment, timestamp, and hashes where available.
- Compare adopt, retain, and reject decisions for upgrades against the current
  baseline using concrete critical-flow scenarios and evidence for quality,
  compatibility, security, operations, cost, ownership, rollout, and rollback.
- Treat technology names as evidence labels, not architecture findings. State
  the invariant, capability, critical flow, and failure or control path.
- Keep candidate evidence separate from verification; do not turn a technology
  comparison or an unbound benchmark into a verified conclusion.

## Fit when

- Models select actions
- use tools
- maintain memory
- or participate in workflows.

## Avoid when

- The system only performs deterministic processing.

## Required capabilities

- ai-agent-core
- evaluations
- traceability

## Benefits

- Makes AI-specific authority and reliability risks explicit.

## Costs and liabilities

- Requires model-versioned and time-bound behavioral evidence.

## Failure modes

- model-owned-policy
- unaudited-tools

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
