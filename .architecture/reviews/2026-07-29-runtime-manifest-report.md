# Selector Runtime Manifest architecture review

## Review boundary

- Subject: Codex Architecture Governance
- Reviewed implementation commit:
  `53335fa7225ac2fba27c6a9b68892aeca7ea8ccf`
- Selector source anchor:
  `d48119c17576ce433dd81d7e61bccb366e8ecdc1`
- Scope: repository-wide correction of Selection provenance, historical trust,
  model-facing context, Profile relevance, and compatibility
- Candidate findings: 4
- Confirmed strengths: 4
- Confirmed risks: 0
- Rejected or needs-evidence findings: 0

The reviewed design keeps the local-first Codex plugin as the ownership
boundary. It adds a source-anchored Selector Runtime Manifest for machine
governance and a selected-only Context projection for model input. The reviewed
project commit and the plugin Selector commit are separate identities.

## Root causes corrected

1. Selection 1.3 hashed only the top-level Selector file and overloaded the
   reviewed project commit as Selector provenance. Selection 1.4 binds eleven
   exact runtime inputs, the plugin manifest and version, the raw Knowledge
   tree, and separate project/plugin commits.
2. A provenance mismatch previously bypassed semantic checks. Trusted
   validation now has three explicit states: exact current replay, non-executing
   verification of anchored historical Git blobs, or fail-closed unverifiable
   provenance. Read-only historical inspection is explicit and cannot enter a
   Review, Decision, or Gate.
3. The active Profile treated generic file processing and CI as product
   domains. It now requires only the evidenced `plugin-platform` and
   `test-automation-platform` domains.
4. The full 205-entry exclusion ledger was useful to machines but noisy for
   models. Skills now consume a compact, lock-bound Context containing only the
   selected entries; scripts and Gates retain the exhaustive lock.

The final compatibility correction also lets legacy Decisions remain readable
when their frozen Facts and Profile no longer match the active project inputs,
while new trusted Decisions continue to require current bindings.

## Verified strengths

1. `CAG-RUNTIME-MANIFEST-001` — complete runtime provenance and distinct
   project/plugin commits.
2. `CAG-ARCHIVED-LOCK-001` — trusted mismatches require verifiable historical
   source and never execute historical Selector code.
3. `CAG-CONTEXT-PROJECTION-001` — model input excludes the full rejection
   ledger without weakening the authoritative lock.
4. `CAG-PROFILE-RELEVANCE-001` — required Domain Knowledge follows evidenced
   product boundaries.

All eleven Git-bound evidence records resolve at the reviewed commit. The
candidate-to-verified binding, 31 Rule Pack rows, six critical flows, ten audit
Knowledge entries, and the accepted architecture Decision validate.

## Evidence limits

- No new external-model A/B/C quality, token, cost, or tool-call result is
  claimed. The repository contains the harness, not production-selected
  outcome evidence.
- Historical verification after an installed runtime changes currently needs a
  matching local Git clone. A signed release-attestation resolver remains a
  compatible future extension.
- GitHub Dependency Graph is enabled, but the final governance commit's hosted
  CI is not evidence until that commit is published and its jobs complete.

The adjacent candidate Review, verified Review, accepted Decision, frozen
inputs, exhaustive Selection locks, and compact Context projections are the
canonical machine-readable records.
