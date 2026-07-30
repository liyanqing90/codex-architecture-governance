# Reset the public identity to Hengmu

- Status: accepted
- Date: 2026-07-30
- Owners: Qingye
- Scope: repository slug, plugin identity, release artifacts, public metadata,
  and pre-rename governance provenance
- Supersedes: the public naming compatibility clause in `CHANGELOG.md`
- Superseded by: none

## Context

The project adopted Hengmu as its public name before it had external users, but
kept `codex-architecture-governance` as the repository slug, installable plugin
ID, and release archive prefix. That split identity made installation,
discovery, badges, package provenance, and brand presentation disagree.

There are no historical users or installations that require the old public
machine identity. The repository does contain hash-bound self-review artifacts
created before the rename. Rewriting those artifacts would falsify their
recorded provenance rather than improve compatibility.

## Decision

1. Use `hengmu` for the GitHub repository slug, installable plugin ID, release
   archive prefix, SBOM package and tool identity, CI marker, and public links.
2. Use Hengmu as the plugin display name and Qingye as the public developer
   identity.
3. Make plugin validation independent of the local checkout directory name.
   Git permits callers to choose any clone directory, so the directory is not
   an authoritative package identity.
4. Treat the old and new GitHub URLs as aliases only while resolving immutable
   pre-rename Selector Runtime locks. Do not expose the old name to new
   installations or newly generated artifacts.
5. Preserve pre-rename self-review bytes and Git ancestry. New governance
   artifacts use the Hengmu identity; old artifacts remain historical evidence.

## Alternatives considered

- Keep the old machine identity indefinitely — rejected because there are no
  users to protect and it would preserve avoidable public inconsistency.
- Rewrite historical Reviews and selections — rejected because their hashes,
  source commits, and recorded identities describe what was actually reviewed.
- Rewrite Git history — rejected because a normal additive change preserves
  auditability and GitHub repository rename redirects provide a safer
  transition.

## Consequences

- Positive: repository, plugin, documentation, release, and provenance surfaces
  present one discoverable name.
- Positive: fresh clones validate even when users choose a custom directory.
- Negative: an unreleased checkout or script that hard-codes the old plugin ID
  must be updated; no compatibility adapter is provided.
- Negative: internal pre-rename evidence still contains the former identity by
  design.

## Verification

- Validate the repository and all public Skill contracts.
- Prove old and new repository URLs resolve to one historical Selector source.
- Build the deterministic package and assert the archive, SBOM package,
  namespace, and creator use Hengmu.
- Run the full test suite, lint, format check, architecture gate, and history
  anchor validation.
- After the GitHub rename, verify the new repository, branch SHA, old URL
  redirect, local `origin`, and CI status.

## Rollback

Before a release, revert this decision commit and rename the GitHub repository
back to `codex-architecture-governance`. After a Hengmu release, rollback
requires a new decision because published repository and package identities
will have external consumers.

## Revisit when

- a package registry introduces a separate immutable package identity;
- GitHub stops redirecting renamed repositories;
- pre-rename governance evidence is intentionally retired under a documented
  retention policy.
