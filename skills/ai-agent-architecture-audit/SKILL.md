---
name: ai-agent-architecture-audit
description: Specialized architecture audit for AI-agent systems and AI-enabled products. Use for agent runtimes, tool-using workflows, memory systems, RAG, MCP integrations, long-running tasks, model routing, evidence tracking, human approval, evaluations, or systems exposed to prompt injection and model uncertainty. Extends rather than replaces the general project architecture audit.
---

# Audit AI-agent architecture

Assess whether probabilistic model behavior is safely bounded by deterministic product and operational controls.

## Load the contract

Read these files completely:

- `../../resources/references/review-contract.md`
- `../../resources/references/knowledge-contract.md`
- `../../resources/references/ai-agent-rules.md`
- `../../resources/rules/ai-agent-core.yaml`
- `../../resources/knowledge/manifest.yaml`

Load the project's profile, constraints, and critical flows. Use `project-architecture-audit` as well when the request covers the whole product rather than only AI-specific boundaries.

## Workflow

1. Ensure `.architecture/repository-facts.yaml` exists by running
   `architecture_tool.py inspect-repository`; never infer a risk directly from
   a detected framework or dependency.
2. Run `architecture_tool.py select-knowledge` with
   `--skill ai-agent-architecture-audit`, the exact task, repository facts, and
   Profile. Persist the full lock as
   `.architecture/knowledge-selection-ai-agent.yaml` and pass
   `--context-output .architecture/knowledge-context-ai-agent.yaml`. Read only
   the compact context index and every Markdown path it selects; reserve the
   full exclusion ledger for scripts, Reviews, and Gates. Do not load unrelated
   packs.
3. Draw the control path from user intent through orchestration, model calls, retrieval, tools, persisted state, human approval, and side effects.
4. Separate deterministic services and policy enforcement from model judgment.
5. Identify trust boundaries for user content, retrieved content, prompts, tools, credentials, memory, and model providers.
6. Trace context and memory lifecycles: creation, scoping, provenance, retention, mutation, retrieval, deletion, and recovery.
7. Trace long-running task state, idempotency, retries, cancellation, checkpoints, resumption, and duplicate side effects.
8. Inspect model routing, timeouts, fallbacks, degraded modes, cost budgets, latency budgets, and failure visibility.
9. Inspect evidence capture, source attribution, evaluation coverage, production feedback, and human confirmation boundaries.
10. Assess every applicable AI rule and record explicit `not_applicable` or `not_assessed` states.

For each finding, prove the complete failure path. A prompt containing untrusted text is not by itself a prompt-injection vulnerability; show how it can cross a policy or tool boundary.

## Verification handoff and output

Apply the candidate evidence requirements in `review-contract.md`. Leave every
finding at `verification.status: candidate`.

Write persistent artifacts under `.architecture/reviews/` using kind `ai-agent`:

- `<timestamp>-ai-agent-candidates.yaml`;

Start machine-readable output from `../../resources/templates/review.yaml` and set `review.kind` to `ai-agent`.

Use Review schema 1.2. Bind the exact repository-facts and AI knowledge
selection paths and hashes, preserve fact/inference boundaries, enumerate
critical-flow coverage, and validate with:

```bash
python3 ../../resources/scripts/architecture_tool.py validate-review \
  <review.yaml> --project <repo>
python3 ../../resources/scripts/architecture_tool.py validate-coverage \
  --project <repo> --review <review.yaml> --allow-candidates
```

Hand off architecture, candidate strengths and risks, critical-flow impact,
coverage, counter-evidence, and limitations. Use
`$architecture-finding-verifier` for confirmed conclusions and the final
report. Do not prescribe fixes.
