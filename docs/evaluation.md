# Skill evaluation

The evaluation strategy separates static repository contracts from behavioral
Codex forward tests.

## Static gate

`python3 scripts/validate_repository.py` verifies:

- plugin identity and Semantic Versioning;
- the exact seven Skill names;
- frontmatter, folder naming, descriptions, line budgets, and UI metadata;
- local Markdown links;
- JSON Schema validity and parseable YAML templates;
- one direct, indirect, incomplete, negative, and edge case per Skill;
- absence of caches, placeholders, and development artifacts from runtime
  directories.

Static validation proves structure and coverage. It does not prove that a model
will select the right Skill or produce a high-quality review.

## Behavioral forward tests

Use `evals/cases.yaml` as the source corpus.

For each case:

1. start a clean Codex task;
2. provide only the Skill path and the case prompt;
3. do not reveal the expected activation or outcome;
4. use a disposable repository or read-only fixture;
5. capture the selected Skill, questions, artifacts, and validation results;
6. compare behavior with the case expectation;
7. classify failure as activation, instruction, tool, environment, or
   unsupported-scope failure.

Do not reuse artifacts between cases. A Skill that succeeds only after seeing
the expected answer has not passed a forward test.

## Acceptance

A release candidate should:

- activate on every direct and indirect case;
- ask or stop correctly on incomplete cases;
- avoid activation on negative cases;
- preserve evidence, scope, and non-inference boundaries on edge cases;
- produce machine-readable artifacts that pass the bundled validator.

Record model and Codex surface when publishing behavioral results. Treat them
as time-bound evidence, not a permanent guarantee.
