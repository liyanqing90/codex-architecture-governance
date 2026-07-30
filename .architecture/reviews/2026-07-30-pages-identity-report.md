# Hengmu canonical repository identity verification

## Outcome

The repository identity correction at
`ab99fcfe39f6d2c31351a1c37ef656a8341fee4f` is ready for hosted verification.
The candidate audit and independent verification found no unresolved
architecture risk across 31 rules, six critical flows, and nine selected
Knowledge entries.

## Failure diagnosed

The first PR run checked out `https://github.com/qingye-lab/hengmu`, while the
runtime manifest still declared `https://github.com/liyanqing90/hengmu`.
Selector replay correctly failed the mismatch in every test-matrix job. Local
checks had previously used the legacy redirecting origin and therefore did not
exercise the canonical GitHub checkout identity.

## Correction

- `qingye-lab/hengmu` is now the current authority in the plugin manifest,
  selector Runtime Manifest, documentation, release verification, SBOM
  expectation, installation instructions, and website links.
- The original project URL and intermediate personal Hengmu URL normalize only
  to the current repository. Unrelated origins continue to fail closed.
- The archived selector source commit remains unchanged and reachable through
  Git history; no historical Review or commit was rewritten.
- The plugin homepage and public website URL now identify the Pages endpoint,
  while the repository field remains the canonical source repository.

## Verification

- Focused repository-rename, selector replay, site-contract, and repository
  contract tests passed.
- Repository validation, Ruff lint, Ruff formatting, Knowledge Selection, exact
  compact Context projection, candidate Review, verified Review, and coverage
  validation passed.
- The negative identity test still rejects an unrelated repository.
- The full cross-platform result remains a hosted CI fact and must be observed
  after the evidence commit is pushed.

## External completion boundary

After hosted CI passes, merge the PR with a merge commit, enable workflow-based
GitHub Pages, dispatch the Pages workflow when necessary, verify the HTTPS
endpoint at desktop and mobile sizes, and only then set the repository
homepage.
