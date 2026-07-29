# Codex Architecture Governance

An installable Codex plugin for evidence-backed architecture audits, solution
decisions, remediation, and deterministic governance across repositories,
specialized AI/mobile systems, and project portfolios.

The plugin treats missing architecture capability as part of the review:
confirmed gaps are diagnosed, compared against viable solutions, planned, and
gated. It also prevents an unverified model opinion from becoming policy.

```text
candidate audit
→ independent verification
→ trusted review
→ architecture solution decision
→ remediation plan
→ layered quality gate
```

Knowledge curation is a maintainer-only workflow that supplies sourced, fresh
decision knowledge without expanding the public end-user Skill surface.

## Included Skills

| Skill | Responsibility |
| --- | --- |
| `project-architecture-audit` | Audit one repository's boundaries, data, contracts, reliability, security, operations, tests, deployment, debt, and proportionality. |
| `ai-agent-architecture-audit` | Audit model, context, Memory, retrieval, tools, injection, approval, recovery, evaluation, cost, latency, and evidence boundaries. |
| `mobile-architecture-audit` | Audit local state, sync, migrations, background work, notifications, privacy, caching, and lifecycle behavior. |
| `portfolio-architecture-audit` | Audit duplication, stack sprawl, shared capabilities, dependencies, data flows, ownership, and hidden coupling across registered projects. |
| `architecture-finding-verifier` | Challenge candidates, resolve evidence, assign V0–V5 verification, and produce a provenance-bound trusted review. |
| `architecture-solution-advisor` | Compare keep-current and structural options against quality scenarios, constraints, team capability, migration risk, cost, and lock-in. |
| `architecture-remediation-planner` | Convert an accepted solution decision into ordered migration slices, protections, stop conditions, rollback, and acceptance criteria. |
| `architecture-quality-gate` | Apply deterministic contract, finding, change, and release policy to trusted artifacts. |

The source-only curator lives at
`maintainer/skills/architecture-knowledge-curator/`; the installable plugin
exposes exactly the eight workflows above.

## What is executable

`resources/` contains the shared runtime:

- JSON Schemas for profiles, reviews, Findings, decisions, plans, policy,
  baselines, risk acceptance, knowledge, providers, rules, behavior
  benchmarks, context manifests, and informational governance runs;
- nineteen machine-readable core and domain Rule Packs, plus repository-local
  organization packs, with complete-coverage enforcement;
- ten Markdown/frontmatter Knowledge Packs containing 205 sourced entries,
  plus 128 read-only 0.2 compatibility entries;
- eleven executable Evidence Provider contracts with safe project-local
  configuration, structured-output validation, and tamper-evident run records;
- a portable Python CLI for initialization, validation, provenance binding,
  Git evidence resolution, review diffing, provider execution, signature
  verification, repository-facts inspection, Profile construction, task-scoped
  knowledge selection, coverage validation, safe artifact migration,
  benchmark scoring, SARIF, and gates.

The repository itself owns CI, tests, behavior benchmarks, contribution policy,
dependency locks, deterministic packaging, SBOM generation, and release
attestation. The accepted boundaries are recorded in
[the 1.1 governance decision](docs/decisions/2026-07-28-adopt-trusted-governance-1.1.md).
The [comprehensive review implementation matrix](docs/comprehensive-review-implementation.md)
maps every material recommendation to executable capability and evidence.
The [target architecture](docs/target-architecture.md) and
[0.3 implementation matrix](docs/target-architecture-implementation.md)
describe the facts, knowledge, workflow, and trust boundaries.
See [governance modes](docs/governance-modes.md) for the lightweight Advisory,
Governed, and Enforced operating tiers.
The accepted [context-precision decision](docs/decisions/2026-07-29-adopt-context-precision-and-tiered-governance.md)
records why historical artifacts are preserved and why run records remain
non-authoritative.

## Requirements and installation

The Skill instructions are Markdown. The deterministic runtime supports Python
3.11–3.13 and requires PyYAML and jsonschema. Install the fully hashed runtime
lock for reproducibility:

```bash
python3 -m pip install --require-hashes \
  -r /path/to/plugin/requirements-runtime.lock
```

`requirements.txt` keeps the supported version ranges for downstream
resolvers. Runtime execution uses no network, credentials, telemetry, hosted
service, or MCP server.

For repository development:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --require-hashes -r requirements-dev.lock
```

Windows PowerShell uses `.venv\Scripts\Activate.ps1`.

## Initialize project governance

```bash
python3 resources/scripts/architecture_tool.py init-project \
  --repo /path/to/repository \
  --name "Example Project" \
  --type service \
  --quality recoverability \
  --review project-architecture
