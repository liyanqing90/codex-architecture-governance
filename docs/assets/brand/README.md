# Hengmu visual assets

Hengmu is a Qingye open-source project. This directory contains the
repository-ready visual system used by both README editions.

## Asset matrix

| Asset | English | 简体中文 | Formats |
| --- | --- | --- | --- |
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
- Brand idea: 理性结构中的持续进化
- Brand proposition: 在不确定中，持续构建。
- Qingye ink: `#161719`
- Qingye blue: `#173FBE`
- Warm white: `#F4F2EC`
- Neutral gray: `#6D7078`
- Hairline: `#D9D9D2`

`qingye-wordmark.svg` is the unmodified official wordmark source. Do not
redraw, rotate, restack, or alter its paths.

## Hengmu mark

The Hengmu icon combines four ideas:

1. a blue measuring beam for explicit architectural judgment;
2. black end marks for scope and constraints;
3. a dark fulcrum for trade-offs;
4. an open center joint for evidence-driven change.

Its visual philosophy is documented in
[`design-philosophy.md`](design-philosophy.md). The SVG files are the
editable sources; PNG files are deterministic rendered exports.

## Qingye character

`source/qingye-character-reference.png` is the character anchor used in the
README illustrations. It derives only from the public Qingye avatar:
slightly wavy short hair, a forward-looking posture, a high-collar
Qingye-blue work jacket, and a restrained path motif. It does not claim to
reconstruct undisclosed facial identity.

The character is original to Qingye. The illustration workflow and
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
Qingye name or wordmark to imply endorsement is not granted.
