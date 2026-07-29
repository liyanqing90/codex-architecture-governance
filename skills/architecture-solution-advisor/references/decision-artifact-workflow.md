# Decision artifact workflow

## Prepare the source context

For Greenfield work, validate the Design Brief:

```bash
python3 ../../resources/scripts/architecture_tool.py validate-design-brief \
  <repo>/.architecture/architecture-design-brief.yaml
```

Create a decision-specific bounded selection. Use `--kind-budget KIND=LIMIT`
when a project needs a tighter type-specific cap. `--maintainer` is an
auditable exception for curation work; it is not a normal product decision
default.

```bash
python3 ../../resources/scripts/architecture_tool.py select-knowledge \
  --facts <repository-facts.yaml> \
  --profile <profile.yaml> \
  --task "<decision problem>" \
  --skill architecture-solution-advisor \
  --output <repo>/.architecture/decision-knowledge-selection.yaml \
  --context-output <repo>/.architecture/decision-knowledge-context.yaml
```

Validate the compact context before reading it:

```bash
python3 ../../resources/scripts/architecture_tool.py validate-knowledge-context \
  <repo>/.architecture/decision-knowledge-context.yaml \
  --selection <repo>/.architecture/decision-knowledge-selection.yaml \
  --facts <repository-facts.yaml> \
  --profile <profile.yaml>
```

Read the compact context index and every selected Markdown entry only after
validation succeeds. Do not place
the full exclusion ledger in model context; scripts, Decisions, and Gates bind
the complete lock. Every architecture style, pattern, technology, reference
architecture, or migration cited by an option must be selected and
SHA-256-bound.

## Create bindings

For remediation, bind a verified Review and the selection:

```bash
python3 ../../resources/scripts/architecture_tool.py decision-bindings \
  --project <repo> \
  --review <verified-review.yaml> \
  --knowledge-selection <decision-knowledge-selection.yaml>
```

For Greenfield work, bind the Design Brief instead:

```bash
python3 ../../resources/scripts/architecture_tool.py decision-bindings \
  --project <repo> \
  --design-brief <architecture-design-brief.yaml> \
  --knowledge-selection <decision-knowledge-selection.yaml>
```

## Write and validate the decision

Start from `../../resources/templates/architecture-decision.yaml`. Use schema
`1.2` for remediation and include only confirmed, unresolved Finding IDs. Use
schema `1.3` for Greenfield work, set `decision_kind: greenfield`, bind the
Design Brief path and SHA-256, and leave `problem.finding_ids` empty.

Write YAML and Markdown under `.architecture/reviews/`, or
`.architecture-portfolio/reviews/` for portfolio work. Validate the decision:

```bash
python3 ../../resources/scripts/architecture_tool.py validate-decision \
  <decision.yaml> --review <verified-review.yaml> --project <repo>
```

For Greenfield work, replace `--review` with
`--design-brief <architecture-design-brief.yaml>`. The command validates exact
knowledge selection hashes and the source context. Keep `decision.status:
proposed` until the authorized decision maker accepts it.