```

The command refuses an existing destination and creates:

```text
.architecture/
├── profile.yaml
├── repository-facts.yaml
├── constraints.md
├── critical-flows.md
├── gate-policy.yaml
├── baseline.yaml
├── risk-acceptances.yaml
├── evidence-providers.yaml
├── evidence/
├── rules/
├── runs/
└── reviews/
```

`profile.yaml` selects project qualities, reviews, and Rule Packs.
`repository-facts.yaml` contains deterministic observations; it never contains
a recommendation. Fact roles distinguish runtime/production evidence from
tests, benchmark fixtures, examples, documentation, generated code, and
vendor trees; only runtime and production facts infer product architecture.
Before each audit or decision, `select-knowledge` creates a task-scoped
`knowledge-selection.yaml` containing exact entry hashes, kind/maturity,
reasons, exclusions, total/per-kind context budgets, and creation-time
Selector/Knowledge/policy provenance. Schema 1.3 replays with the current
runtime only when those provenance bindings still match, so a future Selector
does not retroactively invalidate a historical selection.
`constraints.md` records real limits. `critical-flows.md` defines protected
runtime behavior. Findings, decisions, and plans are stored under `reviews/`.
Organization rules can be versioned as Rule Packs under
`.architecture/rules/`; duplicate IDs cannot shadow bundled packs.

Validate a configuration:

```bash
python3 resources/scripts/architecture_tool.py validate-project /path/to/repository
python3 resources/scripts/validate_knowledge.py
```

## Trusted reviews and evidence

Schema `1.0` remains readable for migration and historical records. Only schema
`1.1` or `1.2` can enter deterministic enforcement. New project, AI-agent, and
mobile audits use `1.2`. A trusted verified Review binds:

- repository identity, Git commit, dirty-tree state, profile hash, and explicit
  scope manifest;
- exact repository-facts and task-scoped knowledge-selection bytes;
- exact Rule Pack versions and SHA-256 hashes;
- a source candidate review and its SHA-256;
- complete coverage for every loaded rule;
- explicit coverage for every declared critical flow;
- an authorized verifier, verification run, V0–V5 level, and semantic Finding
  fingerprint;
- resolvable Git paths, commits, blobs, symbols, line ranges, or declared
  provider-owned evidence;
- role separation required by policy and, for V5, a detached SSH signature
  verified against the repository's allowed-signers file.

Generate deterministic bindings before independent verification:

```bash
python3 resources/scripts/architecture_tool.py review-bindings \
  --project /path/to/repository \
  --candidate .architecture/reviews/example-candidates.yaml
```

For a new audit, establish inputs first:

```bash
python3 resources/scripts/architecture_tool.py inspect-repository \
  --repo /path/to/repository \
  --output /path/to/repository/.architecture/repository-facts.yaml
python3 resources/scripts/architecture_tool.py select-knowledge \
  --facts /path/to/repository/.architecture/repository-facts.yaml \
  --profile /path/to/repository/.architecture/profile.yaml \
  --task "Current architecture audit" \
  --skill project-architecture-audit \
  --output /path/to/repository/.architecture/knowledge-selection.yaml
```

For an architecture decision whose wording could cross semantic domains, bind
the decision namespace explicitly. For example, a locally installed plugin
runtime is not local-first client data authority:

```bash
python3 resources/scripts/architecture_tool.py select-knowledge \
  --facts .architecture/repository-facts.yaml \
  --profile .architecture/profile.yaml \
  --task "Preserve the local-first plugin runtime" \
  --skill architecture-solution-advisor \
  --decision-intent plugin-runtime-topology \
  --output .architecture/decision-knowledge-selection.yaml
```

Then validate and resolve evidence:

```bash
python3 resources/scripts/architecture_tool.py validate-review \
  /path/to/verified.yaml --project /path/to/repository
python3 resources/scripts/architecture_tool.py verify-evidence \
  --repo /path/to/repository --review /path/to/verified.yaml
python3 resources/scripts/architecture_tool.py verify-review-signature \
  --project /path/to/repository --review /path/to/verified.yaml
```

Finding IDs remain readable identifiers. Fingerprints bind baselines, waivers,
and risk acceptance to finding semantics and evidence identity, preventing an
old approval from silently suppressing a changed risk.

Evidence Providers are opt-in and never invoke a shell. The runner resolves
and hashes the actual executable, uses a safe environment allowlist, enforces a
timeout, captures stdout/stderr, validates JSON, SARIF, or JUnit structure, and
binds every output to the project, commit, provider definition, and
configuration:

```bash
python3 resources/scripts/architecture_tool.py evidence-providers --project .
python3 resources/scripts/architecture_tool.py run-evidence-provider \
  --project . --provider test-results
