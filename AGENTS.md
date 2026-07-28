# Repository guidance

## Purpose

Maintain a distributable Codex plugin containing focused architecture-governance Skills and deterministic artifact tooling.

## Layout

- `.codex-plugin/plugin.json`: installable plugin manifest.
- `.architecture/`: this repository's own architecture profile and policy.
- `skills/<skill-name>/`: one user goal per Skill.
- `resources/`: runtime contracts, schemas, knowledge, rules, evidence providers, templates, and the portable CLI used by the Skills.
- `evals/cases.yaml`: activation and boundary cases for every Skill.
- `benchmarks/`: adversarial architecture fixtures and behavioral ground truth.
- `scripts/`: repository validation and deterministic packaging.
- `tests/`: executable behavior and repository-contract tests.

## Working agreements

- Preserve every Skill's public name and artifact schema unless a breaking change is explicitly requested.
- Keep `SKILL.md` frontmatter to `name` and `description`; put trigger conditions in the description.
- Write Skill procedures in imperative form. Keep each `SKILL.md` under 500 lines.
- Put reusable detail in `references/`, deterministic work in `scripts/`, and output material in `assets/`.
- Keep repository documentation outside Skill directories.
- Add or update direct, indirect, incomplete, negative, and edge eval cases when Skill activation or boundaries change.
- Do not weaken schemas, verification states, baselines, waivers, or quality-gate policy to make checks pass.
- Preserve the PAAD attribution in `NOTICE` and `third_party/PAAD-MIT.txt`.

## Verification

Install development dependencies:

```bash
python3 -m pip install --require-hashes -r requirements-dev.lock
```

Run the full local gate:

```bash
python3 scripts/validate_repository.py
python3 resources/scripts/architecture_tool.py validate-project .
python3 resources/scripts/architecture_tool.py validate-knowledge
python3 -m pytest
python3 -m ruff check .
python3 -m ruff format --check .
python3 -m pip_audit -r requirements-runtime.lock
python3 scripts/audit_licenses.py
python3 scripts/package_plugin.py --output-dir dist
python3 scripts/verify_checksum.py dist/*.zip.sha256
python3 scripts/generate_sbom.py \
  --archive dist/codex-architecture-governance-0.2.0.zip \
  --output dist/codex-architecture-governance-0.2.0.spdx.json
```

## Code review rules

- Flag a finding or quality gate that can be produced from unverified model output or incomplete Rule Pack coverage.
- Flag trusted artifacts whose identity, profile, rule, candidate, decision, or fingerprint hashes are not validated.
- Flag Evidence Provider execution that invokes a shell, escapes the project,
  omits executable/config/output hashes, or treats malformed structured output
  as passing.
- Flag accepted risk without separate authorized accepter and approver identities.
- Flag a Skill description that overlaps another Skill without a distinct user goal.
- Flag scripts that can overwrite an existing `.architecture` or `.architecture-portfolio` directory.
- Flag review artifacts whose counts, finding references, verification state, or policy outcome are not schema-validated.
- Flag release archives containing caches, tests, development configuration, or files outside the runtime allowlist.
