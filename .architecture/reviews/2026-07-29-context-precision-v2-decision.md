# ADR-CAG-007: replay-safe local-first Context Precision

## Decision

Adopt Selection schema 1.3 and keep the existing local-first plugin
architecture. New selections bind the creating Selector implementation,
Knowledge manifest and tree, policy version, source commit, canonical result,
and optional semantic decision intent. The validator performs exact
deterministic replay only when those runtime bindings still match.

For the demonstrated wording collision, `plugin-runtime-topology` selects
Plugin Architecture Knowledge and suppresses client data-authority guidance.
`data-authority-topology` remains the explicit namespace for offline writes,
replicas, synchronization, and conflict ownership.

## Why

Replaying historical inputs with a future algorithm changes the meaning of
trusted evidence. Always reconstructing and executing an archived Git runtime
would provide stronger forensic assurance, but adds source-retention,
environment-reconstruction, isolation, and untrusted-code execution costs to
ordinary validation. Creation-time locking is the smallest mechanism that
preserves history while retaining exact replay for current artifacts.

## Alternatives

- Future-runtime replay was rejected because unrelated Knowledge or scoring
  changes can invalidate an unchanged historical Review.
- Mandatory Git-bound replay was rejected as the daily path. It remains a
  viable future V4/V5 archival check when the assurance level justifies its
  operating cost.

## Evidence boundary

The accepted YAML decision binds the verified Review and the 11-entry
decision-specific Knowledge selection. It does not claim new external-model
A/B/C quality, token, cost, or tool-use results.

Earlier project-review inputs are frozen and their hash chain is rebound in the
governance publication commit so active configuration updates cannot silently
invalidate historical evidence.
