# Project profile guide

Use a profile to select applicable architecture rules, not to predetermine findings.

## Field meanings

- `project.id`: stable portfolio and finding prefix; do not derive it from a temporary folder.
- `project.type`: product/system characteristics such as `ai-agent-platform`, `personal-data-system`, `ios-application`, `reminder-system`, `web-application`, or `service`.
- `lifecycle`: changes the acceptable migration and maintenance burden.
- `criticality`: product impact, not code complexity.
- `owners`: accountable people or teams; use `unassigned` only during initialization.
- `critical_qualities`: compatibility shorthand for the few qualities whose
  failure materially harms the product.
- `quality_attributes`: prioritized, justified, measurable quality scenarios
  and their evidence.
- `business_context`: product stage, team ownership, distributed-system
  experience, on-call, change frequency, regulation, scale, throughput,
  latency, availability, data volume, consistency, offline behavior,
  deployment, budget, deadlines, stack constraints, and migration limits.
- `required_reviews`: explicit workflow IDs that must each resolve to a current
  trusted Review before the Contract or Release Gate can pass.
- `review_requirements`: maps every required workflow to one Review kind and
  the exact machine Rule Packs it must cover.
- `rule_packs`: the union of Rule Packs that review requirements may select.
- `data_classification`: highest or mixed classification handled by the project.
- project file paths: resolve within repository root; absolute and `..` escape
  paths are rejected. Portfolio registries explicitly authorize external
  repository locations separately.

Do not encode a current framework, database, or hosting vendor as an immutable constraint unless a real compatibility, cost, legal, or operational requirement makes it one.

## Constraint records for design

When a project asks for an open or constrained target architecture, preserve the
distinction between context and proof. A Brief 1.1 constraint record names its
ID, kind, disposition, target, scope, accountable authority, rationale, review
trigger, and optional Knowledge ID. Its disposition is one of:

- `required`: a candidate hard requirement that the Advisor must challenge for
  authority, conflict, feasibility, and hidden consequences before treating it
  as surviving;
- `preferred`: a negotiable preference that may lose to measured quality,
  compatibility, safety, cost, or operational evidence; or
- `prohibited`: a hard exclusion whose violating options are eliminated with an
  explicit reason.

Profile and Brief constraints are inputs. They do not prove that a design is
compliant, feasible, secure, or suitable. Keep facts, inferences, assumptions,
unknowns, and constraint assessments separate. Do not promote a detected
dependency, framework name, Knowledge entry, or owner assertion into a fixed
constraint without an authoritative reason.

For constrained Greenfield work, the Brief and Decision must assess every
declared constraint and bind the resulting target architecture. Required
conflicts with no surviving compliant variant are a stop condition, not a reason
to silently weaken the constraint.

## Suggested review selection

| Project characteristic | Additional review |
|---|---|
| AI agents, RAG, memory, model tools | `ai-agent-architecture` |
| iOS or mobile local state | `mobile-architecture` |
| personal, confidential, or restricted data | `privacy-review` and `data-architecture` |
| authentication, authorization, external tools | `threat-model` |
| multiple coordinated repositories | portfolio audit from the portfolio registry |

Selections are starting points. The explicit profile remains authoritative.

## Rule Pack selection

Every trusted Review loads exactly the packs assigned to its
`review_requirements` entry. A Review must include its kind's core pack:

| Review kind | Required core |
|---|---|
| `project` | `project-core` |
| `ai-agent` | `ai-agent-core` |
| `mobile` | `mobile-core` |
| `portfolio` | `portfolio-core` |

Project reviews may then add the relevant specialized packs:

| Characteristic | Specialized Rule Pack |
|---|---|
| browser application | `web-frontend` |
| network service or public API | `backend-api` |
| analytical or streaming data platform | `data-platform` |
| event-time or bounded-latency processing | `real-time-system` |
| multi-tenant product | `multi-tenant-saas` |
| identity or authorization boundary | `identity-authorization` |
| trading or financially consequential orders | `financial-trading` |
| devices and edge actuation | `iot-edge` |
| search or recommendation | `search-recommendation` |
| audio/video pipeline | `streaming-media` |
| test execution platform | `test-automation-platform` |
| independent extensions | `plugin-platform` |
| offline writable replicas | `local-first` |
| native desktop application | `desktop-application` |
| shared cloud workload platform | `cloud-native-platform` |

Do not load a specialized pack solely because a repository contains a matching
library. Select it when the corresponding product boundary or critical flow is
actually in scope.

Organization-specific packs may be stored as schema `1.1` YAML files under
`.architecture/rules/` (or `.architecture-portfolio/rules/`). Add their IDs to
the Profile union and the relevant review requirement. The validator rejects
duplicate IDs, including attempts to shadow a bundled pack, and rejects a pack
whose `review_kind` differs from the workflow kind.

## Initialization

Use `architecture_tool.py init-project`; it refuses to overwrite existing configuration. Then replace placeholders in:

- `profile.yaml`;
- `constraints.md`;
- `critical-flows.md`;
- `gate-policy.yaml`;
- `baseline.yaml`;
- `risk-acceptances.yaml`;
- `evidence-providers.yaml`.

Validate with `architecture_tool.py validate-project <repo>`.

Illustrative profiles are in:

- `../templates/cognera-profile.example.yaml`;
- `../templates/assetkeeper-profile.example.yaml`.

They are examples, not facts about the current repositories.
