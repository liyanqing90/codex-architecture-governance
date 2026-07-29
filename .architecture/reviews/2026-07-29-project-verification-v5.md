# Independent verification

- Candidate: `codex-architecture-governance-20260729-project-candidates-v4`
- Candidate SHA-256: `1df40ae7669d74e89af54348ef0122da2001e09618d5e761efeeb411d167560f` — matched
- Reviewed source commit: `a290c4632a0974c087fd2dd578238e38a5004e13` — exists
- Current commit: `d65aabb65bc9af96acf56961aa36a429dd22c365`
- Independence: fresh different-model/session verification; prior verification Markdown was not used as evidence
- Candidate validation: passed
- Evidence resolution: passed with no unresolved references
- Binding hashes for Profile, Rule Packs, repository facts, knowledge selection, and both findings matched
- Source/test blobs cited at `a290c46` match current source; no post-review changes touched the inspected implementation or tests
- Honest verification level: **V2**

## CAG-EVIDENCE-001 — confirmed, V2

**Direct evidence:** Both Terra and Sol scored successfully in archived mode
using artifact commit `b6d406a324f294bf29deaf7b3280e8ae7ab22e4c`.
Each result bound the exact run YAML and JSONL Git blobs, validated 30 log
records, and reported `current_host_match: false` because the current Codex
runtime version differs. Source inspection confirms validation of source
inputs, tools, fixture trees, command templates, exact per-trial argv, log
hashes, exit/stdout/stderr hashes, and complete observations before scoring.

Default strict mode rejected both runs with
`Benchmark runtime version mismatch: model-runtime-1`. Archived mode without
`--artifact-commit` failed with
`Archived runtime verification requires --artifact-commit`.

**Strongest counter-evidence:** Archived verification proves integrity and
reconstructibility of locally controlled inputs and preserved outputs, not the
identity of the remote model build or deterministic reproduction of its
responses. Token and cost telemetry remain unavailable; required-knowledge
coverage remains 0.792 for Terra and 0.625 for Sol.

**Residual limitations:** No remote-model build visibility,
deterministic-output guarantee, current-host runtime match, observed
clean-machine installation, or observed hosted-CI execution.

## CAG-GATE-001 — confirmed, V2

**Direct evidence:** The gate classifies the base range but separately diffs
the reviewed commit against current `HEAD` for critical and security-sensitive
paths. A matching post-review sensitive path produces the explicit
stale-review failure. Compatible migration bypass requires an accepted,
authorized `keep-current` decision whose affected paths cover every classified
migration path and whose slices, validation, and rollback are nonempty.
Otherwise an active remediation plan is required.

Direct regression cases cover:

- governance-only commits after review passing, followed by a post-review
  critical-path change failing;
- an incorrect migration `affected_paths` value failing;
- a non-`keep-current` selection without an active plan failing.

The cited implementation and regression-test blobs at `a290c46` exactly match
current files.

**Strongest counter-evidence:** Enforcement remains only as complete as the
repository’s configured critical, security, and migration path patterns. The
focused tests could not be re-executed because the read-only runtime has no
writable temporary directory; their assertions and production paths were
inspected directly.

**Residual limitations:** Misclassified or omitted policy paths can escape
these controls. Current whole-project validation was also blocked during the
isolated run by the then-unfinalized architecture decision’s stale
knowledge-selection hash.

## Overall verdict

**Confirmed: 2 · Rejected: 0 · Needs evidence: 0.**

Both candidate strengths survive independent verification at **V2**. The
evidence supports tamper-evident portable benchmark scoring and the claimed
gate behavior, within the stated local-runtime, policy-classification, and
non-deterministic remote-model limitations.
