# Publish the Hengmu website with GitHub Pages

- Status: Accepted
- Date: 2026-07-30
- Owners: Hengmu maintainers
- Scope: Public project website and deployment workflow

## Context

Hengmu needs a public entry point that explains the project as a software
decision system rather than reducing it to architecture review. The website
must present system assessment, technical solution comparison, specialized
review, and decision governance in both English and Simplified Chinese.

The repository already contains the approved Hengmu and Qingye brand assets.
The plugin itself remains a local Python and Codex Skill distribution with no
hosted runtime. A website must not add runtime dependencies to the plugin
package or weaken the repository's deterministic validation and supply-chain
controls.

## Decision

Publish a static, dependency-free website through GitHub Pages using a pinned
GitHub Actions workflow:

- keep the entry document at `index.html` and implementation assets under
  `site/`;
- reuse repository-owned Qingye and Hengmu assets instead of loading third-party
  fonts, scripts, analytics, or image hosts;
- keep English and Simplified Chinese copy in one validated locale contract;
- assemble an explicit Pages artifact whose contents are separate from the
  plugin release allowlist;
- require existing repository validation and dedicated site contract tests
  before merge;
- deploy only from `main`, with GitHub Pages' protected deployment environment
  and OIDC identity.

## Alternatives considered

### README-only documentation

This keeps maintenance small but does not provide a focused project narrative,
responsive presentation, or discoverable public URL.

### A framework-based application

Astro, Next.js, or another framework could provide more composition features,
but would add a JavaScript dependency graph, update burden, and build surface
that the current site does not need.

### A hosted site outside GitHub

An external host could offer more infrastructure options, but would introduce
another account, deployment boundary, and operational dependency without a
current product requirement.

## Consequences

- The site is fast, inspectable, and deployable without a package-manager
  install.
- Its visual vocabulary stays aligned with the Qingye brand assets already
  reviewed in this repository.
- Locale parity, local asset references, production URLs, safe DOM usage, and
  pinned workflow actions are enforced by repository validation.
- GitHub Pages becomes an operational dependency for the public website, while
  the Hengmu plugin remains fully usable if the website is unavailable.
- Rich application behavior or content management would require revisiting this
  decision instead of gradually turning the static site into an implicit app.

## Verification

- Run `python3 scripts/validate_repository.py`.
- Run `python3 -m pytest`.
- Render the assembled artifact at desktop and mobile widths.
- Exercise both locales, navigation, and the copy interaction.
- Confirm the Pages workflow completes on `main` and the production URL serves
  the merged commit over HTTPS.

## Rollback

Revert the merge commit that introduced or changed the site, then let the Pages
workflow redeploy the previous artifact. If the public endpoint itself must be
removed, disable GitHub Pages in repository settings. Neither action changes
the plugin release artifact or its runtime behavior.

## Revisit when

- the website needs authenticated or stateful behavior;
- content ownership requires a CMS;
- localization expands beyond the current two-locale contract;
- GitHub Pages no longer satisfies availability, policy, or deployment needs.
