---
id: reference.secure-plugin-host
kind: reference-architecture
version: 1.0.0
status: active
domains:
- extensibility
triggers:
- secure
- plugin
- host
quality_attributes: []
related: []
legacy_ids:
- reference-architecture:secure-plugin-host
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Azure Architecture Styles
  url: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
  authority: official
---

# Secure Plugin Host

## Problem and intent

- Load signed extensions through schema manifests
- compatibility checks
- explicit capability grants
- isolated execution
- and lifecycle control.

## Mechanism

- Expose capabilities rather than host implementation internals.

## Fit when

- Independent extension publishers and release lifecycles are a product requirement.

## Avoid when

- Internal modules within one trust and release boundary are sufficient.

## Required capabilities

- manifest-contract
- provenance
- capability-policy
- sandbox
- version-matrix

## Benefits

- Controlled ecosystem extensibility and host stability.

## Costs and liabilities

- Sandbox
- compatibility
- revocation
- permissions
- support
- and publisher trust.

## Failure modes

- plugins-import-host-internals
- unrestricted-file-network-access

## Alternatives

- sandboxed-process
- wasm
- remote-extension

## Migration and exit

- internal-extension-to-plugin

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
