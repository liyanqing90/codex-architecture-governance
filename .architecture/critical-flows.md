# Critical flows

## Plugin discovery and Skill execution

- Trigger: a user installs the plugin and requests an architecture workflow.
- Actor: Codex or ChatGPT with the installed plugin enabled.
- Preconditions: the manifest, selected Skill, and referenced resources exist.
- Control/data path: manifest → Skill routing metadata → `SKILL.md` → explicit
  references, templates, schemas, and optional local CLI.
- Authoritative owner: `.codex-plugin/plugin.json` for bundle identity; each
  Skill for its workflow; `resources/` for shared contracts.
- Side effects: none unless the user requests review artifacts or initialization.
- Failure and recovery behavior: fail visibly on missing resources or invalid
  artifacts; reinstall a validated package after correcting the source.
- Idempotency boundary: reading and audit routing are repeatable; initialization
  refuses an existing target.
- Security/privacy boundary: repository evidence remains local and must be
  redacted in published reports.
- Observability evidence: plugin validator, Skill validators, and evaluation
  case records.
- Acceptance tests: official validators pass and all bundled paths exist in the
  release ZIP.

## Finding verification and policy enforcement

- Trigger: an audit creates candidate findings and a user requests verification
  or gate evaluation.
- Actor: audit Skill, independent verifier, and deterministic CLI.
- Preconditions: evidence is current enough to inspect and artifacts match
  their schemas.
- Control/data path: candidate review → counter-hypothesis and evidence check →
  verified review → repository policy, baseline, and waiver evaluation.
- Authoritative owner: verifier for finding status; repository policy owner for
  blocking thresholds and explicit risk acceptance.
- Side effects: verified artifacts may be written; the gate only reports and
  exits.
- Failure and recovery behavior: invalid, stale, or candidate-only input fails
  validation or remains non-blocking according to explicit policy.
- Idempotency boundary: identical valid inputs and evaluation date produce the
  same gate result.
- Security/privacy boundary: unverified model output never becomes enforcement.
- Observability evidence: stable exit codes, JSON output, finding IDs, and test
  assertions.
- Acceptance tests: confirmed findings block according to policy; rejected,
  baselined, waived, expired, and needs-evidence paths remain distinct.

## Safe project initialization

- Trigger: a user explicitly requests project or portfolio governance setup.
- Actor: `architecture_tool.py`.
- Preconditions: the target root exists and the destination configuration does
  not.
- Control/data path: arguments → staged temporary directory → schema validation
  → atomic rename to the requested destination.
- Authoritative owner: the target repository or portfolio.
- Side effects: creates one configuration tree and no external resources.
- Failure and recovery behavior: validation failure removes staging; an existing
  destination is never overwritten.
- Idempotency boundary: the first valid call creates state; every repeated call
  fails without mutation.
- Security/privacy boundary: only the explicit local root is in scope.
- Observability evidence: command output, exit code, and created files.
- Acceptance tests: project and portfolio initialization, validation, and
  overwrite refusal tests pass.

## Deterministic release packaging

- Trigger: a maintainer or CI builds versioned release assets.
- Actor: `scripts/package_plugin.py`.
- Preconditions: repository contracts pass and all runtime allowlist files exist.
- Control/data path: manifest identity → sorted runtime allowlist → fixed ZIP
  metadata → versioned archive → SHA-256 checksum.
- Authoritative owner: plugin manifest version and packaging script.
- Side effects: replaces generated assets only in the explicit output directory.
- Failure and recovery behavior: missing files, symlinks, or runtime cache
  artifacts stop packaging before publication.
- Idempotency boundary: identical source bytes produce identical archive bytes.
- Security/privacy boundary: tests, evals, caches, repository guidance, and
  private review artifacts are excluded.
- Observability evidence: archive inventory, checksum, CI logs, and release tag.
- Acceptance tests: two independent builds compare byte-for-byte and the
  checksum verifies from inside the output directory.
