---
id: technology.redis-valkey
kind: technology-profile
version: 1.0.0
status: active
domains:
- key-value-cache
triggers:
- redis
- valkey
quality_attributes: []
related: []
legacy_ids:
- technology-profile:redis-valkey
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: Redis Documentation
  url: https://redis.io/docs/latest/
  authority: official
- title: Valkey Documentation
  url: https://valkey.io/topics/
  authority: official
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project
  decision.
---

# Redis or Valkey

## Problem and intent

- Provide low-latency key-value and data-structure operations for caches
- ephemeral coordination
- streams
- or selected durable state.

## Mechanism

- Provide low-latency key-value and data-structure operations for caches

## Fit when

- Access is key-oriented and latency or data-structure semantics justify an in-memory service.

## Avoid when

- It would become an ungoverned authoritative database or correctness depends on cache availability.

## Required capabilities

- memory-capacity
- eviction-policy
- failure-semantics

## Benefits

- Low latency and useful atomic data structures.

## Costs and liabilities

- Memory cost
- eviction
- persistence semantics
- hot keys
- failover
- and misuse as a queue or lock.

## Failure modes

- The mechanism is adopted by convention without a traced failure path.

## Alternatives

- application-cache
- relational-database
- managed-queue

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
