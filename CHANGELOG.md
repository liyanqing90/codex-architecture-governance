# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-07-28

### Added

- Architecture Solution Advisor and Architecture Knowledge Curator Skills.
- Eight machine-readable quality, style, pattern, technology, reference
  architecture, migration, domain, and decision-guide catalogs with 128
  sourced entries.
- Architecture Decision, Risk Acceptance, Rule Pack, Knowledge, Evidence
  Provider, and Benchmark schemas.
- Verified-review provenance bindings, verification levels, Finding
  fingerprints, Git evidence resolution, repository path containment, and
  machine-complete Rule Pack coverage.
- Contract, Finding, Change, and Release gate stages with exact, ancestor, and
  diff-aware freshness.
- Nineteen bundled core/domain Rule Packs plus validated repository-local
  organization Rule Packs.
- Eleven executable Evidence Provider adapters with shell-free invocation,
  executable/config/output hashing, timeout, safe environment propagation, and
  JSON/SARIF/JUnit structural validation.
- Role separation, human V3–V5 assurance requirements, deterministic evidence
  for V4–V5, and detached SSH review signatures at V5.
- Knowledge-bound three-option architecture decisions, hashed plan completion
  evidence, required-review enforcement, base-commit change classification,
  and review diffing.
- Ten adversarial architecture fixtures, repeated-trial stability, duration
  and optional usage metrics, deterministic benchmark scoring, and a
  caller-supplied forward-test harness.
- Fingerprint-bound baselines and waivers plus separately authorized,
  expiring risk acceptance.
- Fully hashed runtime/development locks, cross-platform checksum verification,
  license allow/deny audit, license-complete SPDX SBOM generation, dependency
  audit, SARIF output, and GitHub provenance/SBOM release attestations.

### Changed

- Trusted enforcement now requires artifact schema `1.1`; schema `1.0`
  remains readable for migration.
- Remediation planning consumes an accepted architecture decision instead of
  selecting technology and target architecture itself.
- CI now covers Python 3.11 and 3.13 on Ubuntu, macOS, and Windows.
- Plugin and portable CLI version are now `0.2.0`.

## [0.1.0] - 2026-07-28

### Added

- Seven focused architecture-governance Skills for project, AI-agent, mobile,
  portfolio, verification, remediation-planning, and quality-gate workflows.
- Versioned review, finding, profile, portfolio, remediation, baseline, and
  policy schemas.
- A portable CLI for initialization, validation, and deterministic policy
  evaluation.
- Repository validation, activation eval corpus, deterministic plugin
  packaging, CI, release automation, and open-source governance documents.
- A dogfooded project architecture profile with explicit constraints and
  critical flows.
