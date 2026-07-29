# Preserved model runs

This directory contains versioned, model-visible behavior evidence rather than
golden answers.

- `*.yaml` files preserve every structured trial, model, Codex surface, Skill
  version, duration, Finding, evidence reference, recommendation, and solution
  decision emitted by the benchmark runner.
- `*-score.json` files are deterministic projections produced by
  `architecture_tool.py benchmark-score` against
  `benchmarks/ground-truth.yaml`.

Do not hand-edit a run or score to improve a metric. Rerun the complete corpus
with a new output artifact when a model, Skill, adapter, fixture, schema, or
Ground Truth contract changes. Model-visible fixtures must remain
outcome-neutral.