python3 resources/scripts/architecture_tool.py validate-evidence-run \
  .architecture/evidence/<run>.yaml --project . --require-passed
```

Compare two valid review snapshots without treating narrative changes as a new
audit:

```bash
python3 resources/scripts/architecture_tool.py review-diff \
  --before previous.yaml --after current.yaml --project .
```

## Decisions, plans, and risk acceptance

Remediation decisions reference a trusted Review by ID and SHA-256. Greenfield
decisions instead bind a validated `architecture-design-brief.yaml`; they
never require or manufacture an empty review. Schema `1.2` remediation and
schema `1.3` Greenfield Decisions compare at least three options, including keep-current, bind
the exact task selection and per-entry Markdown versions and hashes, and score
quality, business, team, evolution, maturity, lock-in, and complexity
trade-offs. Generate their hashes first:

```bash
python3 resources/scripts/architecture_tool.py decision-bindings \
  --project . --review verified.yaml \
  --knowledge-selection .architecture/knowledge-selection.yaml
python3 resources/scripts/architecture_tool.py validate-decision \
  decision.yaml --review verified.yaml --project . --require-accepted
```

For a new system:

```bash
python3 resources/scripts/architecture_tool.py validate-design-brief \
  .architecture/architecture-design-brief.yaml
python3 resources/scripts/architecture_tool.py decision-bindings \
  --project . \
  --design-brief .architecture/architecture-design-brief.yaml \
  --knowledge-selection .architecture/decision-knowledge-selection.yaml
python3 resources/scripts/architecture_tool.py validate-decision \
  decision.yaml \
  --design-brief .architecture/architecture-design-brief.yaml \
  --project .
```

Plans bind the accepted decision and source review. A plan marked complete must
provide repository-relative, SHA-256-bound acceptance evidence for every
declared evidence type. Schema `1.2` items also bind Finding fingerprints,
selected knowledge IDs, assumptions, migration slices, rollback, and stop
conditions:

```bash
python3 resources/scripts/architecture_tool.py validate-plan \
  plan.yaml --review verified.yaml --decision decision.yaml --project .
```

Risk acceptance is not a status-only shortcut. It lives in the separate
`risk-acceptances.yaml` registry and requires:

- a matching Finding fingerprint;
- different accepter and approver identities;
- identities authorized by policy roles;
- rationale, compensating controls, acceptance time, and expiry.

Baselines and waivers are also fingerprint-bound and expiring.

## Layered deterministic gate

```bash
python3 resources/scripts/architecture_tool.py gate \
  --project /path/to/repository \
  --review .architecture/reviews/example-verified.yaml \
  --stage change \
  --sarif-output architecture-results.sarif
