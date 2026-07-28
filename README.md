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

Knowledge curation is a separate maintenance workflow that supplies sourced,
fresh decision knowledge without selecting a product architecture.

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
| `architecture-knowledge-curator` | Maintain quality models, styles, patterns, technology profiles, reference architectures, migrations, rules, and official-source freshness. |

## What is executable

`resources/` contains the shared runtime:

- JSON Schemas for profiles, reviews, Findings, decisions, plans, policy,
  baselines, risk acceptance, knowledge, providers, rules, and benchmarks;
- nineteen machine-readable core and domain Rule Packs, plus repository-local
  organization packs, with complete-coverage enforcement;
- eight sourced architecture knowledge catalogs containing 128 entries;
- eleven executable Evidence Provider contracts with safe project-local
  configuration, structured-output validation, and tamper-evident run records;
- a portable Python CLI for initialization, validation, provenance binding,
  Git evidence resolution, review diffing, provider execution, signature
  verification, benchmark scoring, SARIF, and gates.

The repository itself owns CI, tests, behavior benchmarks, contribution policy,
dependency locks, deterministic packaging, SBOM generation, and release
attestation. The accepted boundaries are recorded in
[the 1.1 governance decision](docs/decisions/2026-07-28-adopt-trusted-governance-1.1.md).
The [comprehensive review implementation matrix](docs/comprehensive-review-implementation.md)
maps every material recommendation to executable capability and evidence.

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
├── constraints.md
├── critical-flows.md
├── gate-policy.yaml
├── baseline.yaml
├── risk-acceptances.yaml
├── evidence-providers.yaml
├── evidence/
├── rules/
└── reviews/
```

`profile.yaml` selects project qualities, reviews, and Rule Packs.
`constraints.md` records real limits. `critical-flows.md` defines protected
runtime behavior. Findings, decisions, and plans are stored under `reviews/`.
Organization rules can be versioned as Rule Packs under
`.architecture/rules/`; duplicate IDs cannot shadow bundled packs.

Validate a configuration:

```bash
python3 resources/scripts/architecture_tool.py validate-project /path/to/repository
python3 resources/scripts/architecture_tool.py validate-knowledge
```

## Trusted reviews and evidence

Schema `1.0` remains readable for migration and historical records. Only schema
`1.1` can enter deterministic enforcement. A trusted verified review binds:

- repository identity, Git commit, dirty-tree state, profile hash, and explicit
  scope manifest;
- exact Rule Pack versions and SHA-256 hashes;
- a source candidate review and its SHA-256;
- complete coverage for every loaded rule;
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

Solution decisions must reference a trusted review by ID and SHA-256. Schema
`1.1` decisions compare at least three options, including keep-current, bind an
exact knowledge snapshot, and score quality, business, team, evolution,
maturity, lock-in, and complexity trade-offs. Generate their hashes first:

```bash
python3 resources/scripts/architecture_tool.py decision-bindings \
  --project . --review verified.yaml
python3 resources/scripts/architecture_tool.py validate-decision \
  decision.yaml --review verified.yaml --project . --require-accepted
```

Plans bind the accepted decision and source review. A plan marked complete must
provide repository-relative, SHA-256-bound acceptance evidence for every
declared evidence type:

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
   decisions, dirty tree, signature policy, and evidence resolution;
4. `release`: required evidence, accepted decisions, decision authority, and
   complete remediation with hashed acceptance evidence.

Exit codes are stable: `0` passes, `1` is a policy failure, and `2` is invalid
input or configuration. SARIF 2.1.0 output can be uploaded with GitHub's
`github/codeql-action/upload-sarif`. The bundled GitHub workflow template also
publishes the Check summary and updates a pull-request comment.

## Behavior evaluation

`evals/cases.yaml` contains one direct, indirect, incomplete, negative, and
edge activation case for each of the nine Skills. `benchmarks/` adds ten
adversarial code fixtures with ground truth, forbidden over-design
recommendations, and metrics for precision, recall, severity agreement,
evidence validity, prohibited recommendations, repeated-trial stability,
duration, and optional token/cost usage.

The forward-test runner accepts a caller-supplied agent command:

```bash
python3 scripts/run_behavior_benchmark.py \
  --model MODEL --surface SURFACE --repetitions 3 \
  --output benchmark-run.yaml -- \
  agent-command --skill '{skill}' --repo '{fixture}' --prompt '{prompt}'
python3 resources/scripts/architecture_tool.py benchmark-score \
  --ground-truth benchmarks/ground-truth.yaml --run benchmark-run.yaml
```

No public model score is claimed until an identified model and surface have
actually run the corpus. See [evaluation guidance](docs/evaluation.md).

## Open-source verification

Run the local gate:

```bash
python3 scripts/validate_repository.py
python3 resources/scripts/architecture_tool.py validate-project .
python3 resources/scripts/architecture_tool.py validate-knowledge
python3 -m pytest
python3 -m ruff check .
python3 -m ruff format --check .
python3 scripts/audit_licenses.py
python3 scripts/package_plugin.py --output-dir dist
python3 scripts/verify_checksum.py dist/*.zip.sha256
python3 scripts/generate_sbom.py \
  --archive dist/codex-architecture-governance-0.2.0.zip \
  --output dist/codex-architecture-governance-0.2.0.spdx.json
```

CI runs the supported Python boundary on Linux, macOS, and Windows. Tagged
releases rebuild the deterministic ZIP, attach its checksum and SPDX SBOM, and
create GitHub provenance plus SBOM attestations. See
[release verification](docs/releasing.md), [compatibility](docs/compatibility.md),
and the [assurance model](docs/assurance-model.md). A scheduled workflow checks
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
