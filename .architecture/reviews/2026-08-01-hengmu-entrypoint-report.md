# Hengmu stable entry review

- Reviewed implementation: `b283cabdbcbbbb8cc2e2c5d959ecce5a8434c629`
- Scope: additive `$hengmu` Skill, public routing contract, documentation,
  website discovery, evaluation coverage, and packaging inclusion
- Candidate review: `hengmu-20260801-entrypoint-candidates`
- Verified review: `hengmu-20260801-entrypoint-verified`
- Result: no confirmed architecture risks

## Architecture shape

`hengmu` is a discovery-only facade. It accepts a short command or natural
language, or shows a non-mutating menu when invoked without a task. Every route
points to exactly one of the eight existing workflow Skills, reads that Skill
completely, and then yields ownership to it. Audit, independent verification,
solution decision, remediation planning, and deterministic gate authority are
not implemented in the facade.

## Verified strengths

- Users need to remember only `$hengmu`; command names are optional.
- The router covers all eight workflows and preserves direct focused
  invocation for existing users and automation.
- Menu-only invocation cannot initialize `.architecture/` or start work.
- The router repeats the lifecycle stop conditions that prevent candidate
  findings from reaching decisions, plans, or gates without the required
  authority.
- Repository validation now requires 9 public Skills and 45 routing cases.
- Focused contract tests prove complete route coverage and direct-invocation
  bypass.
- English and Chinese README content and the Pages source expose the stable
  entry consistently.

## Verification evidence

- Official Skill validator: passed.
- Official plugin validator: passed.
- Repository contract validator: 9 Skills and 45 routing cases passed.
- Test suite: 105 tests and 4 subtests passed.
- Ruff lint and formatting: passed.
- Runtime dependency audit and license audit: passed.

## Limitations

Natural-language routing depends on the installed Codex surface and model. The
static cases prove the intended contract, not permanent runtime accuracy. A
post-install forward test remains required before release. The public Pages site
will change only after an authorized push and deployment.
