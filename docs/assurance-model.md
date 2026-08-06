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
| A serious risk is accepted or released with only shallow verification. | Policy selects the highest of the global, severity, accepted-risk, and release floors; the bundled profile uses critical V3, high V2, medium/low V1, and V4 for acceptance/release. | A dishonest or underqualified authorized verifier can still approve weak evidence. |
| A verified review is detached from its candidate. | Candidate ID, SHA-256, and explicit repository snapshot are bound at Review and Finding level; Review 1.2 requires candidate and verified snapshots to match. | A malicious verifier can approve a malicious candidate. |
| Evidence changes after review. | Current evidence must match the Review commit; older evidence is accepted only when explicitly classified historical. Git path, blob, symbol, optional line/excerpt hashes, and exact/ancestor/diff-aware freshness are checked. | Runtime/document providers require their own trustworthy retention. |
| A path escapes the audited repository. | Configured paths, review paths, source candidates, and evidence reject absolute or parent traversal outside the root. | Symlink and provider-specific behavior still requires platform review. |
| A rule is silently skipped or merely self-declared assessed. | Trusted reviews require exactly one coverage row for every loaded Rule Pack rule, and every current `assessed` rule and critical flow binds Git-resolvable evidence at the Review commit. | Evidence can still be misinterpreted by an auditor. |
| An old waiver suppresses a changed issue. | Semantic Finding fingerprints bind baselines, waivers, and risk acceptance. | Fingerprint inputs deliberately exclude narrative fields and may need versioning later. |
| One person silently accepts risk or verifies their own audit. | Separate registry, role allowlists, required auditor/verifier and accepter/approver separation, controls, and expiry. | Repository maintainers still control the role policy. |
| A high-assurance review is edited after approval. | V5 requires a detached SSH signature checked against a policy-owned allowed-signers file; the signature covers the exact review bytes. | Key custody and allowed-signers maintenance remain organizational responsibilities. |
| An unauthorized solution is treated as accepted. | Decisions bind source review hashes; release checks accepted status and decision-maker role. | Repository maintainers control policy and can change role allowlists. |
| A decision cites generic architectural fashion. | Decision artifacts bind exact selected Markdown entry hashes and compare keep-current plus alternatives across quality scenarios, business/team/evolution fit, complexity, maturity, and lock-in. | Knowledge is guidance; local evidence and accountable judgment still decide. |
| A constrained input is mistaken for proof. | Brief 1.1 records required, preferred, and prohibited constraints; the Advisor challenges required conflicts, permits preferred loss, hard-eliminates prohibited options, and binds each satisfied assessment to the Brief Knowledge ID and concrete target IDs. | An authorized owner can still provide a wrong or stale constraint. |
| A copied template or status string impersonates approval. | The distributed Brief is `draft`; `approved` requires policy-authorized identities, repository-contained SHA-256 evidence, and one detached SSH signature per approver over the exact Brief. | Maintainers still control the allowed-signers policy and can authorize weak signers or evidence. |
| A target architecture omits the boundaries needed to operate it. | Decision 1.4 requires runtime/deployment units, data ownership, interfaces, trust boundaries, critical flows, operations, constraint assessments when present, and Knowledge bindings in both open and constrained modes. | A complete artifact can still describe a poor design. |
| A new-system decision fabricates findings to satisfy the remediation contract. | Greenfield decisions bind a validated Design Brief; their Finding list is empty. Greenfield Plan 1.3 binds Brief/Decision directly and also forbids fake Finding bindings. | The Design Brief can still contain mistaken owner assertions. |
| Repository detection is mistaken for suitability. | The inspector schema contains facts and evidence paths only; Profile inference and Review conclusions are separate artifacts. | A correct fact can still be overinterpreted by an auditor. |
| Irrelevant knowledge overwhelms the task. | Selection binds repository facts, canonical Profile domains, task, Skill, entry hashes, priority, context budget, bounded relation expansion, inclusion reasons, and exclusions. | Trigger quality and an explicit include can still select weak context. |
| A legacy verified label is promoted during migration. | The migration command always emits candidates and records verification and critical-flow unknowns. | A later verifier can still make an unsound decision. |
| An external tool exits successfully with malformed, substituted, or cache-dependent output. | Evidence Providers are opt-in, shell-free, timeout-bounded, executable/configuration/dependency-closure-hashed, cache-isolated, output-captured, and structurally validate JSON, SARIF, or JUnit before a deterministic run can pass. | A declared dependency closure can be incomplete, the external tool can be flawed, and textual providers remain lower assurance. |
| A remediation is marked complete without proving acceptance. | Complete plans require every declared evidence type to be represented by a repository-relative file and SHA-256, optionally bound to a validated provider run. | Evidence can prove the declared test passed without proving that the acceptance criterion was sufficient. |
| Stale framework knowledge drives a decision. | Official source URLs, review dates, freshness windows, curator workflow, and release validation; technology-evolution remains an explicit lens and never supplies version pins from memory. | Fast-changing pricing, advisories, and versions must be checked at use time. |
| A release includes undeclared or incompatible dependencies. | Exact hashed locks, license allow/deny audit, SPDX packages with declared licenses, deterministic ZIP/SHA-256, and GitHub provenance/SBOM attestations. | Attestation proves build origin, not absence of malicious source or workflow. |
| Benchmark expectations leak into evaluation or one lucky trial is reported. | Clean tasks, read-only structured adapter, separate ground truth/run files, explicit model/surface metadata, independent evidence resolution, decision-quality metrics, and repeated-trial stability. | Public fixtures can be overfit; private or rotated suites may still be needed. |

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
