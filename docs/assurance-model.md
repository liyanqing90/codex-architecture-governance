# Assurance and threat model

The plugin separates probabilistic architecture reasoning from deterministic
contract enforcement. It raises the cost of tampering and unsupported claims;
it does not prove that the audited system is correct, secure, compliant, or
complete.

## Assets and trust boundaries

Protected assets are the meaning of a Finding, its evidence, review scope,
verification authority, architecture decision, remediation chain, policy,
suppressions, and release artifact.

Trust boundaries exist between:

- an audit model and an independent verifier;
- repository source and generated review artifacts;
- verifiers, decision makers, risk acceptors, and policy owners;
- mutable worktrees and immutable Git objects;
- curated knowledge and time-sensitive external facts;
- source releases, CI builders, and plugin consumers.

## Threats and controls

| Threat | Executable control | Residual risk |
| --- | --- | --- |
| A model invents or overstates a finding. | Candidate state cannot gate; verification records rationale, counter-evidence, V0–V5 level, identity, and run. | A verifier can still make a poor judgment. |
| A verified review is detached from its candidate. | Candidate ID and SHA-256 are bound at review and Finding level. | A malicious verifier can approve a malicious candidate. |
| Evidence changes after review. | Git commit, path, blob, symbol, optional line/excerpt hashes, and exact/ancestor/diff-aware freshness are checked. | Runtime/document providers require their own trustworthy retention. |
| A path escapes the audited repository. | Configured paths, review paths, source candidates, and evidence reject absolute or parent traversal outside the root. | Symlink and provider-specific behavior still requires platform review. |
| A rule is silently skipped. | Trusted reviews require exactly one coverage row for every loaded Rule Pack rule. | A rule can be marked not applicable with a dishonest rationale. |
| An old waiver suppresses a changed issue. | Semantic Finding fingerprints bind baselines, waivers, and risk acceptance. | Fingerprint inputs deliberately exclude narrative fields and may need versioning later. |
| One person silently accepts risk or verifies their own audit. | Separate registry, role allowlists, required auditor/verifier and accepter/approver separation, controls, and expiry. | Repository maintainers still control the role policy. |
| A high-assurance review is edited after approval. | V5 requires a detached SSH signature checked against a policy-owned allowed-signers file; the signature covers the exact review bytes. | Key custody and allowed-signers maintenance remain organizational responsibilities. |
| An unauthorized solution is treated as accepted. | Decisions bind source review hashes; release checks accepted status and decision-maker role. | Repository maintainers control policy and can change role allowlists. |
| A decision cites generic architectural fashion. | Decisions bind exact catalog hashes and compare keep-current plus alternatives across quality scenarios, business/team/evolution fit, complexity, maturity, and lock-in. | Catalog knowledge is guidance; local evidence and accountable judgment still decide. |
| An external tool exits successfully with malformed or substituted output. | Evidence Providers are opt-in, shell-free, timeout-bounded, executable/configuration-hashed, output-captured, and structurally validate JSON, SARIF, or JUnit before a run can pass. | The external tool can be flawed or malicious, and textual providers remain lower assurance. |
| A remediation is marked complete without proving acceptance. | Complete plans require every declared evidence type to be represented by a repository-relative file and SHA-256, optionally bound to a validated provider run. | Evidence can prove the declared test passed without proving that the acceptance criterion was sufficient. |
| Stale framework knowledge drives a decision. | Official source URLs, review dates, freshness windows, curator workflow, and release validation. | Fast-changing pricing, advisories, and versions must be checked at use time. |
| A release includes undeclared or incompatible dependencies. | Exact hashed locks, license allow/deny audit, SPDX packages with declared licenses, deterministic ZIP/SHA-256, and GitHub provenance/SBOM attestations. | Attestation proves build origin, not absence of malicious source or workflow. |
| Benchmark expectations leak into evaluation or one lucky trial is reported. | Clean tasks, caller-supplied runner, separate ground truth/run files, explicit model/surface metadata, independent evidence resolution, and repeated-trial stability metrics. | Public fixtures can be overfit; private or rotated suites may still be needed. |

## Deliberate non-claims

- `validate-project` proves contract consistency, not architecture quality.
- A gate pass means supplied trusted evidence satisfies repository policy.
- SARIF transport does not strengthen the evidence itself.
- Source links establish provenance, not automatic correctness.
- A zero-finding review is meaningful only with complete rules, scope, and
  explicit limitations.
- Evidence Providers are never run automatically; the project must explicitly
  enable and configure each external command.
- V0–V4 identity fields are policy assertions. Cryptographic artifact integrity
  is available at V5, but the project still owns human-to-key identity.
- A benchmark run template or empty run is not a model-quality result.

## Revisit triggers

Review this model when a remote identity authority or keyless signing replaces
the local allowed-signers model, providers gain network or credentials, the
runtime itself gains network access, schema fingerprints change, hosted
governance is introduced, or GitHub attestation semantics change.
