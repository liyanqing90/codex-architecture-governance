# Adopt context precision and tiered governance

- Status: accepted
- Date: 2026-07-29
- Owners: repository maintainers
- Scope: repository facts, Knowledge selection, behavior benchmarking, and
  operating-mode boundaries
- Supersedes: none
- Superseded by: none

## Context

The plugin's 0.4.0 trust chain was strong, but a benchmark fixture written in
Swift could become product-level `domain.mobile` evidence for the plugin
itself. A full behavior benchmark also could not distinguish no-Skill, public
Skill, and compressed-Skill behavior, and its execution surface did not expose
token, cost, or tool-call telemetry.

The historical facts, selection, Review, and accepted Decision that contain
that old inference are SHA-bound records. Rewriting them would falsify their
history and would not provide a new independent verification.

## Decision

1. Emit role-bearing repository facts. Only runtime and production roles may
   infer product domains, technology profiles, specialist reviews, or Rule
   Packs. Tests, benchmark fixtures, examples, documentation, generated code,
   and vendor evidence remain visible but non-contributing.
2. Preserve historical accepted artifacts. Repair the inference only through a
   fresh inspected facts/Profile/selection chain and a new independently
   verified Review.
3. Retain all eight public workflow Skills. Keep their distinct authority and
   artifact lifecycles; reduce activated context instead of merging roles.
4. Require total and per-kind Knowledge budgets. Solution Advisor discretionary
   context is Golden-only with exact, auditable exceptions; broad topic overlap
   is not a replacement rule.
5. Define Base, Full, and Compressed benchmark treatments. Full and Compressed
   share workflow-required Knowledge. Record a declared corpus-input proxy,
   labelled separately from actual token, cost, and tool-call telemetry.
6. Expose Advisory, Governed, and Enforced operating modes. A gate policy's
   mode label is descriptive and cannot weaken an explicitly invoked gate.
7. Permit optional high-risk governance run manifests only as informational
   trajectory metadata. They cannot prove V4/V5, authorize risk, or enter a
   gate evidence chain.
8. Keep the plugin local-first and do not add a hosted service, MCP server,
   database, remote knowledge service, telemetry, or credential store.

## Alternatives considered

- Rewrite the historical Decision to remove `domain.mobile` — rejected because
  its hashes and accepted time are evidence of what was actually reviewed.
- Treat all visible files as product evidence — rejected because fixtures,
  tests, generated output, and dev dependencies cause false architecture
  routing.
- Remove or merge Skills to reduce prompts — rejected because it would merge
  audit, verification, decision, planning, and gate authorities before an
  ablation demonstrates no loss.
- Treat character counts as token or cost measurements — rejected because
  models and surfaces tokenize and bill differently and the current surface
  may expose neither value.
- Make run manifests trusted gate inputs — rejected because a self-recorded
  trajectory cannot replace independently validated evidence or authorization.

## Consequences

- Positive: fixture and development evidence remains auditable without
  contaminating product routing.
- Positive: context reduction claims can be tested against a declared,
  reproducible A/B/C condition rather than inferred from prompt length.
- Positive: ordinary users can use an Advisory assessment without adopting a
  persistent governance lifecycle.
- Negative: an old artifact can remain historically accurate while being known
  not to represent current routing; consumers must create a superseding review.
- Negative: benchmark quality comparisons require actual external model runs;
  no result is implied by the harness or context manifest alone.

## Verification

- Test every observable non-product fact role and pruned vendor/generated
  tree against domain inference.
- Replay schema 1.2 selections and reject tampered kind, maturity, count, or
  source inputs.
- Validate all Base/Full/Compressed treatments, equal Full/Compressed Knowledge
  input, context proxy hashes, and condition/manifest-bound commands.
- Prove a governance run cannot be interpreted as a Review or alter a gate
  result.
- Run repository validation, project validation, Knowledge validation, tests,
  lint, formatting, dependency audit, deterministic packaging, checksum, and
  SBOM generation before release.

## Revisit when

- an identified model surface exposes stable per-trial token, cost, or
  tool-call telemetry;
- an A/B/C run shows that a public Skill can be simplified or merged without
  behavior loss;
- multiple users demonstrate a justified need for centralized policy,
  identity, or hosted collaboration.
