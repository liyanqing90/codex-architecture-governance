---
name: portfolio-architecture-audit
description: System-of-systems architecture setup and audit across multiple projects. Use when initializing `.architecture-portfolio` or reviewing duplicated capabilities, project boundary conflicts, technology-stack sprawl, shared infrastructure, cross-project data flows, hidden coupling, deployment and domain complexity, reusable components, or a one-year technical governance roadmap. Requires an explicit portfolio registry and does not replace per-project audits.
---

# Audit a project portfolio

Evaluate the portfolio as a system of systems. A locally reasonable design may still create global duplication, coupling, ownership ambiguity, or operational cost.

## Load the contract

Read these files completely:

- `../../resources/references/review-contract.md`
- `../../resources/references/knowledge-contract.md`
- `../../resources/references/portfolio-rules.md`
- `../../resources/rules/portfolio-core.yaml`
- `../../resources/knowledge/manifest.yaml`

Load `.architecture-portfolio/portfolio.yaml`, `shared-capabilities.yaml`, `technology-catalog.yaml`, and `dependency-map.yaml`. The registry defines scope. Do not silently discover unrelated repositories. If the registry is missing, stop and ask the user to initialize or identify the intended projects.

## Initialize a portfolio

When the user requests setup, run:

```bash
python3 ../../resources/scripts/architecture_tool.py init-portfolio \
  --root <portfolio-root> \
  --name "<portfolio name>" \
  --owner "<owner>"
```

Populate the explicit project registry and catalogs, then run `validate-portfolio`. Initialization creates an empty registry; never add repositories that the user did not place in scope.

## Workflow

1. Resolve every registered repository, profile, commit, owner, lifecycle state, and declared dependency. Record inaccessible projects.
2. For each accessible registered repository, run `inspect-repository` and
   `select-knowledge --skill portfolio-architecture-audit` against that
   repository's Profile with a compact `--context-output`. Persist facts,
   selection locks, and context indexes inside the registered project only when
   the user authorized project writes; otherwise use a temporary directory and
   record hashes in the portfolio evidence. Do not derive one project's stack
   from another project's files.
3. Run `validate-knowledge-context` for each context index with its exact
   `--selection`, `--facts`, and `--profile` paths. Read each compact context
   index only after validation succeeds and read its selected Markdown entries, union
   them by canonical ID, and retain every per-project inclusion reason. Keep
   exclusions in the machine lock rather than model context. Do not load the
   whole knowledge tree.
4. Normalize a portfolio inventory:
   - business and platform capabilities;
   - identity, permissions, notifications, scheduling, AI gateways, MCP/Skill/Agent runtimes, design systems, configuration, telemetry, and deployment;
   - databases, caches, queues, object stores, external providers, domains, and environments;
   - APIs, events, shared schemas, data owners, and cross-project flows.
5. Produce a technology matrix and dependency/data-flow maps.
6. Compare implementations by semantics, lifecycle, reliability, privacy, and ownership—not name or technology alone.
7. Identify:
   - repeated capability with a credible consolidation case;
   - intentional duplication that preserves autonomy;
   - shared infrastructure with unclear ownership or blast radius;
   - stack diversity without a justified quality requirement;
   - a project that is becoming a module of another;
   - changes in one project that can silently break another.
8. Require candidate evidence from every affected project. One repository's assumption is not evidence about another.
9. Classify recommendations only as questions or governance opportunities in the audit; use the remediation planner for actual consolidation plans.

For a large portfolio, use up to four read-only specialists when available, partitioned by capabilities, data/integration, runtime/infrastructure, and governance. Keep synthesis and verification in the main agent.

## Output

Write under `.architecture-portfolio/reviews/`:

- `<timestamp>-portfolio-candidates.yaml`;

Start machine-readable output from `../../resources/templates/portfolio-review.yaml`; replace every example value.

The verification handoff must include:

- portfolio architecture diagram;
- project and technology matrix;
- shared-capability and duplication inventory;
- infrastructure dependency and cross-project data-flow maps;
- candidate coupling and ownership risks;
- boundaries that should remain independent;
- open governance questions and a horizon-based roadmap outline.

Keep the roadmap descriptive; do not turn unverified consolidation ideas into committed plans.

Leave every finding at `verification.status: candidate`, validate YAML with
`architecture_tool.py validate-review`, and use
`$architecture-finding-verifier` for confirmed conclusions and the final
report. Do not modify project repositories.

Portfolio Review 1.1 remains the compatibility contract for the aggregate
artifact; each registered repository's facts and knowledge selections are
individually hash-bound as evidence. Never claim the aggregate artifact has
Review 1.2 project-profile bindings.
