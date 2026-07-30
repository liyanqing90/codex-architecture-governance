# Hengmu GitHub Pages publication review

## Outcome

The Pages implementation at
`a778eb7640410d22afec8108cfa6fee7e0516224` is ready for merge and hosted
deployment. The candidate and independent verification passes produced no
architecture risk finding. Coverage includes all 31 rules from the project,
plugin-platform, and test-automation Rule Packs, all six declared critical
flows, and 12 selected Knowledge entries.

## Architecture shape

Hengmu now has two deliberately separate delivery surfaces:

- the installable local plugin, whose manifest and deterministic runtime
  allowlist remain authoritative; and
- a dependency-free static website, whose Pages workflow copies an explicit
  public asset inventory into a separate deployment artifact.

The website uses repository-owned Qingye and Hengmu assets, a validated
English/Simplified Chinese locale contract, local JavaScript without unsafe DOM
injection, and no third-party runtime, analytics, credential, or telemetry
dependency.

## Verified properties

- The Pages workflow uses commit-SHA-pinned actions and grants `pages: write`
  and `id-token: write` only to its deployment job.
- The assembled 4.7MB Pages artifact contains only the entry document, locale,
  styles, script, SEO files, illustrations, and approved brand assets; it
  contains no symlink.
- The plugin ZIP remains governed by its original runtime allowlist. It excludes
  the website, repository workflow, tests, and review evidence, and continues
  to pass checksum and SPDX generation.
- Repository validation checks local resource existence, locale parity,
  production canonical metadata, one local script, safe DOM primitives, action
  pinning, and the Pages artifact contract.
- Three site contract tests cover the valid path, a missing translation key,
  and an injected external script.
- Browser verification covered both locales, the localized image and quick
  start link, the copy feedback, mobile navigation, 1536px desktop rendering,
  390px mobile rendering, and horizontal overflow. No browser warning or error
  was observed.
- The accepted hosting decision records alternatives, consequences,
  verification, rollback, and conditions that would require a different
  hosting architecture.

## Repository verification

- Repository, project, History Anchor, Knowledge Selection, compact Context,
  Knowledge, Review, and coverage validation: passed.
- Test suite: 100 tests passed under Python 3.13 and pytest 9.1.1.
- Ruff lint and formatting: passed for 333 files.
- Runtime dependency audit: no known vulnerabilities.
- Runtime license audit: passed.
- Deterministic plugin package, SHA-256 checksum, and SPDX SBOM: passed.

## External completion boundary

The code-bound Review does not claim that GitHub Pages is already serving the
site. After this evidence commit is merged:

1. enable GitHub Pages with GitHub Actions as its source;
2. run the Pages workflow from `main`;
3. verify the protected deployment result and HTTPS endpoint;
4. confirm the production DOM, both languages, console, and mobile layout;
5. set the repository homepage to the verified Pages URL.

## Residual limitations

- GitHub Pages availability, environment protection, and HTTPS behavior remain
  unobserved until the authorized post-merge deployment.
- The site is a presentation surface, not an availability dependency of the
  Hengmu plugin. GitHub Pages downtime does not affect local plugin use.
