# Adopt trusted governance 1.1 and a separate solution/knowledge layer

- Status: accepted
- Date: 2026-07-28
- Owners: repository maintainers
- Scope: public artifact contracts, Skill boundaries, enforcement, and release assurance
- Supersedes: `2026-07-28-adopt-plugin-skill-repository-layout.md`
- Superseded by: none

## Context

The initial seven-Skill suite could diagnose, verify, plan, and gate
architecture Findings, but it did not provide a governed architecture solution
decision, reusable sourced knowledge, machine-complete rules, strong artifact
provenance, independent risk acceptance, or behavioral ground truth. A review
that only identifies deficiencies cannot justify a target architecture, and a
gate that trusts mutable IDs or partial coverage can enforce unsupported
claims.

## Evidence

| Claim | Kind | Source and environment | Observed | Reference | Freshness / redaction |
| --- | --- | --- | --- | --- | --- |
| The 0.1 schemas allow readable reviews without candidate/profile/rule hashes or exact coverage. | fact | repository schema inspection | 2026-07-28 | `resources/schemas/review.schema.json` history | Repository-owned; no sensitive data. |
| Finding IDs alone do not bind a suppression to evidence or semantics. | inference | gate and baseline contract analysis | 2026-07-28 | `resources/schemas/baseline.schema.json` history | Re-evaluate if fingerprint inputs change. |
| Solution selection and migration execution have different authorities and outputs. | decision-driving inference | Skill boundary review | 2026-07-28 | `resources/references/solution-decision-contract.md` | Stable until superseded. |
| Architecture product/framework capabilities change and require sourced freshness. | fact | official and maintainer documentation review | 2026-07-28 | `resources/knowledge/technology-profiles/catalog.yaml` | Entries carry their own review windows. |
| Release consumers can verify GitHub build and SBOM attestations. | fact | GitHub artifact-attestation documentation | 2026-07-28 | `docs/releasing.md` | Verify action version at release changes. |

## Decision

1. Expand the suite to nine focused Skills by adding Architecture Solution
   Advisor and Architecture Knowledge Curator.
2. Keep audit, verification, solution decision, remediation, and enforcement
   as separate authorities and artifacts.
3. Keep schema `1.0` readable, but require trusted schema `1.1` for
   deterministic enforcement.
4. Bind trusted reviews to repository/profile/rule/candidate identities and
   hashes, complete Rule Pack coverage, verifier/run metadata, verification
   level, and semantic Finding fingerprints.
5. Keep risk acceptance in a separate, expiring, two-party registry.
6. Require `1.1` remediation plans to consume an accepted solution decision.
7. Maintain sourced knowledge catalogs, Rule Packs, evidence-provider
   contracts, and adversarial behavior benchmarks as repository-owned assets.
8. Publish deterministic archives with exact dependency locks, SHA-256, SPDX
   SBOM, and GitHub provenance/SBOM attestations.
9. Execute providers only through explicit, shell-free, timeout-bounded project
   configuration and bind catalog, configuration, executable, Git state, and
   structurally validated output hashes into each run.
10. Require policy role separation, human V3–V5 verification, deterministic
    evidence at V4–V5, and detached SSH artifact signatures at V5.
11. Bind solution decisions to exact knowledge snapshots and completed plans to
    hashed acceptance evidence.

## Alternatives considered

- Add recommendation prose to the audit — rejected because diagnosis would
  silently own technology selection and decision authority.
- Let the remediation planner choose architecture — rejected because a plan
  should operationalize an accepted target, not create it.
- Gate schema `1.0` indefinitely — rejected because missing provenance and
  partial coverage cannot be made trustworthy without new evidence.
- Replace Finding IDs entirely with content hashes — rejected because stable
  human-readable identifiers remain useful; semantic fingerprints can coexist.
- Store current product versions as timeless rules — rejected because volatile
  facts would become stale and misleading.
- Automatically accept risk for baselined issues — rejected because debt
  inventory, waiver, and accountable risk acceptance have different meaning.

## Consequences

- Positive: missing capabilities are diagnosed and connected to a justified,
  accepted solution and migration path.
- Positive: deterministic enforcement has explicit provenance, scope,
  completeness, authority, freshness, and suppression semantics.
- Positive: architecture knowledge is reusable and independently maintainable.
- Positive: missing capabilities now have executable provider, decision, plan,
  and release-evidence paths rather than prose-only recommendations.
- Negative: schema `1.0` artifacts require deliberate migration before gating.
- Negative: contributors must update more linked contracts and tests when
  changing rules, fingerprints, decisions, or policy.
- Negative: provider tools, signing keys, and policy role identities remain
  repository/operator responsibilities.
- Operational: releases require dependency locks, multi-platform CI, SBOM,
  checksum, and attestation workflow evidence.

## Verification

- Validate every schema instance, Skill, plugin artifact, knowledge entry,
  Rule Pack, provider, and benchmark.
- Exercise positive and adversarial tests for provenance, paths, fingerprints,
  risk authority, source hashes, cumulative stages, benchmark scoring, SBOM,
  and deterministic packaging.
- Run the supported operating-system/Python CI matrix.
- Verify tagged release attestations with GitHub CLI before announcing a
  release.

## Revisit when

- a remote identity authority or keyless signer replaces SSH allowed signers;
- evidence providers require credentials, network, or an extension protocol
  beyond the bounded command adapter;
- fingerprint semantics require versioning;
- hosted governance or an MCP server becomes justified;
- Codex Plugin/Skill contracts or GitHub attestations materially change.
