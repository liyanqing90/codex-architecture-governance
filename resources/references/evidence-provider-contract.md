# Evidence Provider execution contract

Evidence Providers connect architecture claims to deterministic static,
contract, runtime, security, supply-chain, or test evidence. They do not
automatically discover truth and are never enabled or run implicitly.

## Configure

The bundled catalog defines provider identity, detection markers, evidence
type, output format, trust class, and documentation. The audited repository
owns the executable command in `.architecture/evidence-providers.yaml`.

For every provider:

- keep `enabled: false` until the exact command has been reviewed;
- use an argument array, never shell syntax;
- pin the project tool dependency where the ecosystem permits;
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
4. hashes the catalog, provider definition, full configuration, and actual
   executable;
5. records repository identity, commit, and dirty-tree state;
6. invokes the command directly without a shell, with only allowlisted
   environment variables;
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
command expansion, Git commit existence, output paths, byte counts, SHA-256
values, timing, and structured content again.

A trusted review cites the run in `tool_evidence` and in any Finding evidence
item of `type: tool`. Both references use the provider ID, repository-relative
run path, and exact run SHA-256. V4 and V5 findings require at least one passed
deterministic run.

## Trust limits

- A validated run proves which configured command and executable produced the
  captured bytes under the recorded environment; it does not prove the tool is
  correct.
- `runtime-observation` is bound to its observation window and cannot establish
  all future behavior.
- A dirty-tree run records that state and may be rejected by project policy.
- Provider commands may themselves access network or credentials if the
  project deliberately allows them. The governance runtime supplies neither
  automatically.
- Store only redacted evidence. Do not capture credentials, personal data, or
  unrestricted production logs.
