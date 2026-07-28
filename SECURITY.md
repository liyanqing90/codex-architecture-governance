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
- does not require network access, credentials, telemetry, or an MCP server;
- does not make unverified model findings blocking by default.

Architecture findings are analysis, not a substitute for a dedicated security
assessment. The quality gate proves policy evaluation of supplied artifacts; it
does not prove that a repository is secure.

## Disclosure

Maintainers will validate scope, coordinate a fix when applicable, and publish
an advisory after affected users have a reasonable update path. Timelines
depend on severity, reproducibility, and maintainer availability.
