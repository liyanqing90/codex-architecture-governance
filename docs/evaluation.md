# Skill evaluation

The evaluation strategy separates static repository contracts from behavioral
Codex forward tests.

## Static gate

`python3 scripts/validate_repository.py` verifies:

- plugin identity and Semantic Versioning;
- the exact nine Skill names;
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

## Adversarial architecture benchmark

`benchmarks/ground-truth.yaml` is a separate behavior corpus. Its ten fixtures
cover false-positive resistance, modular-monolith proportionality, real data
ownership conflicts, queue versus durable workflow proportionality, mobile
client/server ownership, documentation/code contradictions, shared-database
coupling, and injected tool authority.

The ground truth records expected rule IDs and severity plus forbidden
over-design recommendations. A run must use the same case IDs and record the
model, Codex surface, Skill version, and run time. Score it with:

```bash
python3 resources/scripts/architecture_tool.py benchmark-score \
  --ground-truth benchmarks/ground-truth.yaml \
  --run benchmark-run.yaml
```

Metrics are:

- Finding precision and recall by rule ID;
- severity agreement on true positives;
- evidence validity recomputed from fixture-contained file/line/excerpt
  references;
- hits on fixture-specific forbidden recommendations;
- finding and severity stability across repeated independent trials;
- mean duration and optional token/cost usage.

An empty run has zero precision when expected positives exist. It is not a
successful baseline. `benchmarks/run-template.yaml` only proves schema and
scorer operation; it is not a model result.

The caller-supplied harness deliberately does not embed a vendor command:

```bash
python3 scripts/run_behavior_benchmark.py \
  --model MODEL --surface SURFACE --repetitions 3 \
  --output benchmark-run.yaml -- \
  command --skill '{skill}' --repo '{fixture}' --prompt '{prompt}'
```

The command must emit JSON with `observed_findings` and
`observed_recommendations`. Every observed Finding supplies repository-relative
`path`, `line_start`, `line_end`, and exact `excerpt` evidence. The harness and
scorer independently resolve these references inside the fixture; a
caller-supplied validity assertion is not trusted. Use a clean task per case
and never include the ground-truth expectations in the model prompt. Each
repetition launches a new command process; the harness records every trial
rather than averaging model output before scoring.

## Release evidence

A release may state behavioral results only when the run artifact is preserved
with an identified model/surface and the exact plugin version. Until then, the
repository claims corpus and harness coverage, not model quality.
