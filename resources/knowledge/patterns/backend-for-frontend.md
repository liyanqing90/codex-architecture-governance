---
id: pattern.backend-for-frontend
kind: pattern
version: 2.0.0
status: active
domains:
- integration
triggers:
- backend
- for
- frontend
quality_attributes: []
related:
- decision.rest-vs-graphql-vs-grpc
- foundation.system-boundaries
legacy_ids:
- pattern:backend-for-frontend
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Backends for Frontends pattern
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/backends-for-frontends
  authority: official
  supports:
  - BFF-CLIENT
  - BFF-COST
maturity: golden
curation:
  method: assisted-reviewed
  reviewer: Codex Architecture Governance review
  reviewed_at: '2026-07-28'
---

# Backend for Frontend

## Problem and intent

Different web, mobile, or partner clients need materially different aggregation, payload, cadence, or protocol behavior without coupling every backend to presentation details.

## Mechanism

Place a BFF between one client class and backend capabilities. Keep domain commands in owning services, propagate identity and deadlines, bound fan-out, and cache only responses with safe user/tenant keys.

## Operating model

A client-specific edge service authenticates the caller, invokes domain or backend APIs, and shapes a response for one experience. It owns composition and presentation adaptation, not business truth or another copy of domain data.

## Fit when

Client teams have distinct release and aggregation needs and a shared API gateway has accumulated client-specific branching.

## Avoid when

One thin API serves all clients, or the proposed BFF would merely proxy requests without owning composition.

## Required capabilities

Named client owner, upstream contract/version policy, authorization propagation, timeout and partial-failure semantics, fan-out budget, cache isolation, tracing, and no domain-data ownership.

## Benefits

Allows client-oriented APIs and independent experience evolution while protecting domain services from UI-specific churn.

## Costs and liabilities

Adds a deployable hop, duplicated cross-cutting policy risk, more contracts, and possible aggregation latency.

## Failure modes

BFFs become mini-monoliths, duplicate business rules, call many services serially, leak credentials, or multiply one per screen.

## Alternatives

Use a gateway for uniform routing/policy, GraphQL for governed cross-client query composition, or add a single endpoint to the owning backend.

## Migration and exit

Measure client-specific gateway branches, extract one high-value composition behind the existing route, compare latency and authorization behavior, then transfer ownership to the client team without moving domain writes.

## Evidence to inspect

Client release cadence, payload divergence, round trips, gateway conditionals, upstream call graph, authorization mapping, p95 fan-out latency, and team ownership.

## Evidence that changes the recommendation

Prefer a shared API when differences are cosmetic; use a BFF when client-specific composition and ownership are persistent and measurable.

## Quality trade-offs

Client autonomy and fewer round trips trade against service count, duplicated policy, and an extra runtime hop.

## Claim map

- BFF-CLIENT: A BFF separates client-specific backend concerns for different interfaces.
- BFF-COST: Multiple BFF services add operational and duplication overhead.

## Volatile facts

Runtime versions, limits, compatibility, security advisories, pricing, and licensing
must be confirmed from the cited official source at decision time. The stable operating
mechanism remains distinct from those current facts.
