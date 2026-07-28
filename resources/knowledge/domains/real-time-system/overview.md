---
id: domain.real-time-system
kind: domain
version: 1.0.0
status: active
domains:
- domain
triggers:
- real
- time
- system
quality_attributes: []
related: []
legacy_ids:
- domain-guidance:real-time-system
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: stable-principles-plus-official-docs
sources:
- title: OpenAI Practical Guide to Building Agents
  url: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
  authority: official
---

# Real-Time Systems

## Problem and intent

- Govern deadlines
- time semantics
- ordering
- backpressure
- partitioning
- state recovery
- and overload.

## Mechanism

- Use the simplest processing model that meets measured latency and ordering needs.

## Fit when

- Correctness depends on bounded latency or continuous event processing.

## Avoid when

- Batch or request-response processing meets product targets.

## Required capabilities

- real-time-system
- load-tests
- state-recovery

## Benefits

- Makes timing and overload part of correctness.

## Costs and liabilities

- Representative load
- clocks
- and recovery evidence are difficult.

## Failure modes

- average-latency-only
- unbounded-buffer

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
