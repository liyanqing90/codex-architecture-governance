---
id: decision.request-vs-background-job
kind: decision-guide
version: 2.0.0
status: active
domains:
- backend-api
- reliability
triggers:
- request
- background
- job
quality_attributes:
- maintainability
related:
- decision.sync-vs-async
- style.durable-workflow
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure background job guidance
  url: https://learn.microsoft.com/en-us/azure/architecture/best-practices/background-jobs
  authority: official
  supports:
  - JOB-SEPARATION
  - JOB-RELIABILITY
maturity: golden
curation:
  method: assisted-reviewed
  reviewer: Codex Architecture Governance review
  reviewed_at: '2026-07-28'
---

# Request Handler vs Background Job

## Problem and intent

Place work in the interactive request path or in a separately owned worker without creating hidden fire-and-forget behavior.

## Mechanism

A request handler validates and performs only bounded work needed for the response. A background job begins after a durable handoff, has a lease or message, records attempts, and reaches a visible terminal state.

## Options

### Inline request work

- Fit: Short, bounded operations whose result defines the response.
- Avoid: CPU, I/O, or external dependencies exceed the request budget.
- Cost: Consumes request concurrency and couples failures.
- Failure: Timeouts leave unknown completion and retries duplicate effects.
### Durable background job

- Fit: Long, bursty, scheduled, or independently retryable work.
- Avoid: No durable queue/status owner exists or immediate completion is required.
- Cost: Worker fleet, queue, idempotency, retries, status, and support runbooks.
- Failure: Jobs disappear, poison messages loop, or leases cause concurrent execution.

## Fit when

At least one named option fits a measured quality scenario and the team can own its
required failure and recovery behavior.

## Avoid when

The choice is driven only by a technology name, hypothetical scale, or a problem
already solved by the current design.

## Required capabilities

Explicit acceptance boundary, idempotency key, durable payload or reference, attempt limits, lease/visibility timeout, dead-letter path, progress/status, and cancellation policy.

## Benefits

Protects interactive latency and permits job-specific scaling and recovery.

## Costs and liabilities

Introduces operational state, delayed outcomes, and coordination between API and worker.

## Failure modes

In-process background threads die on deploy, job payloads become incompatible, retry repeats non-idempotent effects, or queue age grows unnoticed.

## Alternatives

Compare the current design and the named options—Inline request work, Durable background job—against the same
quality scenarios; do not compare feature lists without operating consequences.

## Migration and exit

Extract the slowest self-contained step, persist a job before returning, run a worker with idempotent completion, expose status, and remove the old inline branch after result parity and restart tests pass.

## Evidence to inspect

Request latency and timeout traces, task duration distribution, deployment interruption behavior, queue depth/age, job retry history, and terminal-state coverage.

## Evidence that changes the recommendation

Inline is preferable for consistently short atomic work; a durable job is required when completion must survive process or deployment failure.

## Quality trade-offs

Background execution protects responsiveness and scalability but adds eventual completion and operational ownership.

## Claim map

- JOB-SEPARATION: Background jobs run independently from the initiating UI or request process.
- JOB-RELIABILITY: Reliable background work needs restart, conflict, result, and poison-message handling.

## Volatile facts

Product versions, protocol/library support, service limits, pricing, licensing, and
security advisories must be rechecked in the cited official sources at decision time.
The mechanisms and decision criteria above are maintained separately from those facts.
