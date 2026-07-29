---
id: technology.fastapi
kind: technology-profile
version: 2.0.0
status: active
domains:
- backend-api
triggers:
- fastapi
- asgi
quality_attributes:
- maintainability
related:
- domain.backend-api
- decision.request-vs-background-job
last_reviewed: '2026-07-28'
review_after_days: 90
source_policy: official-docs-required
sources:
- title: FastAPI features
  url: https://fastapi.tiangolo.com/features/
  authority: official
  supports:
  - FASTAPI-OPENAPI
- title: FastAPI async guidance
  url: https://fastapi.tiangolo.com/async/
  authority: official
  supports:
  - FASTAPI-ASYNC
dynamic_facts: true
version_range: Current supported stable releases; verify official documentation before a project decision.
maturity: golden
curation:
  method: assisted-reviewed
  reviewer: Codex Architecture Governance review
  reviewed_at: '2026-07-28'
---

# FastAPI

## Problem and intent

Evaluate FastAPI as a Python API delivery adapter without letting framework conveniences define the application architecture.

## Mechanism

Keep route functions thin: authenticate and validate, invoke an application use case, commit at an owned transaction boundary, and map typed results/errors to the HTTP contract.

## Operating model

FastAPI is an ASGI web framework that maps Python type annotations and dependency declarations to request validation, OpenAPI generation, and async or sync endpoint execution. The application still owns domain, transaction, authorization, and background-work boundaries.

## Capability boundaries

Use it for HTTP routing, validated request/response models, dependency composition, OpenAPI contracts, and ASGI integration. Do not treat dependencies as a service locator, background tasks as a durable job system, or Pydantic transport models as domain ownership.

## Fit when

The team owns Python/ASGI operations and values typed validation and OpenAPI for HTTP APIs.

## Avoid when

An existing framework already meets the need, CPU-bound work dominates the request path, or the team cannot operate Python packaging and ASGI lifecycle behavior.

## Required capabilities

Supported Python/runtime policy, pinned dependencies, explicit lifespan and resource ownership, request/response schemas, authorization at use-case boundaries, transaction policy, timeout/body limits, and integration/contract tests.

## Benefits

Provides concise typed HTTP adapters and generated API documentation while retaining ordinary Python application structure.

## Costs and liabilities

Framework and validation-library upgrades can affect generated schemas and behavior; async code introduces cancellation and blocking-I/O obligations.

## Failure modes

Blocking calls inside async handlers, request-scoped transactions leaking, trusting validation as authorization, incompatible OpenAPI drift, in-process tasks lost on restart, and overly large dependency graphs.

## Alternatives

Use the repository's current Python web framework, a smaller ASGI layer for minimal endpoints, or a non-Python stack when organizational ownership dominates.

## Migration and exit

Wrap one use case behind a FastAPI adapter, snapshot the OpenAPI contract, load-test sync/async dependencies, verify shutdown and transaction cleanup, then migrate routes without moving domain rules into handlers.

## Evidence to inspect

Current Python stack, route/use-case separation, generated OpenAPI diff, dependency lifecycle, blocking-call traces, concurrency/load tests, transaction cleanup, security tests, and deployment shutdown logs.

## Evidence that changes the recommendation

Reject adoption when it duplicates a healthy framework or when measured runtime and team constraints do not fit; recheck current compatibility in official release documentation.

## Quality trade-offs

Developer speed and typed contracts trade against framework coupling, Python runtime limits, async correctness, and schema migration work.

## Claim map

- FASTAPI-OPENAPI: FastAPI uses Python types to validate data and generate OpenAPI-based documentation.
- FASTAPI-ASYNC: FastAPI supports both async and normal path-operation functions with different execution behavior.

## Volatile facts

Runtime versions, limits, compatibility, security advisories, pricing, and licensing
must be confirmed from the cited official source at decision time. The stable operating
mechanism remains distinct from those current facts.
