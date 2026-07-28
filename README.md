# Codex Architecture Governance

An installable Codex plugin for evidence-backed architecture governance across
one repository, specialized AI and mobile boundaries, and an entire project
portfolio.

The project separates probabilistic diagnosis from deterministic enforcement:

```text
audit candidates
→ independent verification
→ confirmed findings
→ remediation plan
→ policy-controlled quality gate
```

Model output never blocks a build by itself. Only schema-valid, verified
findings can enter the deterministic quality gate.

## Included Skills

| Skill | Purpose |
| --- | --- |
| `project-architecture-audit` | Audit one repository against its actual profile, constraints, critical flows, and executable evidence. |
| `ai-agent-architecture-audit` | Review model, context, Memory, retrieval, MCP tools, prompt-injection, evaluation, approval, cost, and recovery boundaries. |
| `mobile-architecture-audit` | Review local state, sync, migrations, background work, notifications, privacy, and mobile lifecycle behavior. |
| `portfolio-architecture-audit` | Review duplication, stack sprawl, shared capabilities, dependencies, data flows, and hidden coupling across registered projects. |
| `architecture-finding-verifier` | Challenge every candidate, reject heuristics and false positives, and preserve the verification trail. |
| `architecture-remediation-planner` | Turn confirmed findings into options, dependencies, migration slices, rollback conditions, and acceptance criteria. |
| `architecture-quality-gate` | Apply deterministic severity, confidence, freshness, baseline, and waiver policy to verified reviews. |

## Why this structure

Codex Skills should remain focused and progressively disclosed. Repository
documentation, tests, contribution policy, and release automation therefore
live outside `skills/`. The installable plugin points at the seven Skill
directories, while `resources/` provides their schemas, templates,
references, and portable CLI.

See the accepted [repository layout decision](docs/decisions/2026-07-28-adopt-plugin-skill-repository-layout.md).
The repository also dogfoods its own project Profile under `.architecture/`;
no generated review is committed without a real evidence-backed audit.

## Runtime requirements

The Skill instructions are plain Markdown. The deterministic initializer,
schema validator, and quality gate require Python 3.11–3.13, PyYAML, and
jsonschema. Plugin installation does not modify the host Python environment;
install `requirements.txt` in the Python environment Codex will use before
running the helper:

```bash
python3 -m pip install -r /path/to/plugin/requirements.txt
```

Runtime execution needs no network, credentials, or external service.

## Quick start

Create a development environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements-dev.txt
```

Run the complete repository gate:

```bash
python3 scripts/validate_repository.py
python3 resources/scripts/architecture_tool.py validate-project .
python3 -m pytest
python3 -m ruff check .
python3 -m ruff format --check .
```

Build a deterministic plugin archive:

```bash
python3 scripts/package_plugin.py --output-dir dist
```

The command writes a versioned ZIP and a SHA-256 checksum. It packages only
runtime files: the plugin manifest, Skills, shared resources, dependency
manifest, licenses, and attribution.

## Use during local development

Test the complete bundle through a local Codex marketplace so paths resolve
exactly as they do after installation. Put this plugin under the marketplace
root's `plugins/` directory and add an entry like:

```json
{
  "name": "codex-architecture-governance",
  "source": {
    "source": "local",
    "path": "./plugins/codex-architecture-governance"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Developer Tools"
}
```

Place that object in the `plugins` array of
`~/.agents/plugins/marketplace.json`, restart Codex, install the plugin from
the personal marketplace, and test it in a new task. The marketplace path is
resolved from its marketplace root.

For public or team distribution, publish the repository as a Codex plugin or
place the packaged plugin in a governed marketplace. Do not copy repository
development files into a Skill folder.

## Initialize project governance

Invoke the project audit Skill or run its deterministic helper:

```bash
python3 resources/scripts/architecture_tool.py init-project \
  --repo /path/to/repository \
  --name "Example Project" \
  --type service \
  --quality recoverability \
  --review project-architecture
```

This creates:

```text
.architecture/
├── profile.yaml
├── constraints.md
├── critical-flows.md
├── gate-policy.yaml
├── baseline.yaml
└── reviews/
```

The initializer refuses to overwrite an existing `.architecture/` directory.

Validate configuration and reviews:

```bash
python3 resources/scripts/architecture_tool.py validate-project /path/to/repository
```

Run a deterministic gate only after verification:

```bash
python3 resources/scripts/architecture_tool.py gate \
  --project /path/to/repository \
  --review /path/to/project-verified.yaml
```

Exit codes are stable:

- `0`: policy passes;
- `1`: verified findings or freshness policy block;
- `2`: input or configuration is invalid.

## Design guarantees

- Findings require a violated or protected invariant, a complete evidence path,
  an owning boundary, impact, counter-evidence, severity, and confidence.
- File size, imports, directory names, singletons, frameworks, or database
  choices are never sufficient evidence.
- Candidate reviews cannot enter a verified bundle.
- Rejected and needs-evidence findings remain machine-readable for traceability.
- Waivers require a reason, owner, and expiry.
- Initialization is staged and refuses destructive overwrite.
- Portfolio scope is explicit; the tooling never silently discovers unrelated
  repositories.

## Evaluation

`evals/cases.yaml` contains direct, indirect, incomplete, negative, and edge
prompts for every Skill. Static validation checks coverage and metadata;
behavioral forward tests should run in clean Codex tasks without leaking the
expected answer. See [evaluation guidance](docs/evaluation.md).

## Contributing and security

- Read [CONTRIBUTING.md](CONTRIBUTING.md) before changing a Skill or schema.
- Report vulnerabilities using [SECURITY.md](SECURITY.md), not a public issue.
- Community participation follows [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- Support boundaries are documented in [SUPPORT.md](SUPPORT.md).

## License

The project is licensed under the [MIT License](LICENSE). PAAD-derived concepts
retain their original notice in [third_party/PAAD-MIT.txt](third_party/PAAD-MIT.txt)
and [NOTICE](NOTICE).
