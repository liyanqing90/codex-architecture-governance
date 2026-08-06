# Adopt efficient, extensible review execution

- Status: accepted
- Date: 2026-08-06
- Owners: repository maintainers
- Scope: Evidence Providers, AI-agent review depth, technology evolution,
  model-visible context, incremental review execution, run telemetry, and
  validation performance
- Supersedes: none
- Superseded by: none

## Context

Hengmu already separates model-produced candidates, independent verification,
architecture decisions, remediation, and deterministic gates. The next product
need is not a broader all-purpose scanner. It is a more efficient review engine
that can consume project-owned quality evidence, inspect modern AI-agent
boundaries deeply, and decide whether new technology has demonstrated upgrade
or replacement value.

The current execution path has several concrete limits:

- the bundled Evidence Provider catalog is small, and catalog growth requires
  every project configuration to repeat every provider;
- missing tools are observable but the workflow does not clearly distinguish
  unavailable, unconfigured, disabled, and ready capabilities or the authority
  required to install a tool;
- the AI-agent lens does not separately require context necessity, compression
  loss, ordering and cache effects, privacy minimization, or version-bound
  behavioral evidence;
- technology comparison does not make upgrade and replacement value a named
  decision mode with a current-system baseline and adoption evidence;
- stable contracts, project context, run-specific facts, and source evidence
  are not explicitly ordered as separate model-context tiers;
- normal governance runs cannot record declared context, token, cache, tool,
  source-reading, or stage-duration observations;
- repeated review validation reparses schemas and the complete Knowledge tree;
  and
- repeat reviews lack a deterministic change-impact plan that can narrow
  investigation without inheriting an unproved pass.

## Decision

1. Keep the product boundary as **narrow governance core, broad opt-in
   integrations, deep evidence and verification loop**. Do not add a hosted
   service, generic code scanner, package manager, or autonomous upgrader.
2. Expand Evidence Providers with a representative cross-language quality set.
   Keep commands project-owned, disabled by default, and independently hashed.
3. Treat provider configuration as sparse. Catalog additions must not invalidate
   an older project solely because it has not configured the new provider.
4. Report provider capability states deterministically. Never install or enable
   a tool implicitly. Installation is an external project change and requires
   explicit user authorization after the exact package, command, scope, and
   consequence are shown.
5. Extend the AI-agent review with explicit invariants for context relevance,
   compression fidelity, stable ordering and cache boundaries, privacy
   minimization, version-bound behavior evidence, and evidence-based runtime or
   protocol evolution.
6. Make technology refresh an evidence-governed solution decision. Always
   compare keep-current, local improvement, upgrade, and replacement candidates
   against the same quality scenarios, compatibility, migration, operations,
   cost, lock-in, rollback, and pilot evidence.
7. Use progressive model context in this order: a stable operational kernel,
   project-stable Profile and constraints, run-specific facts and selection,
   then source evidence on demand. Preserve full source hashes and load full
   content when a candidate-driving claim or ambiguity requires it.
8. Add optional, informational execution telemetry. Unavailable token, cache,
   cost, or tool data remains absent or null and never becomes Gate evidence.
9. Reuse exact, content-bound schema and Knowledge validation within one process.
   A cache must detect in-process byte changes and must not weaken a release
   validation.
10. Add a deterministic change-impact review plan. Derive changed paths from
    Git and impact classes from the project Gate policy; never trust caller-
    declared impact. Incremental review may reuse a prior verified result only
    as context when repository identity, commit ancestry, evidence fingerprints,
    rule applicability, and critical-flow impact remain valid. Unaffected does
    not mean silently passed.
11. Give parallel specialists one shared compact evidence index and disjoint
    scopes. Keep synthesis in the coordinator and preserve a fresh-context
    verifier that rereads the smallest sufficient source set.
12. Improve the stable `hengmu` entry with read-only lifecycle navigation. It may
    explain the next valid focused workflow from existing artifact state, but it
    may not make findings, accept decisions, mutate policy, or run a gate
    implicitly.
