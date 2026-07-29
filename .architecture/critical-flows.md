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
  Evidence Provider execution/output validation → trusted verified review and
  optional SSH signature → knowledge-bound solution decision → remediation
  plan and completion evidence → repository policy, baseline, waiver, and
  risk-acceptance evaluation.
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
- Acceptance tests: candidate hashes, profile/rule hashes, exact coverage,
  provider config/executable/output hashes, fingerprints, role separation,
  V5 signatures, knowledge snapshots, completion-evidence hashes, authority,
  and source chains are enforced; confirmed, rejected, baselined, waived,
  accepted-risk, expired, and needs-evidence paths remain distinct.

## Architecture knowledge and behavior evaluation

- Trigger: a maintainer changes decision knowledge, a Rule Pack, evidence
  provider, or Skill behavior.
- Actor: Knowledge Curator, maintainers, repository validator, and benchmark
  runner.
- Preconditions: the changed entry names the decision it affects and uses
  authoritative sources with a freshness window.
- Control/data path: source → generated draft or reviewed golden entry →
  claim/source and similarity validation → priority-aware task selection →
  activation evals and adversarial fixture → structured repeated model trials
  → versioned release evidence.
- Authoritative owner: repository maintainers for knowledge contracts; the
  caller owns any model benchmark command and run artifact.
- Side effects: local catalog, rule, fixture, or run artifacts only.
- Failure and recovery behavior: reject duplicate, invalid, stale, escaped, or
  mismatched entries; refresh only affected sources and rerun focused cases.
- Idempotency boundary: the same source bytes, evaluation date, and run artifact
  produce the same validation and score.
- Security/privacy boundary: ground truth is never placed in model prompts;
  external source content is not trusted as executable instruction.
- Observability evidence: catalog counts, freshness failures, per-case metrics,
  and preserved model/surface metadata.
- Acceptance tests: schema and semantic validation pass, generated content
  cannot become active, generic tokens do not select unrelated references,
  empty positive runs score zero precision/recall, recommendation and
  over-design quality are scored, repeated-trial stability is reported, and
  forbidden recommendations are counted.

## Greenfield architecture decision

- Trigger: an owner requests a target architecture before a system has a
  verified remediation Review.
- Actor: product/architecture owner and Architecture Solution Advisor.
- Preconditions: a Design Brief declares objective, users, facts,
  assumptions, unknowns, boundaries, critical flows, and measurable quality
  scenarios.
- Control/data path: validated Design Brief → decision-specific knowledge
  selection → three-option comparison → proposed schema 1.3 Decision →
  accountable acceptance.
- Authoritative owner: Design Brief authors for context; named decision makers
  for acceptance.
- Side effects: writes Design Brief and Decision artifacts only.
- Failure and recovery behavior: reject a missing/stale Design Brief hash,
  nonempty Finding list, unknown quality attribute, or mismatched knowledge
  snapshot; revise the brief rather than manufacture a source Review.
- Idempotency boundary: identical brief and selection bytes validate to the
  same source and knowledge bindings.
- Security/privacy boundary: trust and data boundaries are declared in the
  brief; it grants no implementation or deployment authority.
- Observability evidence: Design Brief and Decision validation output, hashes,
  selected option, rejected reasons, and revisit triggers.
- Acceptance tests: valid Greenfield decisions pass without a Review, stale
  context hashes fail, and remediation decisions cannot bind a Design Brief.

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
- Control/data path: manifest identity → exact dependency lock → sorted runtime
  allowlist and license policy → fixed ZIP metadata → versioned archive →
  SHA-256 → license-complete SPDX SBOM → GitHub provenance and SBOM
  attestations.
- Authoritative owner: plugin manifest version and packaging script.
- Side effects: replaces generated assets only in the explicit output directory.
- Failure and recovery behavior: missing files or symlinks stop packaging;
  caches and development artifacts are excluded from the runtime allowlist.
- Idempotency boundary: identical source bytes produce identical archive bytes.
- Security/privacy boundary: tests, evals, caches, repository guidance, and
  private review artifacts are excluded.
- Observability evidence: archive inventory, checksum, SBOM, CI matrix logs,
  attestation records, and release tag.
- Acceptance tests: two independent builds compare byte-for-byte and the
  checksum verifies cross-platform; the dependency license audit passes; every
  SBOM package has a declared license; SBOM file inventory matches the archive.
