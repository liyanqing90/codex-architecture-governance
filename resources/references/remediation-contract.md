# Remediation planning contract

Plan only from `verification.status: confirmed` risks covered by an accepted
architecture decision. Use `../schemas/remediation-plan.schema.json`.

## Planning unit

Group findings when they share the same owning boundary or one change resolves the same invariant. Keep them separate when they require different authority, migration, or rollback.

Each item must contain:

- linked finding IDs;
- source Review and accepted Decision IDs and SHA-256 bindings;
- desired invariant and owner;
- recommended option;
- alternatives with real tradeoffs;
- do-nothing consequence;
- effort size and uncertainty;
- change risk and governed-change flag;
- prerequisites and dependent items;
- ordered slices;
- test/observability protection;
- rollback or containment;
- migration type, data compatibility, deployment strategy, observability
  changes, and stop conditions;
- measurable acceptance criteria.
- accepted evidence types for every plan item;
- for completed items, repository-relative completion evidence with exact
  SHA-256, result, observation time, and optional Evidence Provider run
  binding.

## Effort scale

- `xs`: hours, one local boundary;
- `s`: roughly one to three focused days;
- `m`: several days across a bounded subsystem;
- `l`: multi-week or cross-team work;
- `xl`: program-level change, migration, or portfolio coordination.

State assumptions. Effort is a range indicator, not a promise.

## Sequencing rules

Prefer:

1. evidence and safety nets;
2. compatibility seams;
3. reversible internal changes;
4. data or contract migration with dual-read/write only when justified;
5. consumer migration;
6. old-path removal after measured acceptance.

Do not recommend parallel structural edits that touch the same boundary. Identify findings that will likely collapse after an earlier fix and re-verify them later.

## Acceptance

Acceptance criteria must be observable. Include the primary path, the owning-boundary invariant, and an adjacent failure or alternate path. “Refactor complete,” “clean architecture,” or a file-size target is not acceptance evidence.

A plan may be proposed without completion evidence. Once the plan or an item
claims completion, every declared `acceptance_evidence_types` value must be
covered by a `completion_evidence` record whose file hash resolves inside the
repository. A provider-backed record also names the provider and validated run.
Status is never accepted as proof by itself.

Flag plans involving persisted data, public contracts, authorization, production infrastructure, deployment, or destructive effects as governed/high-risk. Planning does not authorize execution.

Validate the full chain:

```bash
python3 ../scripts/architecture_tool.py validate-plan \
  <plan.yaml> --review <verified-review.yaml> \
  --decision <accepted-decision.yaml> --project <repository-root>
```
