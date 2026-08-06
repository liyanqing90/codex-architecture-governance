# Hengmu 1.0 constrained target architecture review

## Outcome

The independently verified Review reports no remaining architecture Finding for
commit `9b6a7b45293417623a28322de72735c83cbbc6cb`. Hengmu keeps the existing public
router and eight focused Skills, and adds constrained target-architecture design
to the Solution Advisor instead of creating a competing workflow.

The reviewed path covers Design Brief 1.1, Architecture Decision 1.4,
Greenfield Plan 1.3, SSH-bound approval, Evidence Provider isolation and
dependency closure, migration trust downgrade, source anchors, deterministic
Gate behavior, documentation, diagrams, and runtime-only packaging.

## Independent challenge and repair

The first independent Luna pass rejected the initial zero-Finding conclusion:
when a Brief declared multiple approval evidence records, the validator checked
only the last record's SHA-256. The implementation now checks every record in its
own loop. The real signed Greenfield test uses two approval records, tampers with
the first, proves rejection, restores it, and then completes the valid chain.

After that repair was committed, repository facts, Profile, Knowledge Selection,
Knowledge Context, candidate coverage, and all Git evidence were regenerated for
the new immutable source commit. A second Luna pass returned
`VERIFIED_NO_FINDINGS`.

## Coverage

- 31 Rule Pack entries are present exactly once: 28 assessed and 3 explicitly
  not applicable.
- All 6 declared critical flows are assessed with source-commit, blob, and line
  evidence.
- 9 selected Knowledge entries are bound by ID, version, and SHA-256.
- The candidate and verified Reviews are separate artifacts; the verified Review
  binds the exact candidate bytes and source commit.

## Artifacts

- Candidate Review: `2026-08-06-constrained-target-architecture-project-candidates.yaml`
- Verified Review: `2026-08-06-constrained-target-architecture-project-verified.yaml`
- Archived inputs: `inputs/2026-08-06-constrained-target-architecture-*`

## Residual limits

Installed Codex activation behavior, hosted CI provenance, and downstream
cross-platform installation remain release-time external evidence. They are not
silently promoted to locally verified facts.
