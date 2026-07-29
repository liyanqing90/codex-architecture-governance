# Outcome provenance architecture review

## Boundary and result

- Reviewed implementation: `cf254fafe51844275a8d2dd8e622a8e850703f03`
- Candidate findings: 3
- V2 agent-confirmed strengths: 3
- Confirmed risks: 0
- Rule coverage: 31 of 31
- Critical-flow coverage: 6 of 6
- Resolved Git evidence: 9 of 9

The implementation closes all three machine-enforceable gaps in the external
PR #8 audit. Git-verified archived Selection locks remain readable, but only a
Selection replayed by the current runtime can create a new trusted Review,
Decision, Plan, coverage result, or Gate. Compact Context now has a
consumption-time validator for its Selection file hash, canonical result hash,
and exact ordered selected-entry projection. CI and releases require the
Selector source and latest reviewed implementation commits to remain ancestors
of `HEAD`.

## Compatibility and operating conditions

Historical inventory and explicit `--historical` validation remain available;
no historical artifact is rewritten. Public Skills validate Context before
reading selected Markdown. The accepted `ADR-CAG-009` keeps enforcement inside
the portable CLI and workflows rather than silently changing repository-wide
GitHub merge settings.

PR #8 must be integrated with **Merge Commit**. Squash or rebase merging would
discard reviewed ancestry and is rejected by `validate-history-anchors`.

## Evidence limits

- The verified Review is V2 agent evidence. It does not claim the human V3
  acceptance requested by the external reviewer.
- No new production-selected A/B/C quality, token, cost, or tool-call result is
  claimed.
- Hosted CI and Dependency Review become evidence only after the governance
  commit is pushed.

The adjacent candidate Review, verified Review, accepted Decision, frozen
inputs, Selection locks, and Context sidecars are the canonical
machine-readable records.
