# Hengmu public identity reset review

## Outcome

The identity reset is ready for publication and the authorized GitHub
repository rename. The verified project review covers all 31 rules from the
project, plugin-platform, and test-automation Rule Packs, traces all six
critical flows, and contains no unresolved architecture finding.

The public repository, installable plugin, archive, SBOM, release workflow,
documentation, active project Profile, and gate maintainer identity use
Hengmu/Qingye. Pre-rename Reviews, Decisions, Selections, and Git commits remain
unchanged. Exact repository URL and project identity aliases keep those frozen
artifacts verifiable without making unrelated identities equivalent.

## Decision

`ADR-HENGMU-001` accepts the already implemented unified Hengmu identity.

- Keep the implemented Hengmu identity: selected.
- Preserve the former machine identity behind the Hengmu display brand:
  rejected because there are no users to protect and it creates permanent
  naming debt.
- Rewrite history and historical artifacts: eliminated because it destroys
  hashes, commit references, and evidence provenance.

## Verification evidence

- Repository validation: 8 public Skills, 40 eval cases, 28 schemas, and 20
  templates.
- Architecture coverage: 31 rules, 6 critical flows, and 11 selected Knowledge
  entries.
- Test suite: 97 tests passed under Python 3.13 and pytest 9.1.1.
- Ruff lint and formatting: passed for 330 files.
- Project, History Anchor, Knowledge Context, Review, coverage, accepted
  Decision, and Knowledge validation: passed.
- Runtime and development dependency audits: no known vulnerabilities.
- Runtime dependency license audit: passed.
- Deterministic package: `hengmu-0.4.2.zip`, 330 entries, SHA-256
  `11400efa20c9cdf2eae10c4498b6001d1d71696afbff32999be7b50a64bee690`.
- SPDX package, document namespace, and creator use `hengmu`, the new GitHub
  repository URL, and `hengmu-sbom-0.4.2`.

The dependency audit initially identified `PYSEC-2026-1845` in the development
test runner `pytest` 8.4.2. The development range now starts at 9.0.3, the
hash-locked environment resolves to 9.1.1, and both installed-environment and
lock-file audits pass.

## External completion boundary

The code-bound Review does not claim that an external action has already
happened. After this governance chain is committed:

1. run the clean-tree architecture change gate;
2. push `agent/hengmu-brand-readme`;
3. rename `liyanqing90/codex-architecture-governance` to
   `liyanqing90/hengmu`;
4. update local `origin`;
5. verify the branch SHA, old URL redirect, and hosted CI.

## Residual limitations

- The no-historical-users premise is an explicit owner constraint, not a fact
  inferred from source code.
- GitHub redirect and hosted CI behavior remain unobserved until the external
  rename and push complete.
- Frozen internal evidence still contains the former identity by design; it is
  not a current installation or release surface.