13. Protect Hengmu's own governance surface by classifying public Skills, Rule
    Packs, schemas, selection/validation code, and critical-flow definitions as
    change-sensitive paths in the repository policy.
14. Reject duplicate JSON keys during repository validation. A schema or
    manifest with ambiguous duplicate fields is invalid instead of silently
    inheriting the parser's last-value behavior.
15. Bind every technology-evolution assessment to its exact companion Markdown
    path and SHA-256. Adoption requires complete evidence and a completed pilot;
    keep-current and evidence-only remain valid explicit outcomes.
16. Enforce no-install Provider commands at configuration validation, and make
    diff-aware Gates fail when changed paths fall outside the selected Review's
    bound scope. Informational execution plans are not enforcement authority.
17. Represent evolution baseline, gap, current official claims, compatibility,
    operations, exit, rollback, pilot, and revisit evidence as structured
    Decision fields. Bind every local measurement and source capture by path and
    SHA-256; status labels alone cannot authorize adoption.

## Compatibility and coexistence

- Preserve every public Skill name and the router/focused-workflow authority
  boundaries.
- Make catalog and informational telemetry additions backward compatible.
- Continue reading existing provider configurations and governance-run schema
  1.0 artifacts.
- Keep existing full-review behavior as the safe fallback when no verified
  baseline, Git ancestry, or impact closure is available.
- Do not migrate legacy verification status or infer provider success from
  installation, detection, or an exit code without valid structured evidence.

## Alternatives considered

- Bundle and automatically install every language linter — rejected because it
  expands authority, dependency, network, and supply-chain scope and cannot
  respect project-owned configuration.
- Build a universal static-analysis engine inside Hengmu — rejected because
  language-specific parsing and semantics belong in optional providers or
  project-native tools.
- Remove independent verification to save context — rejected because a fresh
  skeptical pass is the authority boundary that filters model false positives.
- Treat the compact-context character proxy as token savings — rejected because
  actual tokenization, prompt caching, and billing belong to the model surface.
- Use a persistent unverified cache to accelerate validation — rejected because
  stale cached trust would undermine deterministic enforcement.

## Consequences

- Positive: projects can add language and runtime evidence without making Hengmu
  own those toolchains.
- Positive: missing tools become an explicit capability and authorization state
  rather than an implicit failure or installation side effect.
- Positive: AI-agent reviews cover context economics and technology evolution as
  architecture mechanisms, not framework fashion.
- Positive: repeated audits and validation can consume less model context and
  deterministic compute while retaining provenance.
- Negative: provider metadata, context projections, execution observations, and
  change-impact plans add contracts that require compatibility tests.
- Negative: context compression cannot become the production default until
  current-version Full/Compressed behavioral evidence establishes non-inferior
  findings and evidence validity.

## Verification

- Validate old and sparse provider configurations and reject implicit provider
  execution or installation.
- Exercise ready, disabled, unconfigured, undetected, and missing-executable
  provider states.
- Validate AI context, privacy, behavioral evidence, and technology-evolution
  rule coverage with direct, incomplete, negative, and edge cases.
- Validate old governance-run manifests and new optional telemetry, including
  unavailable metrics.
- Prove an in-process Knowledge or schema byte change invalidates reused
  validation state.
- Exercise full and incremental review plans, non-ancestor commits, critical and
  security changes, and missing prior verification.
- Compare Full and Compressed context using the current benchmark contract before
  claiming model-quality, token, cache, duration, or cost improvements.
- Run repository validation, project validation, tests, lint, formatting,
  dependency audit, packaging, checksum, SBOM generation, and the architecture
  change Gate.

## Revisit when

- Codex exposes stable per-stage token and prompt-cache telemetry;
- a language provider requires host-level capabilities that cannot be expressed
  safely as a project-owned subprocess;
- dependency closure from language-native tooling is reliable enough to become
  trusted incremental evidence; or
- measured context compression reduces finding recall or evidence validity.
