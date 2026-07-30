# Governance modes

Architecture Governance has three operating modes. They describe how much
process a repository chooses to retain; they do not change the evidence
standard of a command that is explicitly run.

An explicit invocation of `$project-architecture-audit` selects Governed
persistence by default. The Skill runs `prepare-project-audit`, which
atomically initializes a missing `.architecture/` control plane or validates
the existing one. Select Advisory only with an explicitly read-only request;
a missing directory by itself never selects Advisory.

| Mode | Use it for | Persisted work | Gate behavior |
| --- | --- | --- | --- |
| Advisory | A one-off, read-only assessment or early exploration. | None. Do not initialize `.architecture/`; report observations and clearly labelled candidates in the task response only. | Do not invoke the gate. |
| Governed | An important repository that needs review, decision, and migration history. | Profile, candidates, independently verified Reviews, Decisions, and Plans. | A local or CI gate is optional, but any invocation evaluates the normal deterministic policy. |
| Enforced | A critical or organization-managed repository. | Governed artifacts plus risk-acceptance, release, and CI evidence. | Run the change and release gate in CI; policy controls the thresholds and stages. |

`product_mode` in a schema `1.2` gate policy is a declaration of the chosen
operating tier. It never changes a gate result. In particular, setting
`product_mode: advisory` in an existing policy does not make an explicitly
invoked gate pass, skip evidence, or accept unverified findings. Advisory mode
is achieved by not creating governance artifacts and not invoking the gate.

New `init-project` and `init-portfolio` configurations start with
`product_mode: governed`. Promote to `enforced` only when the repository also
has a maintained CI/release workflow and the owners accept its verification,
risk-acceptance, and freshness requirements.

`prepare-project-audit` is idempotent. It derives a starter Profile from
deterministic repository facts when no control plane exists. It refuses to
overwrite a complete or partial `.architecture/` directory; an existing
control plane must validate before the audit proceeds.

## High-risk run records

For Governed or Enforced work at V4/V5, risk acceptance, or release decision
time, a maintainer may add an informational run record:

```bash
mkdir -p .architecture/runs
cp resources/templates/governance-run-manifest.yaml \
  .architecture/runs/GOV-RUN-YYYYMMDD-001.yaml
python3 resources/scripts/architecture_tool.py validate-governance-run \
  .architecture/runs/GOV-RUN-YYYYMMDD-001.yaml --project .
```

Use the corresponding `.architecture-portfolio/runs/` directory for portfolio
work. Record the workflow, identified model/surface, time window, source
commit and scope, selected Knowledge, tools, written artifact paths, stop
reason, and the authorization boundary. Use SHA-256 values only as traceable
snapshot metadata.

The manifest has `trust: informational-only` by design. It is not a Review,
Evidence Provider run, signature, approval, risk acceptance, or gate input;
the gate never reads it. A valid manifest cannot raise a verification level,
approve a decision, or make a release pass. Keep prompts, model output,
credentials, environment values, secrets, and personal data out of it.

This remains a local-first plugin capability: it does not create a hosted
service, MCP server, database, telemetry stream, or remote policy authority.
