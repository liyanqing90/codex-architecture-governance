# Security policy

## Supported versions

Until the project reaches `1.0.0`, only the latest released minor version
receives security fixes.

## Reporting a vulnerability

Do not open a public issue for a suspected vulnerability.

Use the repository's private GitHub Security Advisory reporting channel. If the
repository has not enabled private reporting, contact a maintainer privately
through the hosting organization and include:

- affected version or commit;
- impacted Skill, script, schema, or gate;
- a minimal reproduction without real credentials or personal data;
- expected and observed behavior;
- plausible impact and preconditions;
- any safe containment already applied.

Do not probe third-party systems, production services, private networks, or
other users' data.

## Security boundaries

This project:

- reads repository evidence selected by the user or project profile;
- can write `.architecture/` and `.architecture-portfolio/` artifacts when the
  user requests initialization or persistence;
- executes a local Python CLI for schema validation and policy evaluation;
- can execute only explicitly enabled, project-configured Evidence Provider
  commands without a shell, under an environment allowlist and timeout;
- does not itself require or supply network access, credentials, telemetry, or
  an MCP server;
- does not make unverified model findings blocking by default.

Trusted schemas `1.1` and `1.2` bind repository/Profile/Rule Pack/candidate
hashes, complete coverage, verification authority, semantic fingerprints, and
Git/evidence-run evidence. Schema `1.2` also binds deterministic repository
facts, task-scoped knowledge selection, exact selected entries, evidence
fingerprints, and critical-flow coverage. Risk acceptance is a separate
two-party, expiring registry. V5 supports detached SSH artifact signatures.
These are integrity controls, not proof of human identity, provider
correctness, or system security.

The repository inspector is intentionally non-interpretive: a detected
dependency, language, or storage technology cannot create a Finding or
recommendation. Scope traversal outside the explicit repository root is
rejected.

Review every provider command before enabling it. The external executable may
have its own network, credential, file-system, or code-execution behavior; the
runner's hashing and capture make that behavior attributable but do not make an
untrusted tool safe.

Release ZIPs are deterministic and accompanied by SHA-256, SPDX SBOM, and
GitHub provenance/SBOM attestations. Consumers should verify both the digest
and attestation. See [docs/assurance-model.md](docs/assurance-model.md) for
threats and residual risks.

Architecture findings are analysis, not a substitute for a dedicated security
assessment. The quality gate proves policy evaluation of supplied artifacts; it
does not prove that a repository is secure.

## Disclosure

Maintainers will validate scope, coordinate a fix when applicable, and publish
an advisory after affected users have a reasonable update path. Timelines
depend on severity, reproducibility, and maintainer availability.
