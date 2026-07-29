---
id: decision.monolith-vs-microservices
kind: decision-guide
version: 2.0.0
status: active
domains:
- backend-api
- distributed-systems
triggers:
- monolith
- microservices
- services
quality_attributes:
- maintainability
related:
- foundation.system-boundaries
- pattern.outbox
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure microservices architecture style
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices
  authority: official
  supports:
  - SERVICE-BOUNDARY
- title: 'Martin Fowler: Monolith First'
  url: https://martinfowler.com/bliki/MonolithFirst.html
  authority: maintainer
  supports:
  - MONOLITH-MODULARITY
maturity: golden
curation:
  method: assisted-reviewed
  reviewer: Codex Architecture Governance review
  reviewed_at: '2026-07-28'
---

# Modular Monolith vs Microservices

## Problem and intent

Choose deployment boundaries from independent change and scaling needs, not from module count or anticipated prestige.

## Mechanism

A modular monolith enforces domain ownership inside one deployable and transaction boundary. Microservices turn selected domain boundaries into separately deployed, versioned, observed, and failure-isolated services.

## Options

### Modular monolith

- Fit: A small team, coupled release cadence, and shared operational envelope.
- Avoid: Independent scaling, compliance, or release ownership is already measurable.
- Cost: Discipline is needed to keep modules and data ownership explicit.
- Failure: Internal imports and shared tables erode boundaries into a big ball of mud.
### Selective service extraction

- Fit: One bounded context has proven independent change, load, data, or isolation needs.
- Avoid: The candidate boundary still changes transactionally with neighbors.
- Cost: Network contracts, deployment, tracing, eventual consistency, and on-call load.
- Failure: A distributed monolith preserves coupling while adding network failure.
### Broad microservice decomposition

- Fit: Multiple autonomous teams and operational capabilities can own many services.
- Avoid: A small team cannot sustain platform and incident overhead.
- Cost: Highest delivery, runtime, data, and governance complexity.
- Failure: Service sprawl, incompatible contracts, and cross-service transaction failure.

## Fit when

At least one named option fits a measured quality scenario and the team can own its
required failure and recovery behavior.

## Avoid when

The choice is driven only by a technology name, hypothetical scale, or a problem
already solved by the current design.

## Required capabilities

Domain/data ownership, dependency rules, consumer contracts, deployment and rollback, distributed tracing, service SLOs, and teams able to own incidents.

## Benefits

A proportional boundary choice preserves simplicity while leaving a measured path to independent deployment.

## Costs and liabilities

Microservices multiply runtime and coordination surfaces; monoliths require strong internal enforcement.

## Failure modes

Shared databases, chatty synchronous calls, cyclic service dependencies, coordinated releases, and extraction before the domain stabilizes.

## Alternatives

Compare the current design and the named options—Modular monolith, Selective service extraction, Broad microservice decomposition—against the same
quality scenarios; do not compare feature lists without operating consequences.

## Migration and exit

First establish modules and owner-owned tables; measure change/load coupling; extract one edge boundary with an anti-corruption interface and reversible routing before considering another.

## Evidence to inspect

Commit and release coupling, team ownership, hot spots, scaling asymmetry, transaction boundaries, incident history, dependency graph, and deployment capability.

## Evidence that changes the recommendation

Prefer a modular monolith until independent deployment or isolation produces measurable value greater than distributed-systems cost.

## Quality trade-offs

Services improve independent evolution and isolation but trade away local transactions, simple debugging, and low operational overhead.

## Claim map

- SERVICE-BOUNDARY: Microservice boundaries carry independent deployment and distributed interaction consequences.
- MONOLITH-MODULARITY: A single deployable can still enforce explicit internal modules.

## Volatile facts

Product versions, protocol/library support, service limits, pricing, licensing, and
security advisories must be rechecked in the cited official sources at decision time.
The mechanisms and decision criteria above are maintained separately from those facts.
