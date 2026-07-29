## Verification record

- Candidate review: `codex-architecture-governance-20260729-project-candidates-v2`
- SHA-256: `5b2bb2b517bab9d5c06abe841e9caf33b2d8133bae52c1d7db918a118c8c4b9b`
- Reviewed commit: `676ff9daa6931ed87ce8bf2da4f0222f47da14ee`
- Verifier model/surface: GPT-5 / Codex
- Finding: `CAG-EVIDENCE-001` (`TESTPLATFORM.EVIDENCE.001`)
- Verdict: **confirmed**
- Verification level recommendation: **V2**

Rationale: The prior rejection correctly found that the earlier results lacked commit-bound provenance. At `676ff9d`, schema 1.3 requires provenance and per-trial execution bindings; the runner records source commit, relevant-input cleanliness, input/tool hashes, fixture manifests, environment, and an execution-log hash. The scorer resolves recorded inputs/tools/fixtures from the recorded commit, rejects dirty inputs, and verifies each log record and trial observation before returning provenance validity. This directly supports the stated bounded invariant.

Evidence checked:

- All cited source/test bindings match commit `676ff9d`: blobs and the four excerpt SHA-256 values match their stated excerpts.
- `benchmark.schema.json` requires provenance and execution bindings for schema-1.3 runs.
- `validate_benchmark_provenance` enforces commit-resolved input/tool/fixture hashes, clean inputs, run-local log hash/count, unique records, and trial-to-log observation bindings.
- The cited test’s tamper path appends to the log and requires scorer exit code `2` with an execution-log hash mismatch.
- Both preserved runs are schema 1.3, bind commit `f06af37f74d4079823abdda6ff10c3b1ae035b1c`, state `dirty: false`, include the required five input hashes and both tool hashes; all seven directly checked input/tool hashes match that commit.
- Terra and Sol each declare three repetitions over ten cases, 30 log records, and log hashes matching the preserved JSONL files and score artifacts. Both scores report provenance valid.

Counter-evidence: The candidate’s own limitations remain: token/cost telemetry is unavailable; model behavior is imperfect and does not follow from provenance validity. The report’s claims of external CI or independent clean-machine reproduction are not established and are not relied upon.

Residual limitations: This was a read-only source/artifact inspection; I did not execute the scorer, tests, or benchmark runner. No external CI or clean-machine evidence is claimed.