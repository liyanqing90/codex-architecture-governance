---
id: style.durable-workflow
kind: architecture-style
version: 2.0.0
status: active
domains:
- application
triggers:
- durable
- workflow
quality_attributes: []
related:
- decision.sync-vs-async
- decision.request-vs-background-job
- decision.workflow-vs-agent
legacy_ids:
- architecture-style:durable-workflow
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Temporal durable execution
  url: https://docs.temporal.io/encyclopedia/durable-execution
  authority: official
  supports:
  - DURABLE-EXEC
  - DURABLE-REPLAY
maturity: golden
curation:
  method: assisted-reviewed
  reviewer: Codex Architecture Governance review
  reviewed_at: '2026-07-28'
---

# Durable Workflow

## Problem and intent

Coordinate long-running, multi-step work that must survive process failure, wait for external events, and expose a trustworthy lifecycle.

## Mechanism

Persist workflow identity, input, current state, timers, event correlation, and terminal result. Keep orchestration deterministic under replay and isolate nondeterministic I/O in retryable activities.

## Operating model

A workflow definition advances persisted execution state through named, idempotent activities. The runtime records enough history to replay or resume after worker, process, or deployment failure; external effects occur only through activities with explicit retry and compensation semantics.

## Fit when

Business processes last beyond one request, cross deploys or outages, wait on humans/external systems, and need visible recovery.

## Avoid when

A short database transaction, simple queue consumer, or stateless request already provides adequate durability.

## Required capabilities

Stable workflow/activity IDs, idempotency, replay-safe orchestration, bounded retry and timeout policy, cancellation, compensation, versioning, history retention, and operator search/recovery.

## Benefits

Makes long-running state and recovery explicit and removes ad hoc cron, status-table, and retry glue.

## Costs and liabilities

Adds a workflow runtime, deterministic coding constraints, history lifecycle, new deployment/versioning rules, and specialist operations.

## Failure modes

Nondeterministic replay, duplicated external effects, unbounded histories, incompatible workflow code upgrades, stuck waits, and compensation that is assumed to be rollback.

## Alternatives

Use a database-backed job for one durable step, a broker consumer for independent events, or an application state machine when an additional runtime is not justified.

## Migration and exit

Model the existing state machine and failure states, move one restart-sensitive process behind stable workflow/activity contracts, replay production-like histories through upgrades, and retain an operator fallback until recovery drills pass.

## Evidence to inspect

Process duration, wait states, restart/deploy failures, current retry tables and cron jobs, side effects, recovery time, state-machine transitions, and workflow-history growth.

## Evidence that changes the recommendation

A queue plus idempotent worker is simpler when work has one step; adopt durable workflow only when persisted orchestration and timers remove demonstrated failure or maintenance cost.

## Quality trade-offs

Recovery and visibility improve at the cost of runtime dependence, replay constraints, history storage, and migration discipline.

## Claim map

- DURABLE-EXEC: Durable execution preserves workflow progress through infrastructure failure.
- DURABLE-REPLAY: Workflow code and activities require replay- and retry-aware design.

## Volatile facts

Runtime versions, limits, compatibility, security advisories, pricing, and licensing
must be confirmed from the cited official source at decision time. The stable operating
mechanism remains distinct from those current facts.
