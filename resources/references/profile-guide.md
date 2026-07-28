# Project profile guide

Use a profile to select applicable architecture rules, not to predetermine findings.

## Field meanings

- `project.id`: stable portfolio and finding prefix; do not derive it from a temporary folder.
- `project.type`: product/system characteristics such as `ai-agent-platform`, `personal-data-system`, `ios-application`, `reminder-system`, `web-application`, or `service`.
- `lifecycle`: changes the acceptable migration and maintenance burden.
- `criticality`: product impact, not code complexity.
- `owners`: accountable people or teams; use `unassigned` only during initialization.
- `critical_qualities`: the few qualities whose failure materially harms the product.
- `required_reviews`: explicit review workflows; custom names are allowed.
- `rule_packs`: rule sets used by installed or project-local audit methods.
- `data_classification`: highest or mixed classification handled by the project.
- file paths: resolve from repository root.

Do not encode a current framework, database, or hosting vendor as an immutable constraint unless a real compatibility, cost, legal, or operational requirement makes it one.

## Suggested review selection

| Project characteristic | Additional review |
|---|---|
| AI agents, RAG, memory, model tools | `ai-agent-architecture` |
| iOS or mobile local state | `mobile-architecture` |
| personal, confidential, or restricted data | `privacy-review` and `data-architecture` |
| authentication, authorization, external tools | `threat-model` |
| multiple coordinated repositories | portfolio audit from the portfolio registry |

Selections are starting points. The explicit profile remains authoritative.

## Initialization

Use `architecture_tool.py init-project`; it refuses to overwrite existing configuration. Then replace placeholders in:

- `profile.yaml`;
- `constraints.md`;
- `critical-flows.md`;
- `gate-policy.yaml`;
- `baseline.yaml`.

Validate with `architecture_tool.py validate-project <repo>`.

Illustrative profiles are in:

- `../templates/cognera-profile.example.yaml`;
- `../templates/assetkeeper-profile.example.yaml`.

They are examples, not facts about the current repositories.
