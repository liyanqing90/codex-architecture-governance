---
id: decision.rest-vs-graphql-vs-grpc
kind: decision-guide
version: 2.0.0
status: active
domains:
- backend-api
triggers:
- rest
- graphql
- grpc
quality_attributes:
- maintainability
related:
- pattern.backend-for-frontend
- decision.sync-vs-async
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: GraphQL Learn
  url: https://graphql.org/learn/
  authority: official
  supports:
  - GRAPHQL-SCHEMA
- title: gRPC introduction
  url: https://grpc.io/docs/what-is-grpc/introduction/
  authority: official
  supports:
  - GRPC-CONTRACT
- title: RFC 9110 HTTP Semantics
  url: https://www.rfc-editor.org/rfc/rfc9110
  authority: standard
  supports:
  - HTTP-SEMANTICS
maturity: golden
curation:
  method: assisted-reviewed
  reviewer: Codex Architecture Governance review
  reviewed_at: '2026-07-28'
---

# REST vs GraphQL vs gRPC

## Problem and intent

Select an API interaction model from consumers, query shape, streaming, compatibility, caching, and operational constraints.

## Mechanism

REST exposes resource representations through HTTP semantics; GraphQL evaluates a typed query against a schema; gRPC invokes generated service methods over Protocol Buffers and HTTP/2.

## Options

### REST over HTTP

- Fit: Resource-oriented public or browser APIs benefit from HTTP tooling and caching.
- Avoid: Clients need arbitrary graph-shaped aggregation or high-rate typed streaming.
- Cost: Endpoint/version discipline and possible over/under-fetching.
- Failure: Action endpoints, ambiguous status semantics, or breaking representations accumulate.
### GraphQL

- Fit: Many client views need different compositions over a governed graph.
- Avoid: Simple resources suffice or query cost cannot be controlled.
- Cost: Schema governance, resolver performance, authorization, and query limits.
- Failure: N+1 resolution or unbounded queries exhaust backends.
### gRPC

- Fit: Controlled service-to-service clients need generated types, low overhead, or streaming.
- Avoid: Direct browser/public interoperability and ordinary HTTP caching dominate.
- Cost: IDL/toolchain coupling, proxies, observability, and compatibility rules.
- Failure: Breaking field reuse or deadline propagation failures disrupt clients.

## Fit when

At least one named option fits a measured quality scenario and the team can own its
required failure and recovery behavior.

## Avoid when

The choice is driven only by a technology name, hypothetical scale, or a problem
already solved by the current design.

## Required capabilities

Consumer inventory, compatibility policy, authentication and field-level authorization, error semantics, deadlines, observability, payload/query limits, and generated-contract discipline where used.

## Benefits

Aligns API mechanics with actual consumers instead of standardizing all interaction on one fashionable protocol.

## Costs and liabilities

Supporting multiple protocols adds gateways and duplicated policy; forcing one protocol creates local workarounds.

## Failure modes

GraphQL N+1 and authorization gaps, REST chatty aggregation, gRPC deadline/compatibility mistakes, or leaking internal schemas publicly.

## Alternatives

Compare the current design and the named options—REST over HTTP, GraphQL, gRPC—against the same
quality scenarios; do not compare feature lists without operating consequences.

## Migration and exit

Stabilize domain operations behind an application boundary, pilot the new protocol for one consumer, run contract tests and telemetry in parallel, then retire the old adapter only after consumers migrate.

## Evidence to inspect

Consumer environments, request shapes, payload and round-trip traces, streaming needs, cache behavior, schema change history, gateway support, and team tooling.

## Evidence that changes the recommendation

REST is the default for ordinary resource APIs; GraphQL earns its cost with real composition diversity; gRPC earns it in controlled typed and streaming service links.

## Quality trade-offs

Flexibility, interoperability, runtime efficiency, cacheability, and schema governance pull in different directions.

## Claim map

- GRAPHQL-SCHEMA: GraphQL executes client-specified typed queries against a schema.
- GRPC-CONTRACT: gRPC uses service definitions to generate clients and servers.
- HTTP-SEMANTICS: HTTP methods and status codes provide standardized resource interaction semantics.

## Volatile facts

Product versions, protocol/library support, service limits, pricing, licensing, and
security advisories must be rechecked in the cited official sources at decision time.
The mechanisms and decision criteria above are maintained separately from those facts.
