# Skill evaluation

The evaluation strategy separates static repository contracts from behavioral
Codex forward tests.

## Static gate

`python3 scripts/validate_repository.py` verifies:

- plugin identity and Semantic Versioning;
- the exact eight public Skill names;
- frontmatter, folder naming, descriptions, line budgets, and UI metadata;
- local Markdown links;
- JSON Schema validity and parseable YAML templates;
- one direct, indirect, incomplete, negative, and edge case per Skill;
- parseable routing, knowledge-selection, decision-quality, false-positive,
  and artifact-validity corpora;
- absence of placeholders and symlinks from runtime directories; packaging
  excludes caches and development artifacts.

Static validation proves structure and coverage. It does not prove that a model
will select the right Skill or produce a high-quality review.

## Behavioral forward tests

Use `evals/cases.yaml` as the source corpus.

The 0.3 evaluation sets have separate responsibilities:

| Corpus | Proves |
| --- | --- |
| `routing.yaml` | Exact public Skill activation and negative boundaries |
| `knowledge-selection.yaml` | Relevant inclusion, important exclusion, reasons, and budget |
| `decision-quality.yaml` | Quality-first comparison and prohibited shortcuts |
| `false-positive.yaml` | Leads are not promoted without an invariant and failure path |
| `artifact-validity.yaml` | Hash, fingerprint, coverage, and migration tampering fails |

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

Fixture directory names, titles, and content must remain outcome-neutral.
Repository tests reject phrases such as `Expected behavior`, `Expected
decision`, and `do not recommend` inside model-visible fixtures. Case IDs may
remain descriptive in the hidden ground-truth artifact because the runner
never places those IDs in the model command.

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
over-design recommendations. Solution Advisor cases also record the expected
option, required trade-offs and knowledge, over-design options, rejected-option
depth, and migration-slice depth. A run must use the same case IDs and record
the model, Codex surface, Skill version, and run time. Score it with:

```bash
python3 resources/scripts/architecture_tool.py benchmark-score \
  --ground-truth benchmarks/ground-truth.yaml \
  --run benchmark-run.yaml \
  --output benchmark-score.json
```

Metrics are:

- Finding precision and recall by rule ID;
- severity agreement on true positives;
- evidence validity recomputed from fixture-contained file/line/excerpt
  references;
- hits on fixture-specific forbidden recommendations;
- finding and severity stability across repeated independent trials;
- recommendation accuracy and selected-option stability;
- over-design rate and required trade-off coverage;
- validity and relevance of cited knowledge IDs;
- rejected-option explanation coverage and migration actionability;
- mean duration and optional token/cost usage.

The score reports `usage_trials` and uses JSON `null` for token and cost totals
when the model surface supplied no usage metadata; missing telemetry is never
represented as zero consumption.

An empty run has zero precision when expected positives exist. It is not a
successful baseline. `benchmarks/run-template.yaml` only proves schema and
scorer operation; it is not a model result.

The harness remains command-agnostic. A bundled adapter invokes Codex in a
read-only fixture with a strict observation schema:

```bash
python3 scripts/run_behavior_benchmark.py \
  --model MODEL --surface SURFACE --repetitions 3 \
  --output benchmark-run.yaml -- \
  python3 scripts/codex_benchmark_adapter.py \
    --model MODEL --skill '{skill}' \
    --fixture '{fixture}' --prompt '{prompt}'
```

The command must emit JSON with `observed_findings` and
`observed_recommendations`; Solution Advisor cases also require
`observed_decision`. Every observed Finding supplies repository-relative
`path`, `line_start`, `line_end`, and exact `excerpt` evidence. The harness and
scorer independently resolve these references inside the fixture; a
caller-supplied validity assertion is not trusted. Use a clean task per case
and never include the ground-truth expectations in the model prompt. Each
repetition launches a new command process; the harness records every trial
rather than averaging model output before scoring. For schema 1.3 runs it also
writes a sibling JSONL execution log and binds its hash to the result. Each
trial records hashes of the rendered command, stdout, stderr, normalized
observation, and exact log record. Run-level provenance binds the clean source
commit, execution environment, dependency lock, schemas, Ground Truth,
Knowledge manifest, fixture trees, and runner/adapter bytes.

The bundled Codex adapter constrains Finding IDs to the bundled machine Rule
Packs and solution trade-offs to a documented atomic vocabulary. It performs
at most one evidence-only correction call when the first response contains an
escaped path, non-contiguous excerpt, or non-verbatim line citation. The
correction receives the prior response and deterministic validation errors,
never ground truth or expected findings. A second invalid response fails the
trial instead of being repaired or scored as valid.

For release evidence, run at least two identified models with three fresh
trials per case. Preserve each run YAML, sibling `*.log.jsonl`, and score JSON.
The scorer resolves every provenance hash against the recorded source commit
and rejects dirty relevant inputs. A failed or interrupted run leaves a
hash-only execution-log record and must not be rewritten as a passing model
result.

## Release evidence

A release may state behavioral results only when the run artifact is preserved
with an identified model/surface and the exact plugin version. Until then, the
repository claims corpus and harness coverage, not model quality.

A deterministic release report may cover repository contracts, selector cases,
and artifact tamper tests without claiming model behavior. A model-quality
report still requires an actual external run.

Version 0.4.0 satisfies that evidence condition with two models, three trials
per case, preserved run/score artifacts, and an explicit limitations section
in `benchmarks/reports/0.4.0-model-behavior.md`.
