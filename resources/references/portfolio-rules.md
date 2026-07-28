# Portfolio architecture rule set

Assess each rule across the explicitly registered projects.

| Rule ID | Domain | Invariant to inspect |
|---|---|---|
| `PORTFOLIO.BOUNDARY.001` | Project boundaries | Each project has an independent product or platform responsibility and a clear reason to exist separately. |
| `PORTFOLIO.CAPABILITY.001` | Shared capabilities | Repeated capabilities are inventoried and intentionally shared, duplicated, or retired. |
| `PORTFOLIO.IDENTITY.001` | Identity/permissions | Authentication and authorization semantics are consistent where identities cross projects. |
| `PORTFOLIO.AI.001` | AI platform | Model gateways, tool runtimes, MCP, Skills, memory, and evaluation capabilities are shared only where semantics and risk align. |
| `PORTFOLIO.UI.001` | Design systems | Shared visual and interaction components have explicit consumers, versioning, and ownership. |
| `PORTFOLIO.DATA.001` | Data ownership | Cross-project data has one authoritative owner, classified flows, and controlled replication. |
| `PORTFOLIO.CONTRACT.001` | Contracts | APIs, events, shared schemas, and libraries have compatibility and consumer discovery. |
| `PORTFOLIO.COUPLING.001` | Hidden coupling | A project can change, deploy, or fail without undocumented simultaneous changes elsewhere. |
| `PORTFOLIO.STACK.001` | Technology stack | Diversity follows different quality needs or constraints rather than accidental preference. |
| `PORTFOLIO.STORAGE.001` | Data stores | PostgreSQL, Redis, SQLite, graph stores, queues, and object stores have explicit roles and operators. |
| `PORTFOLIO.OBSERVABILITY.001` | Observability | Logs, metrics, traces, correlation, retention, and alert ownership support cross-project flows. |
| `PORTFOLIO.CONFIG.001` | Configuration/secrets | Environment, secrets, flags, and configuration follow a coherent ownership and rollout model. |
| `PORTFOLIO.DEPLOY.001` | Deployment | Environments, domains, certificates, release paths, and rollback responsibilities remain operable. |
| `PORTFOLIO.INFRA.001` | Shared infrastructure | Shared services have SLOs, capacity, tenancy, change control, and a known blast radius. |
| `PORTFOLIO.OWNERSHIP.001` | Governance | Every shared capability and cross-project contract has an owner and lifecycle. |
| `PORTFOLIO.REUSE.001` | Reuse economics | Consolidation reduces total cost after migration, coordination, availability, and coupling costs. |
| `PORTFOLIO.ROADMAP.001` | Evolution | Governance work is sequenced around real dependencies and product horizons. |

## Duplication decision test

Do not recommend consolidation until all are supported:

1. The implementations express substantially the same semantics.
2. Consumers need compatible reliability, privacy, latency, and release behavior.
3. A stable owner and support model exist.
4. Migration cost is lower than continued duplication over the review horizon.
5. Sharing will not create a larger blast radius or synchronized release burden.

Classify repeated code as:

- intentional autonomy;
- candidate library;
- candidate platform service;
- product-specific implementation;
- unknown pending evidence.

## Required evidence for cross-project findings

- evidence from every affected repository or runtime;
- the cross-project flow or dependency;
- owners and consumers;
- failure/change propagation;
- counter-evidence supporting independence;
- observed or forecast cost with assumptions stated.
