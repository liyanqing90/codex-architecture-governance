# AI-agent architecture rule set

Assess these rules in addition to applicable project rules.

| Rule ID | Domain | Invariant to inspect |
|---|---|---|
| `AI.BOUNDARY.001` | Agent boundary | Model judgment is used only where probabilistic behavior is acceptable; deterministic policy and business rules remain authoritative. |
| `AI.CONTEXT.001` | Context lifecycle | Context has explicit sources, scope, size limits, freshness, redaction, and disposal. |
| `AI.CONTEXT.002` | Context source inventory | Every assembled source has an owner, purpose, necessity, authority, scope, freshness, sensitivity, transformation, retention, and disposal decision. |
| `AI.CONTEXT.003` | Context budget integrity | Budgeting and compression preserve authority, provenance, and required recency, or fail closed with an explicit loss record. |
| `AI.CONTEXT.004` | Context ordering and cache | Ordering and cache reuse are stable, scoped, observable, and invalidated when authorization, provenance, or relevant content changes. |
| `AI.CONTEXT.005` | Stable and volatile context | Stable policy, contracts, and instructions are separated from volatile user, retrieval, task-state, and provider context. |
| `AI.MEMORY.001` | Memory tiers | Working, episodic, semantic, and durable records have distinct ownership, retention, update, and retrieval semantics. |
| `AI.MEMORY.002` | Memory isolation | User, tenant, task, and agent memories cannot leak across scopes. |
| `AI.PROVENANCE.001` | Evidence | Claims and durable memories preserve source, time, transformation, confidence, and contradiction history. |
| `AI.TOOL.001` | Tool authorization | Tool access is allowlisted by identity, task, scope, arguments, and side-effect class. |
| `AI.TOOL.002` | Side-effect boundary | Important or irreversible actions require deterministic validation and the declared human confirmation. |
| `AI.INJECTION.001` | Prompt injection | Untrusted instructions cannot override system policy, obtain credentials, or expand tool authority. |
| `AI.SECRET.001` | Secret handling | Prompts, traces, model providers, retrieval stores, and tool outputs do not expose unnecessary secrets or personal data. |
| `AI.PRIVACY.001` | Data minimization | Sensitive and personal data is minimized by purpose, field, scope, retention, and representation across prompts, retrieval, memory, and traces. |
| `AI.STATE.001` | Long tasks | Plans and workflows have durable state, checkpoints, cancellation, resumption, and terminal outcomes. |
| `AI.IDEMPOTENCY.001` | Repeated actions | Model retries and resumed tasks cannot duplicate external side effects. |
| `AI.MODEL.001` | Routing | Model selection, capability assumptions, versions, timeouts, and fallbacks are explicit and observable. |
| `AI.DEGRADE.001` | Degraded mode | Provider failure, rate limits, context overflow, and low confidence have safe product behavior. |
| `AI.EVAL.001` | Evaluation | Critical capabilities have representative offline evaluations and production signals tied to release decisions. |
| `AI.EVAL.002` | Behavior evidence | Behavior evidence is bound to exact model/runtime, prompt, tool, retriever, context, evaluation-data, environment, and time versions or hashes. |
| `AI.HUMAN.001` | Human oversight | Approval points are placed at actual risk boundaries and show evidence, scope, and consequences. |
| `AI.COST.001` | Cost/latency | Token, tool, retrieval, and retry budgets are bounded per task and visible operationally. |
| `AI.OBSERVABILITY.001` | Traceability | A task can be reconstructed across prompts, models, retrieval, tools, state transitions, and approvals without leaking sensitive content. |
| `AI.RECOVERY.001` | Recovery | Partial model/tool failure has explicit retry ownership, compensation, and escalation. |
| `AI.MULTIAGENT.001` | Coordination | Multiple agents have clear ownership, handoff contracts, conflict handling, and bounded shared state. |
| `AI.CHANGE.001` | Prompt/model evolution | Prompt, model, tool, retrieval, and policy changes are versioned and evaluated before rollout. |
| `AI.CHANGE.002` | Upgrade decisions | New or upgraded agent runtimes, protocols, models, and frameworks are adopted, retained, or rejected from evidence against a current baseline and critical-flow requirements. |

## Proof requirements

- For injection or permission findings, trace untrusted input to an authority-expanding or side-effecting sink.
- For memory leakage, identify the scope key, retrieval filter, writer, and reader.
- For recovery, identify durable state and demonstrate what happens after termination between two steps.
- For evaluation gaps, tie the missing coverage to a declared critical capability; “no benchmark” alone is not a high-severity finding.
- For context assembly, inventory every source and prove necessity; inspect authority, scope, sensitivity, freshness, transformation, retention, and disposal rather than treating a source list as sufficient.
- For context budgets, trace truncation, summarization, ranking, and fallback and verify that authority, provenance, and recency survive or that the system fails closed and records the loss.
- For ordering and caches, compare stable ordering and cache keys across retries, tasks, tenants, and releases; treat ordering changes as cache and evidence-boundary changes.
- For stable-versus-volatile context, classify policy and contracts separately from user, retrieval, task-state, and provider data and inspect reusable-cache boundaries.
- For data minimization, inspect field-level allowlists, redaction, purpose, scope, retention, deletion, and reference-versus-raw-content representation independently for prompts, retrieval, memory, and traces.
- For behavior evidence, require exact model/runtime, prompt, tool schema and policy, retriever/index/ranking, context treatment, evaluation data, environment, timestamp, and hashes where available; reject incomparable aggregate results.
- For upgrades, compare adopt, retain, and reject options against the current baseline with critical-flow evidence for quality, compatibility, security, operations, cost, ownership, rollout, and rollback. Record named technologies only as versioned evidence, never as the finding itself.
- Treat model-provider features and framework defaults as claims to verify, not controls to assume.

Every candidate strength or risk must identify at least one concrete affected
critical flow and a complete trigger-to-impact or control-to-outcome path.
Technology names are evidence labels only; findings must state the violated or
protected architecture invariant.
