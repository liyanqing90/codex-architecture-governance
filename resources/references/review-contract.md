# Architecture review contract

## Contents

1. Sources of truth
2. Artifact layout
3. Review lifecycle
4. Finding semantics
5. Evidence standard
6. Severity and confidence
7. Verification rules
8. Coverage and reporting

## 1. Sources of truth

Use this precedence:

1. current executable behavior, schemas, migrations, contracts, deployment configuration, and tests;
2. accepted architecture decisions and current product requirements;
3. `.architecture/profile.yaml`, constraints, and critical flows;
4. other documentation and repository history;
5. inference.

A higher source may still be defective; precedence decides what exists, not what is desirable. Record contradictions as evidence.

## 2. Artifact layout

Use project-local state:

```text
.architecture/
├── profile.yaml
├── constraints.md
├── critical-flows.md
├── gate-policy.yaml
├── baseline.yaml
└── reviews/
    ├── <timestamp>-<kind>-candidates.yaml
    ├── <timestamp>-<kind>-verified.yaml
    ├── <timestamp>-<kind>-report.md
    └── <timestamp>-remediation.yaml
```

Use portfolio-local state:

```text
.architecture-portfolio/
├── portfolio.yaml
├── shared-capabilities.yaml
├── technology-catalog.yaml
├── dependency-map.yaml
├── gate-policy.yaml
├── baseline.yaml
└── reviews/
```

Treat YAML as canonical. Markdown is a human projection and must not introduce findings absent from YAML.

## 3. Review lifecycle

Use this state flow:

```text
candidate → confirmed → planned → in-progress → resolved
         ↘ rejected
         ↘ needs-evidence
confirmed → accepted-risk
```

- Candidate audits may contain `verification.status: candidate`.
- Verified reviews must contain no candidate verification states.
- Audit Skills own candidate artifacts. `architecture-finding-verifier` alone
  owns verified artifacts and the final human report.
- Keep rejected and needs-evidence items in verified YAML for auditability.
- Only confirmed risks may enter remediation or the default quality gate.
- Never rewrite a candidate artifact; create a new verified artifact.

## 4. Finding semantics

Every finding represents one invariant at one owning boundary. Use the schema in `../schemas/finding.schema.json`.

Required concepts:

- stable `id` and `rule_id`;
- `kind`: `risk` or `strength`;
- title and invariant;
- severity and calibrated confidence;
- verification status and rationale;
- lifecycle status;
- one or more concrete evidence items;
- affected components, failure mode, and blast radius;
- first-seen and last-seen dates.

Stable IDs must survive wording and line-number changes. Prefer:

```text
<scope>-<rule-family>-<sequence>
```

Examples: `CGN-MEM-001`, `AK-SYNC-002`, `PORT-IDP-001`.

Do not reuse an ID for a different invariant. Record merged duplicate IDs in `related_findings`.

## 5. Evidence standard

Each evidence item must state:

- evidence type: source, config, schema, migration, test, runtime, history, or document;
- path, URL, trace, query, or other stable location;
- symbol or line when applicable;
- concrete observation;
- source commit or freshness when available.

Short excerpts are optional and must be redacted. Do not paste credentials, personal data, full logs, or large copyrighted text.

An architecture risk requires a relationship or failure path:

```text
trigger/state → control or data path → owning boundary → violated invariant → impact
```

Counts and names may identify hotspots but do not prove a violation. “Could become a problem at scale” is an unknown unless the profile defines the scale requirement.

## 6. Severity and confidence

Calibrate severity by actual impact:

- `critical`: plausible immediate compromise, irreversible loss, unsafe financial action, or portfolio-wide outage without effective containment;
- `high`: critical-flow failure, serious privacy/security exposure, unrecoverable corruption, or multi-component outage;
- `medium`: bounded reliability, operability, maintainability, or change-cost risk with a credible failure path;
- `low`: localized friction or debt with limited blast radius;
- `info`: strength or observation that does not represent a current risk.

Confidence is evidence confidence, not impact:

- `0.90–1.00`: directly demonstrated by executable or runtime evidence;
- `0.75–0.89`: strongly supported by current code and relevant contracts;
- `0.60–0.74`: plausible but incomplete; normally use `needs-evidence`;
- below `0.60`: omit from the review.

Profile critical qualities may raise impact only when the finding affects a declared critical flow.

## 7. Verification rules

For every candidate:

1. Re-read the cited source at the recorded or current commit.
2. Inspect the minimum callers, data owners, schemas, configuration, tests, and history needed to validate the path.
3. State and test the strongest benign counter-explanation.
4. Confirm applicability to the project's profile and constraints.
5. Confirm category, severity, confidence, and affected scope.
6. Deduplicate by invariant, not wording.
7. Record a rationale for `confirmed`, `rejected`, or `needs-evidence`.

The verifier must be independent in stance even when the same agent performs the pass. Agreement among reviewers raises inspection priority but is not proof.

## 8. Coverage and reporting

For every applicable rule, record:

- `assessed`: evidence was inspected;
- `not_applicable`: the rule does not apply, with a reason;
- `not_assessed`: evidence was missing or scope excluded it, with a reason.

Do not use “no finding” as proof of correctness. Report coverage and limitations explicitly.

Human reports must contain:

- subject, commit(s), scope, date, profile, and inspected inputs;
- architecture summary or maps;
- strengths;
- confirmed risks ordered by severity;
- critical-flow and ownership impact;
- coverage and evidence gaps;
- raw, confirmed, rejected, and needs-evidence counts.

Validate artifacts using `../scripts/architecture_tool.py`.
