- Candidate: `codex-architecture-governance-20260729-project-candidates-v2`
- SHA-256: `3f53e3d1d6283c0da7bdd6c4f0a162f1db6d4624c0468cfae2c0b1a6ef093365`
- Commit: `676ff9daa6931ed87ce8bf2da4f0222f47da14ee`
- Verifier model/surface: GPT-5.6 / Codex, read-only inspection

## Verdict: confirmed

Rationale: `CAG-EVIDENCE-001` accurately describes a bounded, verifiable provenance chain. Schema 1.3 requires provenance and per-trial execution bindings; the runner records source, tracked inputs/tools/fixtures, environment, and log hash; the scorer resolves hashes from the recorded commit and fails on dirty, mismatched, incomplete, or inconsistent evidence.

Evidence:

- Reconstructed diff of the prior `5b2bb2…` bytes: exactly four `evidence[].repository` values change from `.` to `codex-architecture-governance`, plus the resulting fingerprints:
  - Finding: `1fe76e…48dcb` → `0ff733…6b229`
  - Evidence: `c98a2b…a3dc0` → `2062db…8e3e6`
- Reconstructed prior content hashes exactly to `5b2bb2b517bab9d5c06abe841e9caf33b2d8133bae52c1d7db918a118c8c4b9b`; the supplied artifact hashes as stated, and both new fingerprints recompute correctly.
- [`run_behavior_benchmark.py`](../../scripts/run_behavior_benchmark.py#L68) records the required provenance inputs and tracked cleanliness.
- [`architecture_tool.py`](../../resources/scripts/architecture_tool.py#L4085) validates commit-resolved input/tool/fixture hashes, log integrity, and every trial/log binding.
- [`test_behavior_benchmark.py`](../../tests/test_behavior_benchmark.py#L86) specifies failure on appended-log tampering.
- Both preserved score artifacts report valid provenance, 30 records, clean source commit `f06af37…`.

Counter-evidence: provenance does not establish model quality; required-knowledge coverage is 0.750 (Terra) and 0.625 (Sol), and token/cost telemetry is unavailable.

V0–V5 recommendation: **V2** — strong read-only source, schema, test, run/log, score, and hash evidence for this bounded strength.

Residual limitations: no repository code or tests were executed; no external CI or clean-machine claim is made.
