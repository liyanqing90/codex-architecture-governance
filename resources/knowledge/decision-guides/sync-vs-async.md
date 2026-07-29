---
id: decision.sync-vs-async
kind: decision-guide
version: 2.0.0
status: active
domains:
- backend-api
- distributed-systems
triggers:
- sync
- async
- queue
quality_attributes:
- maintainability
related:
- decision.request-vs-background-job
- style.durable-workflow
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Asynchronous Request-Reply pattern
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/asynchronous-request-reply
  authority: official
  supports:
  - ASYNC-ACCEPT
  - ASYNC-COMPLEXITY
maturity: golden
curation:
  method: assisted-reviewed
  reviewer: Codex Architecture Governance review
  reviewed_at: '2026-07-28'
---

# Synchronous vs Asynchronous Interaction

## Problem and intent

Choose whether the caller waits for completion or hands work to a durable boundary with later status.

## Mechanism

Synchronous calls bind caller latency and availability to the callee. Asynchronous calls acknowledge durable acceptance, carry an idempotency key and correlation ID, and expose completion or failure independently.

## Options

### Synchronous request-reply

- Fit: Fast bounded work where the caller needs the result to continue.
- Avoid: Latency is long or the dependency frequently fails independently.
- Cost: Tight latency and availability coupling.
- Failure: Timeouts trigger duplicate work or cascading resource exhaustion.
### Asynchronous command with status

- Fit: Work is long-running, bursty, retryable, or independently scalable.
- Avoid: The caller requires immediate atomic completion.
- Cost: Queue, status model, idempotency, retries, and operator tooling.
- Failure: Accepted work is lost, stuck, duplicated, or never reaches a terminal state.

## Fit when

At least one named option fits a measured quality scenario and the team can own its
required failure and recovery behavior.

## Avoid when

The choice is driven only by a technology name, hypothetical scale, or a problem
already solved by the current design.

## Required capabilities

Latency budget, timeout and cancellation semantics, durable acceptance for async work, idempotency, bounded retries, dead-letter handling, correlation, and terminal status.

## Benefits

Makes coupling and overload behavior deliberate and lets long-running work scale independently.

## Costs and liabilities

Async interaction adds state machines and eventual outcomes; sync interaction consumes caller capacity during waits.

## Failure modes

Retry amplification, orphan jobs, poison messages, invisible partial completion, and using language-level async while retaining distributed synchronous coupling.

## Alternatives

Compare the current design and the named options—Synchronous request-reply, Asynchronous command with status—against the same
quality scenarios; do not compare feature lists without operating consequences.

## Migration and exit

Measure tail latency and timeout retries, introduce an operation resource returning HTTP 202 for one long path, dual-observe results, then retire the synchronous completion contract after consumers migrate.

## Evidence to inspect

p95/p99 duration, timeout rate, retry behavior, job durability, queue age, idempotency store, cancellation needs, and consumer expectations.

## Evidence that changes the recommendation

Keep synchronous behavior when completion is reliably within budget and required by the next step; choose async when durability and load leveling matter more than immediate completion.

## Quality trade-offs

Synchronous flows are simpler to reason about but couple failures; asynchronous flows isolate and buffer at the cost of state and delayed feedback.

## Claim map

- ASYNC-ACCEPT: Long-running HTTP work can acknowledge acceptance and expose a status resource.
- ASYNC-COMPLEXITY: Decoupling request and response adds completion and failure coordination.

## Volatile facts

Product versions, protocol/library support, service limits, pricing, licensing, and
security advisories must be rechecked in the cited official sources at decision time.
The mechanisms and decision criteria above are maintained separately from those facts.