```

Stages are cumulative:

1. `contract`: schemas, provenance, identity, hashes, roles, and coverage;
2. `finding`: severity, confidence, verification level, status, baseline,
   waiver, and risk acceptance;
3. `change`: required review workflows, review age,
   exact/ancestor/diff-aware Git freshness, changed public contracts, required
   decisions, compatible migration or active remediation planning, dirty tree,
   signature policy, and evidence resolution. Governance-only commits may
   follow a review, but classified critical or security paths may not;
4. `release`: required evidence, accepted decisions, decision authority, and
   complete remediation with hashed acceptance evidence.

Exit codes are stable: `0` passes, `1` is a policy failure, and `2` is invalid
input or configuration. SARIF 2.1.0 output can be uploaded with GitHub's
`github/codeql-action/upload-sarif`. The bundled GitHub workflow template also
publishes the Check summary and updates a pull-request comment.

`product_mode` is a declared operating tier, not a bypass. A project using
Advisory mode does not initialize or invoke the gate; an explicitly invoked
gate evaluates its deterministic policy regardless of that label. High-risk
Governed/Enforced work may add a validated but non-authoritative trajectory
record under `.architecture/runs/`; it never substitutes for a Review,
Evidence Provider run, approval, or gate evidence.

## Behavior evaluation

`evals/cases.yaml` contains one direct, indirect, incomplete, negative, and
edge activation case for each of the eight public Skills: 40 cases total.
Separate corpora cover routing, knowledge selection, decision quality,
false-positive resistance, and artifact tampering. `benchmarks/` adds ten
adversarial code fixtures with ground truth, forbidden over-design
recommendations, and metrics for precision, recall, severity agreement,
evidence validity, prohibited recommendations, repeated-trial stability,
duration, optional token/cost usage, recommendation accuracy, over-design,
trade-off coverage, knowledge citation validity, rejected-option explanations,
and migration actionability.

The bundled Codex adapter limits outputs to machine Rule IDs and canonical
atomic trade-offs. It allows one disclosed evidence-only correction when an
initial path/line/excerpt citation is not verbatim; it never sends benchmark
ground truth to the model. Schema 1.4 run artifacts also bind the source
commit, relevant dirty state, execution environment, dependency lock,
configuration schemas, plugin manifest and Skill version, fixture tree hashes,
runner and adapter hashes, the reconstructible command template, exact
per-trial argument vectors, command/model executable fingerprints and version
outputs, and a hash-verified JSONL execution log. Interrupted trials leave a
failure log instead of disappearing.

Schema 1.5 adds a declared `base` / `full` / `compressed` context ablation.
Base has no Skill, Reference, or Knowledge content. Full uses the public Skill;
Compressed uses a compact workflow instruction; both share the same
workflow-required Knowledge per Skill. Each run records a corpus-level
declared-input character/byte proxy, not tokens or cost. Token, cost, and
tool-call totals remain `null` unless the executed surface reports them. See
[evaluation guidance](docs/evaluation.md) before interpreting or publishing an
A/B/C comparison.

The forward-test runner accepts a caller-supplied agent command:

```bash
python3 scripts/run_behavior_benchmark.py \
  --model MODEL --surface SURFACE --runtime-executable codex --repetitions 3 \
  --output benchmark-run.yaml -- \
  python3 scripts/codex_benchmark_adapter.py --model MODEL \
    --skill '{skill}' --fixture '{fixture}' --prompt '{prompt}'
python3 resources/scripts/architecture_tool.py benchmark-score \
  --ground-truth benchmarks/ground-truth.yaml --run benchmark-run.yaml \
  --output benchmark-score.json
```

The default score mode strictly replays runtime identity checks. For portable
review of a committed run on a different host, add
`--runtime-verification archived --artifact-commit COMMIT`; this binds the run
and JSONL bytes to Git and reports, rather than conceals, host-runtime mismatch.

The runner writes `benchmark-run.log.jsonl` beside the YAML result. Preserve
both files; the scorer rejects a missing, modified, incomplete, or
source-inconsistent provenance chain.

Version 0.4.0 preserves 60 real trials from two identified models on
`codex-cli 0.146.0-alpha.3.1`, including non-perfect results and limitations.
See the [model behavior evidence](benchmarks/reports/0.4.0-model-behavior.md)
and [evaluation guidance](docs/evaluation.md). The planned context-precision
migration is documented in [the 0.4.2 guide](docs/migrating-to-0.4.2.md).

## Open-source verification

Run the local gate:

```bash
python3 scripts/validate_repository.py
python3 resources/scripts/architecture_tool.py validate-project .
python3 resources/scripts/validate_knowledge.py
python3 -m pytest
python3 -m ruff check .
python3 -m ruff format --check .
python3 scripts/audit_licenses.py
python3 scripts/package_plugin.py --output-dir dist
python3 scripts/verify_checksum.py dist/*.zip.sha256
python3 scripts/generate_sbom.py \
  --archive dist/codex-architecture-governance-0.4.2.zip \
  --output dist/codex-architecture-governance-0.4.2.spdx.json
```

CI runs the supported Python boundary on Linux, macOS, and Windows. Tagged
releases rebuild the deterministic ZIP, attach its checksum and SPDX SBOM, and
create GitHub provenance plus SBOM attestations. See
[release verification](docs/releasing.md), [compatibility](docs/compatibility.md),
the [0.3 migration guide](docs/migrating-to-0.3.md), and the
[assurance model](docs/assurance-model.md). A scheduled workflow checks
knowledge freshness and opens or updates an issue; it never silently rewrites
sourced decision knowledge.

## Non-goals

The plugin does not prove that a system is secure or correct, autonomously
approve decisions or risk, discover unrelated repositories, implement audited
product code, operate a hosted dashboard, or replace specialist security,
privacy, performance, or compliance assessment.

## Contributing and license

Read [CONTRIBUTING.md](CONTRIBUTING.md), [GOVERNANCE.md](GOVERNANCE.md),
[SECURITY.md](SECURITY.md), and [SUPPORT.md](SUPPORT.md). The project is
licensed under [MIT](LICENSE). PAAD-derived concepts retain attribution in
[NOTICE](NOTICE) and [third_party/PAAD-MIT.txt](third_party/PAAD-MIT.txt).
