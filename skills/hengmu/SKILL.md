---
name: hengmu
description: Unified public entry point for Hengmu. Use when the user invokes $hengmu, cannot remember a focused Hengmu Skill name, asks what Hengmu can do, or wants Hengmu to route a natural-language request for repository, AI-agent, mobile, or portfolio audit, finding verification, solution comparison, remediation planning, or a deterministic quality gate.
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
| `decide`, compare architecture, pattern, technology, or keep-current options | `../architecture-solution-advisor/SKILL.md` |
| `plan`, turn an accepted decision into a safe migration | `../architecture-remediation-planner/SKILL.md` |
| `gate`, apply contract, finding, change, or release policy | `../architecture-quality-gate/SKILL.md` |

Treat Chinese and English intent as equivalent. Prefer an explicit command when
present. Otherwise infer the narrowest matching intent from the user's desired
outcome, subject count, artifacts, and lifecycle stage. Ask one short question
only when two routes would materially change the work.

Before acting, read the routed `SKILL.md` completely and follow every resource,
evidence, authorization, persistence, and verification instruction it requires.
Pass all text after `$hengmu` through as the user's request. Once routed, the
focused Skill owns the task and this entry point adds no competing procedure.

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
