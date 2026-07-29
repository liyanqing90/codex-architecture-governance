---
id: decision.local-first-vs-server-first
kind: decision-guide
version: 2.0.0
status: active
domains:
- mobile
- data
triggers:
- offline
- local-first
- server-first
quality_attributes:
- maintainability
related:
- decision.optimistic-vs-pessimistic-update
- decision.state-management
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Local-first software
  url: https://www.inkandswitch.com/essay/local-first/
  authority: research
  supports:
  - LOCAL-FIRST
  - SYNC-CONFLICT
maturity: golden
curation:
  method: assisted-reviewed
  reviewer: Codex Architecture Governance review
  reviewed_at: '2026-07-28'
---

# Local-First vs Server-First

## Problem and intent

Choose the authoritative and interaction path for data when devices may be offline, concurrent, constrained, or shared.

## Mechanism

Server-first commits against a central authority and may cache locally. Local-first commits to a device replica and synchronizes operations or versions later, so conflicts and convergence are product semantics rather than transport details.

## Options

### Server-first with local cache

- Fit: Connectivity is expected and shared authority must arbitrate changes.
- Avoid: Core work must remain writable for long offline periods.
- Cost: Offline behavior is limited and latency depends on network.
- Failure: A cache is mistaken for a writable replica and loses edits.
### Offline queue over server authority

- Fit: Users need bounded offline commands that can replay later.
- Avoid: Concurrent offline edits require rich merging.
- Cost: Command durability, ordering, idempotency, expiry, and rejection UI.
- Failure: Replayed commands are no longer valid or execute twice.
### Local-first replicated data

- Fit: Instant offline-capable collaboration is a defining product requirement.
- Avoid: The team cannot define conflict and convergence semantics.
- Cost: Replica identity, sync protocol, merge model, tombstones, migration, and support.
- Failure: Silent conflict resolution loses intent or replicas never converge.

## Fit when

At least one named option fits a measured quality scenario and the team can own its
required failure and recovery behavior.

## Avoid when

The choice is driven only by a technology name, hypothetical scale, or a problem
already solved by the current design.

## Required capabilities

Authority declaration, offline duration, replica/device identity, version or operation model, conflict UX, encryption, deletion/tombstone rules, schema migration, and sync observability.

## Benefits

Makes offline reliability and user-perceived responsiveness an explicit architecture property.

## Costs and liabilities

Local-first moves distributed-systems complexity onto every device; server-first depends on connectivity.

## Failure modes

Last-write-wins data loss, duplicate offline commands, clock assumptions, unbounded tombstones, account crossover, and incompatible local schema upgrades.

## Alternatives

Compare the current design and the named options—Server-first with local cache, Offline queue over server authority, Local-first replicated data—against the same
quality scenarios; do not compare feature lists without operating consequences.

## Migration and exit

Begin with read caching and a single idempotent offline command, simulate long disconnect and concurrent edits, introduce versioned conflict handling, and expand only after convergence and recovery tests pass.

## Evidence to inspect

Offline product scenarios, concurrent editor count, data sensitivity, conflict examples, device storage limits, sync traces, deletion behavior, and migration tests across skipped versions.

## Evidence that changes the recommendation

Server-first remains simpler unless offline writes and instant local interaction are critical product capabilities, not convenience features.

## Quality trade-offs

Availability and local latency trade against centralized consistency, simpler authorization, and lower client complexity.

## Claim map

- LOCAL-FIRST: Local-first software treats the local copy as primary for interaction and synchronizes in the background.
- SYNC-CONFLICT: Replicated writes require explicit conflict or convergence behavior.

## Volatile facts

Product versions, protocol/library support, service limits, pricing, licensing, and
security advisories must be rechecked in the cited official sources at decision time.
The mechanisms and decision criteria above are maintained separately from those facts.
