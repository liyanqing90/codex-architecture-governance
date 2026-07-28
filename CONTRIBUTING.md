# Contributing

Thank you for improving Codex Architecture Governance.

## Before opening a change

Use an issue for a new workflow, schema-breaking change, or policy behavior
change. Small documentation, test, and correctness improvements may go directly
to a pull request.

Keep each change tied to one observable outcome. Separate:

- Skill activation or instruction changes;
- artifact schema or CLI contract changes;
- policy and quality-gate changes;
- repository-only documentation or automation.

## Development setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements-dev.txt
```

Windows PowerShell users can activate with:

```powershell
.venv\Scripts\Activate.ps1
```

## Making a Skill change

Every Skill must:

1. own one recognizable user goal;
2. keep only `name` and `description` in YAML frontmatter;
3. state trigger conditions and boundaries in the description;
4. use imperative instructions with explicit inputs and outputs;
5. point directly to every supporting reference it requires;
6. stay below 500 lines;
7. avoid repository README, changelog, or setup documents inside the Skill;
8. include deterministic scripts only when instructions alone are unreliable;
9. preserve rejected hypotheses and evidence limitations;
10. update direct, indirect, incomplete, negative, and edge cases in
    `evals/cases.yaml`.

When adding a Skill, generate `agents/openai.yaml` with the Codex
`skill-creator` helper and ensure `default_prompt` explicitly mentions the
Skill as `$skill-name`.

## Changing schemas or the CLI

- Treat artifact schemas and CLI exit codes as public contracts.
- Prefer additive, backward-compatible changes.
- Update templates, tests, documentation, and changelog in the same pull
  request.
- Add a migration note before intentionally rejecting a previously valid
  artifact.
- Never weaken verification state, baseline, or waiver integrity to obtain a
  passing gate.

## Required checks

Run:

```bash
python3 scripts/validate_repository.py
python3 resources/scripts/architecture_tool.py validate-project .
python3 -m pytest
python3 -m ruff check .
python3 -m ruff format --check .
python3 scripts/package_plugin.py --output-dir dist
```

The pull request should explain what each new test proves. A generated archive
is local evidence and should not be committed.

## Pull request expectations

Include:

- the user-visible outcome;
- the affected Skill, schema, or policy boundary;
- compatibility implications;
- exact commands and observed results;
- activation cases added or changed;
- remaining limitations.

Do not include secrets, personal data, proprietary review artifacts, generated
caches, or unrelated formatting.

By contributing, you agree that your contribution is licensed under this
project's MIT License.
