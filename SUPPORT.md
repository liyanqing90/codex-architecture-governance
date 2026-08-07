# Support

Use the repository's issue tracker for reproducible defects, documentation
gaps, focused feature proposals, and real-world compatibility reports from
Codex, Cursor, or another Agent Plugins host.

Before opening an issue:

1. run `python3 scripts/validate_repository.py`;
2. record the plugin version and Python version;
3. reduce the problem to the smallest Skill, command, or artifact;
4. remove secrets, personal data, and proprietary source excerpts;
5. include the exact command, exit code, and sanitized error.

For a trusted-review failure, also include the schema version, selected gate
stage, freshness strategy, review ID, and sanitized validation message. Do not
publish source excerpts, review hashes, or repository identity when they are
sensitive.

For an Evidence Provider failure, include the provider ID, output format,
runner status, and sanitized structural-validation error. Do not attach raw
stdout/stderr when it may contain credentials, personal data, or production
records.

For an IDE or host compatibility report, also include:

- the package format (`codex` or `agent-plugins`);
- Hengmu version or commit SHA;
- client name and version, operating system, and installation path;
- Skill name or prompt used;
- expected and observed behavior; and
- sanitized logs or screenshots when they do not contain private data.

Successful reports are useful too: they help separate a reproducible host
compatibility result from an assumption based only on the shared package
format. We do not treat an untested client as verified support.

Open a [bug report](https://github.com/qingye-lab/hengmu/issues/new?template=bug_report.yml)
for incorrect behavior or a
[feature request](https://github.com/qingye-lab/hengmu/issues/new?template=feature_request.yml)
for a focused improvement. Use [SECURITY.md](SECURITY.md) instead of a public
issue for vulnerabilities.

Questions about an audited product's architecture belong to that product's
maintainers. This project can validate its own schemas and quality-gate logic,
but it cannot decide another project's risk acceptance, ownership, or release
policy.

Use the private process in [SECURITY.md](SECURITY.md) for vulnerabilities.
