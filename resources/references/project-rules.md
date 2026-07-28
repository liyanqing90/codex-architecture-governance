# Project architecture rule set

Assess each applicable rule. A rule can yield a risk, a strength, or no finding.

| Rule ID | Domain | Invariant to inspect |
|---|---|---|
| `PROJECT.BOUNDARY.001` | Module boundaries | A module has a coherent responsibility and an explicit public boundary. |
| `PROJECT.DEPENDENCY.001` | Dependency direction | Stable domain or policy code does not depend on volatile delivery or infrastructure details without an intentional adapter. |
| `PROJECT.COHESION.001` | Cohesion | A logical change is owned by a bounded set of components; unrelated behavior is not accumulated in a grab-bag. |
| `PROJECT.FRONTEND.001` | Frontend/backend responsibility | Security, authoritative validation, and cross-client business invariants are enforced at an authoritative boundary. |
| `PROJECT.DATA.001` | Data model | Persisted models express identity, lifecycle, constraints, and relationships without contradictory sources of truth. |
| `PROJECT.OWNERSHIP.001` | Data ownership | Every authoritative datum has one declared owner and controlled writers. |
| `PROJECT.CONTRACT.001` | API/event contracts | Interfaces have explicit semantics, validation, errors, compatibility expectations, and ownership. |
| `PROJECT.TRANSACTION.001` | Transactions | Atomicity boundaries match business invariants; cross-system partial failure has an explicit strategy. |
| `PROJECT.IDEMPOTENCY.001` | Idempotency | Retried or duplicated commands cannot repeat irreversible side effects. |
| `PROJECT.RELIABILITY.001` | Resilience | Timeouts, retries, backoff, cancellation, overload, and degraded behavior are deliberate and observable. |
| `PROJECT.STATE.001` | State machines | Long-lived workflows have explicit states, legal transitions, recovery, and terminal outcomes. |
| `PROJECT.SECURITY.001` | Security | Authentication, authorization, secrets, trust boundaries, and least privilege are enforced at owning boundaries. |
| `PROJECT.PRIVACY.001` | Privacy | Collection, retention, access, export, deletion, and logging follow declared data classifications. |
| `PROJECT.OBSERVABILITY.001` | Observability | Critical flows can be correlated across logs, metrics, traces, jobs, and external dependencies. |
| `PROJECT.CONFIG.001` | Configuration | Configuration has one precedence model, validation, safe defaults, and no secret leakage. |
| `PROJECT.PERFORMANCE.001` | Performance | Known latency, throughput, memory, storage, or cost budgets are protected by evidence and backpressure. |
| `PROJECT.TEST.001` | Testability | Critical invariants have stable seams and behavioral protection at the owning boundary. |
| `PROJECT.DEPLOY.001` | Build/deploy | Artifacts are reproducible; rollout, rollback, migration ordering, and environment drift are controlled. |
| `PROJECT.CHANGE.001` | Evolution | Public and persisted contracts can evolve without silent consumer breakage. |
| `PROJECT.DEBT.001` | Technical debt | Debt has a demonstrated change or operational cost, not just disliked style. |
| `PROJECT.DESIGN.001` | Proportionality | Abstractions and services solve present variability or isolation needs rather than hypothetical futures. |

## Investigation guidance

- Trace at least one primary and one failure path for each critical flow.
- Inspect tests and runtime configuration, not only implementation files.
- Mark distributed-only concerns not applicable for a single-process application.
- Treat a shared database, synchronous call, singleton, or large module as a lead. Prove ownership, coupling, recovery, or change-cost impact before reporting a flaw.
- Report strong patterns that should be preserved during remediation.
