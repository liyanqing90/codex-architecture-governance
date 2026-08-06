---
name: hengmu
description: Unified public entry point for Hengmu. Use when the user invokes $hengmu, cannot remember a focused Hengmu Skill name, asks what Hengmu can do, wants a read-only lifecycle or status explanation, or wants Hengmu to route a natural-language request for repository, AI-agent, mobile, or portfolio audit, finding verification, emerging technology-evolution assessment, solution comparison, remediation planning, or a deterministic quality gate.
---

# Use Hengmu

Act as the stable navigation layer for Hengmu. Let users remember `$hengmu`
instead of eight focused Skill names. Route the request; never reimplement a
focused workflow here.

## Accept three forms

1. Accept a command, such as `$hengmu audit this repository`.
2. Accept natural language, such as `$hengmu 核实最新审核中的问题` or
   `$hengmu compare the queue and durable-workflow options`.
3. When the invocation contains no task, show the capability menu and recommend
   likely next actions from declared repository context. Do not start a workflow
   merely because the user opened the menu.

The user never needs to know the routed Skill name. Mention it briefly when
routing so the authority boundary remains visible.

## Route the request

| Intent or command | Read and follow this Skill |
| --- | --- |
| `audit`, `project`, repository/system assessment | `../project-architecture-audit/SKILL.md` |
| `ai`, AI-agent runtime, Context, Memory, tools, recovery, evaluation | `../ai-agent-architecture-audit/SKILL.md` |
| `mobile`, iOS/client state, offline sync, notifications, migrations | `../mobile-architecture-audit/SKILL.md` |
| `portfolio`, multiple projects, shared capability, stack sprawl, coupling | `../portfolio-architecture-audit/SKILL.md` |
| `verify`, challenge or confirm candidate findings | `../architecture-finding-verifier/SKILL.md` |
| `decide`, `evolve`, `upgrade`, `replace`, or compare architecture, pattern, technology, or keep-current options | `../architecture-solution-advisor/SKILL.md` |
| `plan`, turn an accepted decision into a safe migration | `../architecture-remediation-planner/SKILL.md` |
| `gate`, apply contract, finding, change, or release policy | `../architecture-quality-gate/SKILL.md` |
| `status`, `lifecycle`, `next`, or “what should I do next?” | Use the read-only lifecycle/status navigation below; do not start a workflow without an explicit request. |

Treat Chinese and English intent as equivalent. Prefer an explicit command when
present. Otherwise infer the narrowest matching intent from the user's desired
outcome, subject count, artifacts, and lifecycle stage. Ask one short question
only when two routes would materially change the work.

Before acting, read the routed `SKILL.md` completely and follow every resource,
evidence, authorization, persistence, and verification instruction it requires.
Pass all text after `$hengmu` through as the user's request. Once routed, the
focused Skill owns the task and this entry point adds no competing procedure.

## Read-only lifecycle and status navigation

For a status or next-step request, inspect only existing, schema-valid project
artifacts under `.architecture/` or `.architecture-portfolio/`. Report the
declared state, source artifact, freshness or validation ambiguity, and the
owning focused Skill that is valid next. Do not infer a state from a filename,
trend, timestamp, prose-only report, or missing artifact. An invalid or
contradictory artifact is an unrouteable state; report the ambiguity and name
the focused workflow that can resolve it.

Use this map as navigation, not as a lifecycle engine:

| Existing declared state | Explain as the valid next handoff |
| --- | --- |
| No usable Profile or no candidate Review | `project-architecture-audit` to establish repository-scoped evidence |
| Candidate Review, `verification_state: candidates`, or candidate findings | `architecture-finding-verifier` to independently verify the Review |
| Verified Review with confirmed unresolved findings | `architecture-solution-advisor` to compare a solution, including technology evolution when explicitly requested |
| Verified Review with no confirmed unresolved findings | No solution or remediation handoff is implied; explain that the declared Review supplies no confirmed problem for those workflows |
| Decision `status: proposed` | An authorized decision maker must accept, reject, or supersede it; the router cannot perform that authority transition |
| Decision `status: accepted` | `architecture-remediation-planner` may turn the accepted decision into a migration plan |
| Remediation Plan `draft`, `accepted`, or `in-progress` | The remediation planner owns plan work; implementation is not implied by router status |
| Remediation Plan `complete`, or an explicit gate request | `architecture-quality-gate` is a possible next workflow only when the user explicitly requests it |
| Decision or Plan `rejected`/`superseded`, or no compatible source chain | Explain the terminal or stale chain and request the focused workflow that creates a new valid source; do not silently restart one |

The router may summarize that an artifact declares `candidate`, `confirmed`,
`proposed`, `accepted`, `in-progress`, `complete`, `rejected`, or `superseded`.
It must not verify findings, make audit conclusions, merge audit and decision
authority, accept a decision or plan, mutate state, create artifacts, or invoke
any focused Skill or gate implicitly. A status projection is not an audit
conclusion and a next-step hint is not authorization.

## Show the menu

For an invocation containing only `$hengmu` or a request such as “what can you
do?”, respond with a compact menu like this:

```text
Hengmu
  audit      审查一个仓库
  ai         审查 AI / Agent 系统
  mobile     审查移动端系统
  portfolio  审查多个项目及共享能力
  verify     核实候选问题
  decide     比较架构、技术与实施方案
  evolve     评估新兴升级或替代价值
  status     查看只读生命周期与下一步
  plan       规划已接受方案的改造路径
  gate       运行确定性质量门禁

直接描述目标即可，例如：$hengmu 帮我比较这两个技术方案
```

If a repository is available, read `.architecture/profile.yaml` when it exists
and use only declared `type`, `critical_qualities`, and `required_reviews` to
mark up to three menu items as recommended. If the Profile is absent, use only
obvious repository facts to suggest `audit`; do not infer specialist scope from
a directory name or one dependency. Do not create `.architecture/` while only
showing the menu.

## Preserve workflow boundaries

- Keep all eight focused Skill names directly invocable for compatibility.
- Keep audit findings candidate-only until the verifier confirms them.
- Do not turn verification into solution selection or implementation.
- Require decision-driving evidence before solution selection.
- Require an accepted decision before remediation planning.
- Let only trusted, schema-valid artifacts reach the deterministic gate.
- Do not use the router to bypass a focused Skill's stop condition.

If the user explicitly invokes a focused Skill instead of `$hengmu`, do not
activate this router or redirect them unnecessarily.
