# Hengmu visual assets

Hengmu is a 青野 open-source project for evidence-bound software engineering
decisions: system assessment, finding verification, technical solution
comparison, remediation planning, and deterministic governance. Architecture
is the connecting system view, not the project's only capability. This
directory contains the repository-ready visual system used by both README
editions.

## Asset matrix

| Asset | English | 简体中文 | Formats |
| --- | --- | --- | --- |
| 青野 primary logo | `qingye-logo-primary.png` | `qingye-logo-primary.png` | PNG |
| Project icon | `en/hengmu-icon.*` | `zh-CN/hengmu-icon.*` | SVG, PNG |
| Project banner | `en/hengmu-banner.*` | `zh-CN/hengmu-banner.*` | SVG, PNG |
| README editorial figures | `../../../assets/hengmu-readme-illustrations/en/` | `../../../assets/hengmu-readme-illustrations/zh-CN/` | PNG |
| Governance flow | `../../../diagrams/en/` | `../../../diagrams/zh-CN/` | Mermaid, Excalidraw, SVG, PNG |

The two icon files deliberately use the same language-neutral geometry while
carrying localized SVG titles and descriptions. Banners, editorial figures,
and diagrams localize all visible text.

## Brand source

- Source of truth: `liyanqing90/qingye-brand`
- Asset baseline: `v1.1 Refined`
- Logo source: `exports/social/avatar/qingye-avatar-primary-1024.png`
- Logo SHA-256: `1ac86268c87d0eb618d198218438c7e4f05d16c443fc9517393d0929897cfefc`
- Brand idea: 理性结构中的持续进化
- Brand proposition: 在不确定中，持续构建。
- 青野 ink: `#161719`
- 青野 blue: `#173FBE`
- Warm white: `#F4F2EC`
- Neutral gray: `#6D7078`
- Hairline: `#D9D9D2`

`qingye-wordmark.svg` is the unmodified official wordmark source.
`qingye-logo-primary.png` is the brand repository's Final 1024 px
warm-paper, black-wordmark social logo. Both localized banners use that
published asset; they do not typeset a Latin-script substitute. Do not redraw,
rotate, restack, or alter the official wordmark.

## Hengmu mark

The Hengmu icon combines two written ideas in one structural mark:

1. the brand-blue horizontal member is the explicit measuring beam, `衡`;
2. the ink-black spine and load paths abstract the timber structure, `木`.

The mark is intentionally joinery rather than a literal scale, shield,
building, or architecture diagram.

Its visual philosophy is documented in
[`design-philosophy.md`](design-philosophy.md). The SVG files are the
editable sources; PNG files are deterministic rendered exports.

## 青野 character

`source/qingye-character-reference.png` is the character anchor used in the
README illustrations. It derives only from the public 青野 avatar:
slightly wavy short hair, a forward-looking posture, a high-collar
brand-blue work jacket, and a restrained path motif. It does not claim to
reconstruct undisclosed facial identity.

The character is original to 青野. The illustration workflow and
hand-drawn editorial discipline were produced with the Ian Xiaohei
Illustrations Skill; Xiaohei itself is not used as Hengmu's public character.

## Usage

- Use `hengmu-icon.png` for square repository, release, or package surfaces.
- Use `hengmu-banner.png` for GitHub social preview and announcement covers.
- Prefer the locale matching the surrounding copy.
- Do not recolor individual elements, add gradients, or place the mark on a
  low-contrast photographic background.
- Preserve at least one-quarter of the icon width as clear space.

The software is licensed under the repository's MIT License. Use of the
青野 name or wordmark to imply endorsement is not granted.
