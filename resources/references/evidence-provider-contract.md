# Evidence Provider execution contract

Evidence Providers connect architecture claims to deterministic static,
contract, runtime, security, supply-chain, or test evidence. They do not
automatically discover truth and are never enabled or run implicitly.

## Configure

The bundled catalog defines provider identity, detection markers, evidence
type, output format, trust class, and documentation. The audited repository
owns the executable command in `.architecture/evidence-providers.yaml`.

The catalog includes opt-in quality providers for Ruff (Python), ESLint
(JavaScript/TypeScript), Clippy (Rust), golangci-lint (Go), SwiftLint
(Swift), and Detekt (JVM). Their `ecosystem` and `category` metadata is
descriptive only. `missing_tool_guidance` is advisory prose for a non-ready
capability; it is not an install command and the governance runtime never
installs, resolves, or runs a missing tool automatically.

For every provider:

- keep `enabled: false` until the exact command has been reviewed;
- use an argument array, never shell syntax;
- do not use shell wrappers, compound package runners such as `corepack`,
  package runners such as `npx` or `uvx`, or package-manager installation
  subcommands; the runtime rejects these entry points and shell shebangs;
- pin the project tool dependency or wrapper where the ecosystem permits;
- declare every project-relative lock, toolchain, configuration, plugin, or
  dependency-tree input in `dependency_inputs`; patterns must resolve inside
  the project and directories are hashed recursively;
- Evidence Run 1.2 records that resolved closure before and after execution;
  trusted deterministic evidence requires identical snapshots and a current
  post-run closure;
- set `cache_mode: isolated` for deterministic providers; the runner replaces
  common user-level cache locations with an empty run-scoped cache;
- use a project-owned executable or no-install package invocation; never use
  a provider command that downloads or installs a tool as a side effect;
- use the smallest environment allowlist needed by the command;
- set a bounded timeout and explicit success exit codes;
- retain detection unless the project has documented why
  `allow_without_detection` is safe;
- choose `stdout`, `stderr`, or a run-scoped `file` as the output source.

A file output must pass `{evidence_output}` as an exact command token and use
`result_path: "{evidence_output}"`. This prevents different runs from
overwriting one another.

## Inspect and execute

```bash
python3 resources/scripts/architecture_tool.py evidence-providers --project .
python3 resources/scripts/architecture_tool.py run-evidence-provider \
  --project . --provider <provider-id>
```

The runner:

1. validates the project, catalog, and configuration;
2. requires explicit enablement and project marker detection;
3. resolves an executable file and verifies execute permission;
4. hashes the catalog, provider definition, full configuration, actual
   executable, and every declared dependency-closure file;
5. records repository identity, start/end commits, and dirty-tree state before
   and after execution;
6. invokes the command directly without a shell, with only allowlisted
   environment variables and isolated caches for deterministic providers;
7. enforces the configured timeout;
8. captures stdout, stderr, and optional structured output under
   `.architecture/evidence/`;
9. structurally validates JSON, SARIF 2.1.0, and JUnit XML; and
10. writes a non-overwriting run record with all content hashes.

JUnit parsing rejects DTD and entity declarations. An exit code listed as
successful still produces failed evidence when structured output is malformed.
Text and exit-code providers are captured and hashed but receive no
format-specific semantic assurance.

## Revalidate and cite

```bash
python3 resources/scripts/architecture_tool.py validate-evidence-run \
  .architecture/evidence/<run>.yaml --project . --require-passed
```

Revalidation checks the current provider catalog/configuration, executable,
declared dependency closure, cache mode,
command expansion, Git commit existence, output paths, byte counts, SHA-256
values, timing, and structured content again.

A trusted review cites the run in `tool_evidence` and in any Finding evidence
item of `type: tool`. Both references use the provider ID, repository-relative
run path, and exact run SHA-256. V4 and V5 findings require at least one passed
deterministic run.

## Quality-provider defaults

The quality entries in the bundled catalog are disabled in the template. The
template commands are project-owned starting points: Ruff resolves the selected
environment's `ruff` executable, ESLint resolves the project-local binary,
Clippy uses Cargo in offline mode and the
project Rust toolchain, golangci-lint and SwiftLint use the project-approved
tool resolution, and Detekt uses a pre-provisioned Gradle executable in offline
mode. Maven and Gradle wrappers are not Provider commands because they may
download a build-tool distribution. A project must provision and pin tools and
dependencies before enabling a provider. If an executable or offline dependency
is absent, capability status remains non-ready and non-passing; installation or
dependency resolution requires an explicit user decision outside the runner.

## Trust limits

- A validated deterministic run proves which configured command, executable,
  declared dependency closure, and isolated cache produced the captured bytes;
  it does not prove the closure declaration is semantically complete or that
  the tool is correct.
- `runtime-observation` is bound to its observation window and cannot establish
  all future behavior.
- A dirty-tree run remains readable as informational local evidence but cannot
  enter a trusted Review or Gate.
- A provider that changes HEAD or leaves tracked/untracked project files behind
  cannot produce trusted evidence. Run-scoped evidence output files are excluded
  from this post-run comparison.
- Provider commands may themselves access network or credentials if the
  project deliberately allows them. The governance runtime supplies neither
  automatically.
- Store only redacted evidence. Do not capture credentials, personal data, or
  unrestricted production logs.
