# Remediation planning contract

Plan only from `verification.status: confirmed` risks. Use `../schemas/remediation-plan.schema.json`.

## Planning unit

Group findings when they share the same owning boundary or one change resolves the same invariant. Keep them separate when they require different authority, migration, or rollback.

Each item must contain:

- linked finding IDs;
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
- measurable acceptance criteria.

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

Flag plans involving persisted data, public contracts, authorization, production infrastructure, deployment, or destructive effects as governed/high-risk. Planning does not authorize execution.
