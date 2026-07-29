# Knowledge authoring

Architecture knowledge supports a decision; it does not decide for a project.

## Choose the pack

Use the narrowest semantic kind:

| Kind | Canonical ID prefix | Purpose |
| --- | --- | --- |
| Foundation | `foundation.` | Stable cross-domain reasoning |
| Domain | `domain.` | Domain-specific forces and evidence |
| Decision guide | `decision.` | Compare named alternatives |
| Architecture style | `style.` | System organization and ownership model |
| Pattern | `pattern.` | Bounded implementation mechanism |
| Technology profile | `technology.` | Capabilities and operating liabilities |
| Reference architecture | `reference.` | A compositional starting point |
| Migration guide | `migration.` | Reversible evolution path |
| Anti-pattern | `anti-pattern.` | Contextual failure mechanism |
| Case study | `case-study.` | Evidence-backed proportionality example |

Do not use a technology profile to encode a style, or an anti-pattern to ban a
product by name.

## Required frontmatter

Every entry must satisfy
`resources/schemas/knowledge-entry.schema.json` and include:

- canonical ID, kind, semantic version, and lifecycle status;
- domains, task triggers, affected quality attributes, and related IDs;
- last-reviewed date and review window;
- source policy and at least one HTTPS authoritative source;
- for technology profiles, `dynamic_facts` and a supported `version_range`
  statement.

`last_reviewed` is an evidence date, not a publication convenience. Never move
it forward without inspecting the cited material.

Generated entries must use `status: draft` and
`curation.method: generated`. An active entry cannot carry generated
provenance.

Golden entries set `maturity: golden` and record a non-generated curation
method, reviewer, and date. In addition to the common body contract:

- decision guides define at least two named options, each with explicit
  `Fit`, `Avoid`, `Cost`, and `Failure` fields;
- styles and patterns define an operating model;
- technology profiles define an operating model and capability boundaries;
- reference architectures define component responsibilities and data flow;
- every golden entry defines at least two claim IDs in `Claim map`;
- every source declares the exact claim IDs it supports.

The validator compares golden entries for high template similarity. Shared
headings are expected; repeated generic mechanism prose is not.

## Selection budgets and maturity

New selection artifacts use schema `1.4`. They bind each selected entry's
`kind` and `maturity`, retain a total entry cap, and account for all ten kinds
individually. The Selector Runtime Input Manifest binds the plugin repository,
plugin source commit and version, plugin manifest, exact transitive Python,
dependency-lock, and schema inputs, the complete raw Knowledge tree, policy
version, and canonical result hash. `inputs.project_commit` separately binds
the repository being reviewed.

Validation has three explicit states:

- **Current replay**: the complete Runtime Manifest equals the installed
  runtime, so selection is executed again and compared exactly.
- **Archived lock**: the runtime differs, but `CAG_SELECTOR_SOURCE_ROOT`
  or the plugin checkout resolves the recorded repository and commit. The
  validator checks every Git blob and selected Knowledge record without
  executing historical code.
- **Unverifiable lock**: the source is unavailable or any anchored byte
  differs. `--read-only` permits inspection, but trusted Reviews, Decisions,
  and Gates reject the artifact.

Use `--kind-budget KIND=LIMIT` to tighten a kind without letting another kind
silently consume the freed context budget. Mandatory Skill and decision-intent
contracts must fit both caps; the selector fails rather than silently dropping
one. Pass `--context-output` to write a compact model-facing index containing
only selected IDs, paths, priorities, reasons, and hashes. Keep exclusions and
runtime provenance in the full machine lock. Run
`architecture_tool.py validate-knowledge-context` with the exact Selection,
Facts, and Profile paths before any Skill reads that compact index.

The Solution Advisor is Golden-only for discretionary context. A standard entry
may appear only when its recorded reason is one of:

- a required Skill contract dependency;
- an explicit caller include;
- maintainer mode;
- an exact profile-required domain with no declared Golden replacement; or
- an exact detected technology with no declared Golden replacement; or
- an exact, caller-declared decision-intent match.

A broad domain or task-token overlap is not a Golden replacement match.
`--maintainer` is deliberately visible in the selection inputs and is reserved
for curation or maintenance work; it should not be the default for an ordinary
architecture decision.

Use `--decision-intent plugin-runtime-topology` when deciding hosted versus
locally installed plugin execution. Use
`--decision-intent data-authority-topology` only for client replicas, offline
writes, synchronization, and conflict ownership. Ambiguous text such as
`local-first` does not activate the data-authority guide without that semantic
namespace.

## Failure-driven expansion

Do not grow the Knowledge library as a framework catalogue. A proposed new
Golden entry, or a material expansion of one, must begin with a concrete
decision-quality gap: a benchmark false negative or false positive, unstable
recommendation, missing trade-off, verified project finding, user rejection or
correction, or a documented incident/rollback.

For each promotion, preserve the source of that gap in the curation change and
add the smallest representative regression: an evaluation case, benchmark
fixture/ground-truth update, or deterministic validator test. State why an
existing Golden entry cannot cover the gap. Popularity, broad topic overlap,
or a desire for a complete technology inventory is not sufficient evidence.

Historical entries are not retroactively relabelled to meet this rule. Apply it
to new curation work and use fresh evidence when replacing a stale or
insufficient recommendation.

## Required body

Use one level-one title and all fourteen level-two sections:

1. Problem and intent
2. Mechanism
3. Fit when
4. Avoid when
5. Required capabilities
6. Benefits
7. Costs and liabilities
8. Failure modes
9. Alternatives
10. Migration and exit
11. Evidence to inspect
12. Evidence that changes the recommendation
13. Quality trade-offs
14. Volatile facts

State what would falsify the recommendation. A shallow list of benefits is not
decision knowledge.

## Source policy

- Use standards for stable quality models and protocols.
- Use official or maintainer documentation for product capabilities,
  compatibility, lifecycle, and operational constraints.
- Use research for empirical claims not established by primary documentation.
- Verify versions, support status, security advisories, pricing, service
  limits, and current defaults from official sources at decision time.

Do not encode popularity, search rank, or unsourced “best practice” as a
decision rule.

## Relationships and compatibility

Relationships must reference canonical IDs that exist in the same validated
tree. `legacy_ids` may map a 0.2 catalog identifier to one canonical Markdown
entry, but aliases must be globally unique. Removing or changing the semantics
of a canonical ID requires migration guidance and a compatible versioning
decision.

## Validation workflow

Run:

```bash
python3 resources/scripts/validate_knowledge.py
python3 scripts/validate_repository.py
python3 -m pytest tests/test_target_architecture.py
```

The validator rejects invalid frontmatter, missing or shallow sections,
duplicate IDs, duplicate aliases, unknown relationships, non-HTTPS sources,
future review dates, stale entries, generated-active promotion, unsupported
golden claims, shallow option analysis, template similarity, and forbidden
placeholders.

When adding selection triggers, add a focused case to
`evals/knowledge-selection.yaml` and prove both expected inclusions and
important exclusions. More context is not automatically better.
