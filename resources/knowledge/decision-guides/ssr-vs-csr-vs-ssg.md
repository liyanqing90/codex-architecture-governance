---
id: decision.ssr-vs-csr-vs-ssg
kind: decision-guide
version: 2.0.0
status: active
domains:
- frontend
triggers:
- ssr
- csr
- ssg
quality_attributes:
- maintainability
related:
- decision.data-loading-and-refresh
- decision.state-management
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: Next.js automatic static optimization
  url: https://nextjs.org/docs/pages/building-your-application/rendering/automatic-static-optimization
  authority: official
  supports:
  - STATIC-RENDER
- title: Next.js server-side rendering
  url: https://nextjs.org/docs/pages/building-your-application/rendering/server-side-rendering
  authority: official
  supports:
  - SSR-REQUEST
- title: Next.js Server and Client Components
  url: https://nextjs.org/docs/app/getting-started/server-and-client-components
  authority: official
  supports:
  - CLIENT-BOUNDARY
maturity: golden
curation:
  method: assisted-reviewed
  reviewer: Codex Architecture Governance review
  reviewed_at: '2026-07-28'
---

# SSR vs CSR vs SSG

## Problem and intent

Choose where and when HTML is produced for each route from freshness, personalization, discoverability, interaction, security, and delivery cost.

## Mechanism

SSG renders at build or revalidation time, SSR renders per request, and CSR renders primarily in the browser after JavaScript and data arrive. A product may compose these at route or component boundaries.

## Options

### Static generation

- Fit: Content changes on a bounded cadence and fast cacheable delivery matters.
- Avoid: Per-request personalization or immediate freshness is mandatory.
- Cost: Build/revalidation pipelines and invalidation delay.
- Failure: Build duration or stale pages grow without bounds.
### Server-side rendering

- Fit: Request-specific or frequently changing content needs useful initial HTML.
- Avoid: Server cost and latency cannot meet traffic targets.
- Cost: Per-request compute, caching, and hydration complexity.
- Failure: Slow dependencies delay the whole response or leak user-scoped content through caches.
### Client-side rendering

- Fit: The view is highly interactive, authenticated, and initial indexing/HTML is secondary.
- Avoid: Low-end clients, discoverability, or first-content latency are critical.
- Cost: Larger JavaScript, client data waterfalls, and loading states.
- Failure: Blank shells, hydration/state bugs, or exposed browser-only trust decisions.

## Fit when

At least one named option fits a measured quality scenario and the team can own its
required failure and recovery behavior.

## Avoid when

The choice is driven only by a technology name, hypothetical scale, or a problem
already solved by the current design.

## Required capabilities

Route inventory, freshness and personalization matrix, cache keys, bundle and server budgets, loading/error behavior, hydration tests, and security boundaries.

## Benefits

Allows rendering to follow route needs instead of forcing a whole application into one mode.

## Costs and liabilities

Hybrid rendering adds mental models and cache rules; single-mode designs may waste server or client resources.

## Failure modes

Caching personalized SSR output, client waterfalls, rebuild bottlenecks, hydration mismatch, and moving authorization to the browser.

## Alternatives

Compare the current design and the named options—Static generation, Server-side rendering, Client-side rendering—against the same
quality scenarios; do not compare feature lists without operating consequences.

## Migration and exit

Classify routes, move one stable public page to static or one dynamic page to server rendering, measure user timing and server cost, then expand by route rather than by global rewrite.

## Evidence to inspect

Route freshness/personalization, web-vital traces, HTML usefulness without JavaScript, bundle size, server latency/cost, cache headers, and hydration errors.

## Evidence that changes the recommendation

Static is preferred for stable public content; SSR for request-dependent initial content; CSR for interaction-heavy private surfaces where client cost is acceptable.

## Quality trade-offs

Freshness, initial content, server spend, client work, cacheability, and implementation complexity trade at route level.

## Claim map

- STATIC-RENDER: Static generation can emit HTML ahead of requests.
- SSR-REQUEST: SSR generates HTML for each request.
- CLIENT-BOUNDARY: Client components are needed for browser APIs and interactive state.

## Volatile facts

Product versions, protocol/library support, service limits, pricing, licensing, and
security advisories must be rechecked in the cited official sources at decision time.
The mechanisms and decision criteria above are maintained separately from those facts.
