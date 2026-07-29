---
id: decision.state-management
kind: decision-guide
version: 2.0.0
status: active
domains:
- frontend
- mobile
triggers:
- state
- store
- server-state
quality_attributes:
- maintainability
related:
- decision.optimistic-vs-pessimistic-update
- decision.data-loading-and-refresh
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: React preserving and resetting state
  url: https://react.dev/learn/preserving-and-resetting-state
  authority: official
  supports:
  - STATE-IDENTITY
- title: Next.js preserving UI state
  url: https://nextjs.org/docs/app/guides/preserving-ui-state
  authority: official
  supports:
  - STATE-USER-SCOPE
maturity: golden
curation:
  method: assisted-reviewed
  reviewer: Codex Architecture Governance review
  reviewed_at: '2026-07-28'
---

# UI State Management

## Problem and intent

Place state with the narrowest owner that can preserve correctness, rather than copying all remote and local state into one global store.

## Mechanism

Distinguish server authority, URL/navigation state, form drafts, component UI state, and durable local data. Store a value once at its authority and derive or cache downstream representations.

## Options

### Component or feature-local state

- Fit: Only one subtree owns a transient interaction.
- Avoid: Multiple distant features must coordinate the same durable fact.
- Cost: Prop/context wiring at feature boundaries.
- Failure: Lifting everything upward creates incidental coupling.
### Server-state cache

- Fit: Remote resources need deduplication, freshness, retry, and mutation invalidation.
- Avoid: The value is purely local UI or an unsaved draft.
- Cost: Cache keys, stale policy, and mutation reconciliation.
- Failure: Cached copies are mistaken for authority or leak across users.
### Application store or state machine

- Fit: Several features coordinate client-owned state or explicit transitions.
- Avoid: Ordinary remote reads or local toggles are the only need.
- Cost: Actions, lifecycle, persistence, and debugging conventions.
- Failure: A universal store becomes a dependency hub with ambiguous ownership.

## Fit when

At least one named option fits a measured quality scenario and the team can own its
required failure and recovery behavior.

## Avoid when

The choice is driven only by a technology name, hypothetical scale, or a problem
already solved by the current design.

## Required capabilities

State inventory, authoritative owner, lifecycle/reset rules, scope key including user/tenant, serialization policy, transition tests, and devtools/telemetry for complex flows.

## Benefits

Reduces duplicated truth and makes reset, persistence, and synchronization behavior reviewable.

## Costs and liabilities

Several small state mechanisms may coexist; teams must understand the boundary between them.

## Failure modes

Global-store sprawl, copied props drifting, stale server data, persistence across logout, circular derived state, and race-prone effects.

## Alternatives

Compare the current design and the named options—Component or feature-local state, Server-state cache, Application store or state machine—against the same
quality scenarios; do not compare feature lists without operating consequences.

## Migration and exit

Inventory values in the global store, move remote resources to a server-state boundary and leaf interactions local, preserve selectors during transition, then delete duplicated copies after behavior tests pass.

## Evidence to inspect

Read/write ownership graph, reset and login/logout paths, persistence keys, duplicate representations, effect dependencies, render traces, and transition tests.

## Evidence that changes the recommendation

Escalate from local state only when multiple owners or explicit cross-feature transitions are demonstrated.

## Quality trade-offs

Centralization improves discoverability and coordination but increases coupling, lifetime, and accidental persistence.

## Claim map

- STATE-IDENTITY: React state is associated with a component's position and must be reset deliberately.
- STATE-USER-SCOPE: Preserved client state can cross authentication changes unless reset.

## Volatile facts

Product versions, protocol/library support, service limits, pricing, licensing, and
security advisories must be rechecked in the cited official sources at decision time.
The mechanisms and decision criteria above are maintained separately from those facts.
