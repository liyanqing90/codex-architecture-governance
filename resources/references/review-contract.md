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
├── risk-acceptances.yaml
├── evidence-providers.yaml
├── evidence/
├── rules/
└── reviews/
    ├── <timestamp>-<kind>-candidates.yaml
    ├── <timestamp>-<kind>-verified.yaml
    ├── <timestamp>-<kind>-report.md
    ├── <timestamp>-architecture-decision.yaml
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
- Only confirmed risks may enter solution decisions or the default quality
  gate. Only accepted decisions may enter remediation.
- `accepted-risk` requires a separate, authorized, expiring acceptance bound to
  the exact Finding fingerprint. Editing Finding status alone never accepts
  risk.
- Never rewrite a candidate artifact; create a new verified artifact.

## 4. Finding semantics

Every finding represents one invariant at one owning boundary. Use the schema in `../schemas/finding.schema.json`.

Required concepts:

- stable `id` and `rule_id`;
- semantic fingerprint bound to subject, invariant, severity, and evidence;
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
- repository, source commit, path, blob SHA, line or symbol, and excerpt hash
  when Git source evidence is used;
- provider and freshness for runtime or external evidence.

Tool evidence must reference a validated Evidence Provider run by provider ID,
repository-relative run path, and run SHA-256. The run contract binds the
actual executable, provider definition, project configuration, Git state, and
captured output. See `evidence-provider-contract.md`.

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
8. Record verifier type, identity, run ID, time, verification level, candidate
   Review ID, and candidate SHA-256.

The verifier must be independent in stance even when the same agent performs the pass. Agreement among reviewers raises inspection priority but is not proof.

Verification levels:

- `V0`: same-run self-check;
- `V1`: same model in fresh context;
- `V2`: different model or agent;
- `V3`: human review;
- `V4`: human plus deterministic evidence;
- `V5`: controlled signed approval and audit chain.

Trusted-policy enforcement requires a human verifier for V3–V5, passed
deterministic tool evidence for V4–V5, and a detached SSH signature for V5.
The gate verifies that signature against the policy's allowed-signers file.
Policy `role_separation` rejects configured auditor/verifier and other
authority overlaps; role membership is evaluated before findings can gate.

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

Use `review-diff --before <old> --after <new> --project <repo>` to compare
finding and coverage evolution between trusted snapshots.

Schema `1.0` remains readable for migration. Deterministic enforcement requires
trusted `1.1` metadata, complete machine Rule Pack coverage, source bindings,
and evidence resolution according to policy.
