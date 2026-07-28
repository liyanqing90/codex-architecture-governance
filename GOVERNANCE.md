# Governance

The project uses a maintainer-led, evidence-first model.

## Maintainer responsibilities

Maintainers:

- protect Skill focus and trigger boundaries;
- preserve artifact and CLI compatibility;
- require executable evidence for quality-gate behavior;
- review dependency, security, and release changes;
- maintain attribution and licensing;
- publish releases from validated tags.

## Decision levels

- Routine fixes and documentation follow normal pull request review.
- New Skills require a distinct use case, activation evals, metadata, and
  repository validation.
- Breaking schemas, exit codes, verification semantics, or gate policy require
  an accepted decision record and migration guidance.
- Risk acceptance remains owned by the repository using the plugin; this
  project does not create waivers on a user's behalf.

## Releases

Releases follow Semantic Versioning:

- patch: compatible fixes and documentation;
- minor: compatible Skills, rules, schemas, or CLI capabilities;
- major: incompatible artifact, policy, or invocation changes.

At least one maintainer must confirm the full repository gate and deterministic
package checksum before publishing a release.
