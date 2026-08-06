# Decision artifact workflow

## Evolution assessment gate

Use this gate when the question concerns an emerging architecture or
technology, an upgrade, or a replacement. It is a bounded evidence assessment,
not a trend report and not an additional source mode. The decision still uses
exactly one valid source mode: a verified Review for Remediation or an approved
validated Design Brief for Greenfield.

Before generating a decision, copy
`../../resources/templates/evolution-assessment.md` to a project-relative
companion Markdown file and complete this evidence packet:

| Required check | Minimum record | Stop condition |
| --- | --- | --- |
| Current baseline | Keep-current/local-correction option, owner, current measures, and do-nothing consequence | No baseline or no observed current measure |
| Capability/quality gap | Scenario, current value, target, measurement method, evidence, and threshold | Gap is only novelty, popularity, naming, or hypothetical scale |
| Volatile claims | Official publisher and URL, exact claim, scope, reviewed/accessed date, freshness decision, and bound knowledge/source entry | Version, support, compatibility, security, license, price, limit, roadmap, or benchmark claim lacks current official evidence |
| Compatibility and migration | Consumers, public/persisted contracts, data, mixed-version behavior, migration steps, duration, and cost | Compatibility or migration cost is unknown for an affected contract |
| Operational/team fit | Owner, skills, support/on-call, observability, failure semantics, security, and operating cost | No accountable operator or material fit assumption is untested |
| Lock-in and rollback | Proprietary surface, portability/exit cost, rollback point, data recovery semantics, and irreversible gate | Rollback or exit cannot be described and tested |
| Shadow/pilot evidence | Bounded cohort or shadow, success/stop criteria, observed measures, and evidence owner | An applicable pilot has not run; keep-current or evidence-only remains the outcome |
| Revisit triggers | Metric/event, threshold, owner, review date/cadence, and reopening evidence | Trigger is vague, unowned, or not measurable |

Current official evidence is required for volatile claims even when the source
is authoritative. Record the review date and source scope; do not silently
carry forward a stale source. Official documentation establishes a claimed
capability, not project fit. A missing or stale source is an unknown and must
not increase an option's score.

The packet must compare keep-current/local correction, the smallest compatible
structural improvement, and a materially viable upgrade or replacement when
the evidence supports it. The selected option may remain keep-current. A
proposed decision is not adoption authority, and the router must never accept
it, create the packet, mutate artifacts, or run a gate on the advisor's behalf.

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

For an evolution assessment, bind the official volatile-claim sources and the
shadow/pilot evidence in the companion Markdown record. Keep claims that are
not current, official, or project-observed in `unknowns`; they cannot justify
selecting an upgrade or replacement. If the evidence packet is incomplete,
record keep-current or stop before decision generation rather than filling the
gaps with trend signals.

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

For an evolution assessment, validation is incomplete until the companion
Markdown shows the baseline, measurable gap, current official evidence,
compatibility/migration cost, operational/team fit, lock-in, rollback,
shadow/pilot evidence or an explicit keep-current disposition, and measurable
revisit triggers. Do not call an evidence-only pilot an adoption decision.
Set `decision.assessment_kind: technology-evolution` and add this exact binding
to the Decision:

```yaml
evolution_assessment:
  path: .architecture/reviews/<decision-id>-evolution-assessment.md
  sha256: <sha256-of-the-exact-markdown-bytes>
  disposition: keep-current # or evidence-only, adopt
  baseline:
    owner: <accountable-owner>
    local_correction: <smallest-current-system-correction>
    do_nothing_consequence: <measured-consequence>
    measures:
      - metric: <metric>
        value: <observed-value>
        method: <measurement-method>
        evidence: {path: <project-relative-path>, sha256: <sha256>, description: <description>}
  gap:
    scenario: <quality-scenario>
    current_value: <observed-value>
    target: <target-value>
    measurement_method: <measurement-method>
    threshold: <decision-threshold>
    evidence:
      - {path: <project-relative-path>, sha256: <sha256>, description: <description>}
  volatile_claims:
    - claim: <exact-claim>
      publisher: <official-publisher>
      url: <official-url>
      scope: <version-and-capability-scope>
      accessed_on: <yyyy-mm-dd>
      freshness: current # or stale, unknown
      capture: {path: <project-relative-capture>, sha256: <sha256>, description: <description>}
  compatibility:
    consumers: [<affected-consumer>]
    contracts: [<public-or-persisted-contract>]
    mixed_version_behavior: <coexistence-behavior>
    migration_steps: [<bounded-migration-step>]
    duration: <duration-estimate>
    cost: <migration-cost>
  operations:
    owner: <operating-owner>
    required_skills: [<required-skill>]
    support_model: <support-and-on-call-model>
    observability: <required-observability>
    failure_semantics: <failure-and-recovery-behavior>
    security: <security-impact>
    operating_cost: <measured-or-estimated-cost>
  lock_in_exit:
    proprietary_surfaces: [<proprietary-surface>]
    portability: <portability-boundary>
    exit_cost: <exit-cost>
    data_recovery: <data-recovery-semantics>
  rollback:
    rollback_point: <last-safe-rollback-point>
    irreversible_gate: <explicit-irreversible-step>
    validation: <rollback-validation>
    compatible_state: <state-kept-compatible-until-acceptance>
  pilot:
    status: not-run # or not-applicable, completed
    owner: <pilot-owner>
    cohort: <bounded-cohort>
    success_criteria: [<measurable-success>]
    stop_criteria: [<measurable-stop>]
    observed_measures: [] # completed adoption requires bound measurements
  revisit_triggers:
    - {metric_or_event: <metric-or-event>, threshold: <threshold>, owner: <owner>, review_on: <yyyy-mm-dd>, reopening_evidence: <required-evidence>}
```

The schema requires the complete structured packet. The validator resolves the
report and every measurement, gap, official-source capture, and pilot evidence
path inside the project and verifies each SHA-256. Adoption additionally
requires all volatile claims to be current plus a completed pilot with bound
observed measures. A selected upgrade or replacement requires `adopt`; a
keep-current option cannot claim adoption. Status strings alone are never
adoption evidence.
