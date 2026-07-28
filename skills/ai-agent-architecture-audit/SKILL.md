---
name: ai-agent-architecture-audit
description: Specialized architecture audit for AI-agent systems and AI-enabled products. Use for agent runtimes, tool-using workflows, memory systems, RAG, MCP integrations, long-running tasks, model routing, evidence tracking, human approval, evaluations, or systems exposed to prompt injection and model uncertainty. Extends rather than replaces the general project architecture audit.
---

# Audit AI-agent architecture

Assess whether probabilistic model behavior is safely bounded by deterministic product and operational controls.

## Load the contract

Read these files completely:

- `../../resources/references/review-contract.md`
- `../../resources/references/ai-agent-rules.md`

Load the project's profile, constraints, and critical flows. Use `project-architecture-audit` as well when the request covers the whole product rather than only AI-specific boundaries.

## Workflow

1. Draw the control path from user intent through orchestration, model calls, retrieval, tools, persisted state, human approval, and side effects.
2. Separate deterministic services and policy enforcement from model judgment.
3. Identify trust boundaries for user content, retrieved content, prompts, tools, credentials, memory, and model providers.
4. Trace context and memory lifecycles: creation, scoping, provenance, retention, mutation, retrieval, deletion, and recovery.
5. Trace long-running task state, idempotency, retries, cancellation, checkpoints, resumption, and duplicate side effects.
6. Inspect model routing, timeouts, fallbacks, degraded modes, cost budgets, latency budgets, and failure visibility.
7. Inspect evidence capture, source attribution, evaluation coverage, production feedback, and human confirmation boundaries.
8. Assess every applicable AI rule and record explicit `not_applicable` or `not_assessed` states.

For each finding, prove the complete failure path. A prompt containing untrusted text is not by itself a prompt-injection vulnerability; show how it can cross a policy or tool boundary.

## Verification handoff and output

Apply the candidate evidence requirements in `review-contract.md`. Leave every
finding at `verification.status: candidate`.

Write persistent artifacts under `.architecture/reviews/` using kind `ai-agent`:

- `<timestamp>-ai-agent-candidates.yaml`;

Start machine-readable output from `../../resources/templates/review.yaml` and set `review.kind` to `ai-agent`.

Validate YAML with `architecture_tool.py validate-review`.

Hand off architecture, candidate strengths and risks, critical-flow impact,
coverage, counter-evidence, and limitations. Use
`$architecture-finding-verifier` for confirmed conclusions and the final
report. Do not prescribe fixes.
