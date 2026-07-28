---
name: mobile-architecture-audit
description: Specialized architecture audit for mobile applications, especially iOS and SwiftUI. Use when assessing local persistence, offline behavior, synchronization and conflicts, migrations, background execution, notifications, networking and caches, state ownership, privacy permissions, battery efficiency, or excessive client-side business logic. Extends rather than replaces the general project architecture audit.
---

# Audit mobile architecture

Assess correctness across application lifecycle transitions, unreliable networks, local persistence, and operating-system constraints.

## Load the contract

Read these files completely:

- `../../resources/references/review-contract.md`
- `../../resources/references/mobile-rules.md`
- `../../resources/rules/mobile-core.yaml`
- `../../resources/knowledge/domains/catalog.yaml`

Load the project profile, constraints, and critical flows. Pair with `project-architecture-audit` for backend, shared contracts, or full-product scope.

## Workflow

1. Map state ownership across views, domain logic, repositories, local stores, caches, remote APIs, extensions, widgets, and background tasks.
2. Trace the critical flows through cold launch, foreground/background transitions, offline mode, retries, cancellation, and process termination.
3. Trace schema and data migrations, including downgrade assumptions, partial failure, backup/restore, and store corruption handling.
4. Trace synchronization identities, ordering, conflict policy, tombstones, idempotency, and eventual consistency.
5. Inspect notification scheduling, authorization changes, timezone and calendar behavior, deduplication, cancellation, and reconciliation.
6. Inspect network caching, stale data policy, connectivity assumptions, request cancellation, and error recovery.
7. Inspect SwiftUI or equivalent state lifetimes, actor/thread isolation, observation boundaries, and test seams.
8. Inspect privacy manifests, permission purpose, sensitive storage, logs, analytics, and data deletion.
9. Assess battery, background execution, and resource pressure against actual product requirements.

Do not flag local-first architecture, SQLite/Core Data/SwiftData, singletons, or client-side logic without proving a violated product invariant.

## Verification handoff and output

Apply the candidate evidence requirements in `review-contract.md`. Leave every
finding at `verification.status: candidate`.

Write persistent artifacts under `.architecture/reviews/` using kind `mobile`:

- `<timestamp>-mobile-candidates.yaml`;

Start machine-readable output from `../../resources/templates/review.yaml` and set `review.kind` to `mobile`.

Validate YAML with `architecture_tool.py validate-review`.

Hand off architecture, candidate strengths and risks, lifecycle and
critical-flow impact, coverage, counter-evidence, and limitations. Use
`$architecture-finding-verifier` for confirmed conclusions and the final
report. Do not prescribe fixes.
