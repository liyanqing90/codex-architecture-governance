# Migrating from 0.1 to 0.2

Version 0.2 keeps schema `1.0` readable but requires trusted schema `1.1` for
the deterministic quality gate. There is no silent in-place migration because
provenance, verification authority, complete rule coverage, and approvals
cannot be inferred safely.

## 1. Preserve the old artifacts

Keep existing `1.0` reviews as historical evidence. Do not relabel them `1.1`
or copy placeholder hashes into them. A `1.0` review can still be validated
without `--project`, but it cannot gate a commit.

## 2. Update project configuration

Compare the current project files with:

- `resources/templates/profile.yaml`;
- `resources/templates/gate-policy.yaml`;
- `resources/templates/baseline.yaml`;
- `resources/templates/risk-acceptances.yaml`.

Set `schema_version: "1.1"` in the Profile, policy, and baseline. Add:

- structured quality attributes and business context to the Profile;
- an exact `review_requirements` mapping from every required workflow to its
  review kind and Rule Packs;
- policy roles, cumulative stages, freshness and evidence strategy, release
  requirements, role-separation pairs, optional SSH signature policy, and
  `risk_acceptances_file`;
- `.architecture/risk-acceptances.yaml`,
  `.architecture/evidence-providers.yaml`, `.architecture/evidence/`, and
  `.architecture/rules/`.

Keep real project owners and constraints; do not copy template identities into
production policy. Repository-local organization Rule Packs use schema `1.1`
under `.architecture/rules/`; their IDs must not duplicate bundled packs.

## 3. Create a new candidate and verified review

Run the selected audit against the new Rule Packs. The candidate must record
one coverage row for every applicable loaded rule and a reason for each
`not_applicable` or `not_assessed` row.

Generate trusted binding values:

```bash
python3 resources/scripts/architecture_tool.py review-bindings \
  --project . \
  --candidate .architecture/reviews/<candidate>.yaml
```

An independent verifier then creates a `1.1` review that records the candidate
ID/hash, repository identity, Profile and Rule Pack hashes, commit, dirty-tree
state, explicit scope, verification run, verifier identity, verification
level, and Finding fingerprints.

For V3–V5 use a human verifier. V4–V5 also require passed deterministic tool
evidence; V5 additionally requires a detached SSH signature whose identity is
authorized by the policy allowed-signers file.

```bash
python3 resources/scripts/architecture_tool.py validate-review \
  .architecture/reviews/<verified>.yaml --project .
python3 resources/scripts/architecture_tool.py verify-evidence \
  --repo . --review .architecture/reviews/<verified>.yaml
```

## 4. Migrate suppressions explicitly

For every retained baseline or waiver:

1. confirm the same risk still exists;
2. copy the current Finding fingerprint;
3. preserve the accountable owner and reason;
4. add an expiry;
5. add an authorized `approved_by` identity to a waiver.

Move accepted risk into `.architecture/risk-acceptances.yaml`. Each acceptance
requires a matching fingerprint, different `accepted_by` and `approved_by`
identities, compensating controls, acceptance time, and expiry. A Finding with
`status: accepted-risk` blocks if no matching active registry entry exists.

## 5. Insert the solution decision boundary

The remediation planner no longer chooses target architecture or technology.
Run `architecture-solution-advisor`, accept the decision through an authorized
decision maker, and bind a `1.1` plan to both the trusted review and accepted
decision by ID and SHA-256. A new decision needs at least three options,
including keep-current, an exact knowledge-catalog snapshot, quality effects,
business/team/evolution fit, complexity tier, maturity/lock-in notes, and the
full trade-off scorecard.

Generate the non-inferable binding values:

```bash
python3 resources/scripts/architecture_tool.py decision-bindings \
  --project . --review .architecture/reviews/<verified>.yaml
```

Every plan item declares acceptance evidence types. Once `status: complete`,
each declared type must have a repository-relative evidence file and SHA-256;
validate it in repository context:

```bash
python3 resources/scripts/architecture_tool.py validate-plan \
  <plan>.yaml --review <verified>.yaml --decision <decision>.yaml --project .
```

## 6. Enable gate stages gradually

Start with `contract`, then enable `finding`, `change`, and `release` after the
required evidence and decision process exist. Selecting a later stage is
cumulative and fails if a prerequisite stage is disabled.

```bash
python3 resources/scripts/architecture_tool.py gate --project . --stage contract
python3 resources/scripts/architecture_tool.py gate --project . --stage finding
python3 resources/scripts/architecture_tool.py gate --project . --stage change
```

Use `time-window` only when commit binding is genuinely unavailable. Prefer
`exact-commit` for immutable review inputs or `diff-aware` when unaffected
paths may change.

## Compatibility summary

| Artifact or behavior | 0.1 / schema 1.0 | 0.2 trusted path |
| --- | --- | --- |
| Read and schema validate historical review | Supported | Supported |
| Enter deterministic gate | Supported by 0.1 | Requires schema 1.1 |
| Finding suppression | ID plus expiry | ID plus semantic fingerprint and authority |
| Accepted risk | Finding status | Separate two-party registry |
| Rule coverage | Partial allowed | Exact loaded Rule Pack coverage |
| Remediation source | Verified review | Verified review plus accepted solution decision |
| Completion | Narrative status | Hashed evidence covering every declared acceptance type |
| Tool evidence | Unstructured reference | Executable/config/output-bound Evidence Provider run |
| Review identity | String assertions | Role separation, plus SSH artifact signature at V5 |
| Git freshness | Exact commit boolean | Time, exact, ancestor, or diff-aware |

If a project cannot produce the required evidence, retain a `1.0` historical
record or mark the new Finding `needs-evidence`; do not fabricate trust fields.
