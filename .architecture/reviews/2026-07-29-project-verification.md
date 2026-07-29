## Verification record

- Candidate review: `codex-architecture-governance-20260729-project-candidates`
- SHA-256: `1b87e04ac957a3702c190bea77a9f496f533cb7da8d7b4c71c4fc0c60e505e91`
- Reviewed commit: `4099c61341ed074997c8636c5e6870ee80b0777e`
- Models/surface: `gpt-5.6-terra`, `gpt-5.6-sol` / `codex-cli-0.146.0-alpha.3.1`
- Finding: `CAG-EVIDENCE-001` (`TESTPLATFORM.EVIDENCE.001`)
- Verdict: **rejected**

Rationale: The adapter does enforce fixture-relative, readable, range-valid, verbatim evidence excerpts, and all three cited path/line/blob/excerpt bindings match the reviewed commit. However, the claimed invariant is materially broader: the preserved runs do not bind code commit/hash, environment, dependencies, configuration, artifacts, logs, or the runner/adapter identity. The run schema permits only model, surface, Skill version, time, repetitions, cases, and trial observations. Nothing commit-binds the recorded runs to the adapter that provides the stronger validation. The strength is therefore overstated rather than fully demonstrated.

Evidence checked:

- `scripts/codex_benchmark_adapter.py:113–138`, blob `36ee632…`; its excerpt hash matches and the function performs the stated source-resolution checks.
- `tests/test_behavior_benchmark.py:68–111`, blob `6dc5a8f…`; its excerpt hash matches, but it tests the separate benchmark runner’s `evidence_is_valid`, not the cited adapter. It scans fixture content for limited leakage phrases.
- `benchmarks/results/gpt-5.6-terra.yaml:1–10`, blob `f670c9b…`; its excerpt hash matches and records model, surface, Skill version, timestamp, and three repetitions.
- `benchmarks/results/gpt-5.6-sol.yaml`, blob `af0a866…`, and `benchmarks/reports/0.4.0-model-behavior.md`, blob `7fc9a53…`; both preserve ten cases with three trials and document 60 accepted trials.
- `resources/schemas/benchmark.schema.json` and `scripts/run_behavior_benchmark.py:113–234`; these demonstrate the missing provenance fields and that stored `evidence_valid` is produced by the runner rather than cryptographically bound evidence.

Counter-evidence: The report’s claim that validation resolved excerpts is documentation, not provenance carried by the result artifacts. The report also records incomplete required-knowledge coverage (`0.708`) and missing token/cost usage. External CI and clean-machine reproduction remain unavailable.

Verification level recommendation: **E3** — direct source and preserved-artifact inspection supports bounded excerpt validation, but not the candidate’s E4-level reproducibility/provenance claim.

Residual limitations: No execution was performed; all inspection was read-only against the specified Git commit. The candidate YAML itself is untracked at that commit, though its supplied SHA-256 matches the working-tree artifact.