---
id: domain.ai-agent
kind: domain
version: 1.0.0
status: active
domains:
- domain
triggers:
- agent
quality_attributes: []
related: []
legacy_ids:
- domain-guidance:ai-agent
last_reviewed: '2026-07-28'
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
