---
id: domain.plugin-platform
kind: domain
version: 1.0.0
status: active
domains:
- domain
triggers:
- plugin
- platform
quality_attributes: []
related: []
legacy_ids:
- domain-guidance:plugin-platform
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: stable-principles-plus-official-docs
sources:
- title: OpenAI Practical Guide to Building Agents
  url: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
  authority: official
---

# Plugin Platforms

## Problem and intent

- Govern extension contracts
- capability authority
- isolation
- compatibility
- lifecycle
- and supply-chain trust.

## Mechanism

- Prefer internal modules until independent extension lifecycle is a product need.

## Fit when

- A host loads independently versioned or third-party extensions.

## Avoid when

- Internal modules within one release satisfy extensibility.

## Required capabilities

- plugin-platform
- manifest-schema
- artifact-provenance

## Benefits

- Makes ecosystem boundaries explicit.

## Costs and liabilities

- Compatibility and trust become long-lived public obligations.

## Failure modes

- plugins-call-host-internals
- unbounded-permissions

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
