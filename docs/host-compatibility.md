# Host compatibility

Hengmu targets **workflow-outcome equivalence**, not identical host controls.
The portable contract is the same public Skills, runtime resources, schemas,
CLI behavior, and persisted artifacts. Invocation syntax, UI, approval prompts,
and lifecycle events remain properties of each agent client.

## Distribution paths

| Host family | Distribution | Automated evidence | Host evidence required before a support claim |
| --- | --- | --- | --- |
| Codex | `hengmu-<version>.zip` with `.codex-plugin/plugin.json` | deterministic inventory, unit tests, checksum, and SBOM | install and route a current Codex surface |
| Agent Plugins clients | `hengmu-<version>-agent-plugins.zip` with root `plugin.json` | schema-aligned source validation plus an extracted audit-path smoke test | install, route, and run the workflow in each named client/version |
| Repository/source consumers | repository root `plugin.json`, `skills/`, and `resources/` | the same source and packaging tests | client-specific source-install test |

Cursor, VS Code/Copilot, and Kiro can be evaluated through the Agent Plugins
distribution when their current versions accept the standard. Passing Hengmu's
archive smoke test proves package completeness and runtime execution; it does
not by itself prove a particular client version installs or renders the plugin.
Release evidence must therefore name the client, version, operating system,
installation path, routed Skill, and observed result.

## Capability equivalence boundary

| Outcome | Portable core | Host-specific boundary |
| --- | --- | --- |
| Audit, verify, design, decide, plan, and explicit gate workflows | Public Skills and shared contracts | Invocation syntax and UI |
| Deterministic project inspection, artifact validation, and Knowledge Selection | Packaged Python CLI and locked runtime dependencies | User or host performs explicit dependency setup and tool invocation |
| Static repository guidance | Skill instructions and repository `AGENTS.md` | Host rules or steering may add guidance but are not required by Hengmu |
| Read-only review behavior | Audit/verification Skill semantics and artifact authority separation | A host may impose stronger tool restrictions; Hengmu does not claim enforcement |
| Session-start scanning | Not a Hengmu capability | Optional future lifecycle adapter only |
| Dangerous-operation interception | Not a Hengmu capability | Host permission policy or pre-tool Hook |
| Automatic completion gate | Not a Hengmu capability; the Gate is explicit | Optional future stop/post-tool Hook |

Hengmu never silently installs dependencies, changes client permissions, or
registers Hooks. The portable runtime supports CPython 3.11–3.13 with the exact
hashes in `requirements-runtime.lock`. Evidence Provider commands remain
project-owned explicit configuration.

## Package identity

The repository owns two manifests:

- `.codex-plugin/plugin.json` is the native Codex identity and the exact
  provenance input already bound by Knowledge Selection artifacts.
- root `plugin.json` is the host-neutral Agent Plugins discovery manifest.

The portable ZIP contains both. Agent Plugins clients discover only the root
manifest; the hidden Codex manifest is inert package data retained so the same
Knowledge Selection implementation and historical source hashes work in both
distributions. Packaging rejects drift between their shared identity fields.

## Lifecycle adapters

Agent Plugins v1 standardizes Skills and MCP, not a cross-client Hook or
permission lifecycle. Any future SessionStart, pre-tool, stop, rules, or
steering integration must be a thin, opt-in adapter with its own host-version
tests and setup instructions. It must not change the portable Skill/CLI
contract or silently broaden user permissions.

See the [Agent Plugins specification](https://agent-plugins.org/specification)
and the accepted
[cross-host equivalence decision](decisions/2026-08-08-adopt-cross-host-workflow-equivalence.md).
