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
future review dates, stale entries, and forbidden placeholders.

When adding selection triggers, add a focused case to
`evals/knowledge-selection.yaml` and prove both expected inclusions and
important exclusions. More context is not automatically better.
