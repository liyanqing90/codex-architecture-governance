# AI-agent architecture rule set

Assess these rules in addition to applicable project rules.

| Rule ID | Domain | Invariant to inspect |
|---|---|---|
| `AI.BOUNDARY.001` | Agent boundary | Model judgment is used only where probabilistic behavior is acceptable; deterministic policy and business rules remain authoritative. |
| `AI.CONTEXT.001` | Context lifecycle | Context has explicit sources, scope, size limits, freshness, redaction, and disposal. |
| `AI.MEMORY.001` | Memory tiers | Working, episodic, semantic, and durable records have distinct ownership, retention, update, and retrieval semantics. |
| `AI.MEMORY.002` | Memory isolation | User, tenant, task, and agent memories cannot leak across scopes. |
| `AI.PROVENANCE.001` | Evidence | Claims and durable memories preserve source, time, transformation, confidence, and contradiction history. |
| `AI.TOOL.001` | Tool authorization | Tool access is allowlisted by identity, task, scope, arguments, and side-effect class. |
| `AI.TOOL.002` | Side-effect boundary | Important or irreversible actions require deterministic validation and the declared human confirmation. |
| `AI.INJECTION.001` | Prompt injection | Untrusted instructions cannot override system policy, obtain credentials, or expand tool authority. |
| `AI.SECRET.001` | Secret handling | Prompts, traces, model providers, retrieval stores, and tool outputs do not expose unnecessary secrets or personal data. |
| `AI.STATE.001` | Long tasks | Plans and workflows have durable state, checkpoints, cancellation, resumption, and terminal outcomes. |
| `AI.IDEMPOTENCY.001` | Repeated actions | Model retries and resumed tasks cannot duplicate external side effects. |
| `AI.MODEL.001` | Routing | Model selection, capability assumptions, versions, timeouts, and fallbacks are explicit and observable. |
| `AI.DEGRADE.001` | Degraded mode | Provider failure, rate limits, context overflow, and low confidence have safe product behavior. |
| `AI.EVAL.001` | Evaluation | Critical capabilities have representative offline evaluations and production signals tied to release decisions. |
| `AI.HUMAN.001` | Human oversight | Approval points are placed at actual risk boundaries and show evidence, scope, and consequences. |
| `AI.COST.001` | Cost/latency | Token, tool, retrieval, and retry budgets are bounded per task and visible operationally. |
| `AI.OBSERVABILITY.001` | Traceability | A task can be reconstructed across prompts, models, retrieval, tools, state transitions, and approvals without leaking sensitive content. |
| `AI.RECOVERY.001` | Recovery | Partial model/tool failure has explicit retry ownership, compensation, and escalation. |
| `AI.MULTIAGENT.001` | Coordination | Multiple agents have clear ownership, handoff contracts, conflict handling, and bounded shared state. |
| `AI.CHANGE.001` | Prompt/model evolution | Prompt, model, tool, retrieval, and policy changes are versioned and evaluated before rollout. |

## Proof requirements

- For injection or permission findings, trace untrusted input to an authority-expanding or side-effecting sink.
- For memory leakage, identify the scope key, retrieval filter, writer, and reader.
- For recovery, identify durable state and demonstrate what happens after termination between two steps.
- For evaluation gaps, tie the missing coverage to a declared critical capability; “no benchmark” alone is not a high-severity finding.
- Treat model-provider features and framework defaults as claims to verify, not controls to assume.
