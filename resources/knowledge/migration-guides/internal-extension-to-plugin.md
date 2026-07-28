---
id: migration.internal-extension-to-plugin
kind: migration-guide
version: 1.0.0
status: active
domains:
- extensibility
triggers:
- internal
- extension
- plugin
quality_attributes: []
related: []
legacy_ids:
- migration:internal-extension-to-plugin
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Cloud Design Patterns
  url: https://learn.microsoft.com/en-us/azure/architecture/patterns/
  authority: official
---

# Internal Extension to Plugin Platform

## Problem and intent

- Extract a stable capability contract
- manifest
- permissions
- compatibility
- and isolation around existing extensions.

## Mechanism

- Do not expose third-party loading until authority and revocation are enforceable.

## Fit when

- Independent extension release or third-party participation becomes a product requirement.

## Avoid when

- Extensions remain internal and deploy with the host.

## Required capabilities

- extension-inventory
- contract-tests
- permission-model
- provenance

## Benefits

- Incremental contract hardening before ecosystem exposure.

## Costs and liabilities

- Adapters
- compatibility promises
- sandboxing
- and migration of internal access.

## Failure modes

- publishing-host-internals
- permissions-after-launch

## Alternatives

- Keep the current design and apply a smaller local correction.

## Migration and exit

- inventory-capabilities
- define-manifest
- mediate-host-calls
- isolate
- sign
- open-publisher-boundary

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
