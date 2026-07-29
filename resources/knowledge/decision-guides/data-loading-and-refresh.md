---
id: decision.data-loading-and-refresh
kind: decision-guide
version: 2.0.0
status: active
domains:
- frontend
- backend-api
triggers:
- prefetch
- refresh
- stale
quality_attributes:
- maintainability
related:
- decision.cache-strategy
- decision.optimistic-vs-pessimistic-update
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: MDN HTTP caching
  url: https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching
  authority: official
  supports:
  - CACHE-FRESHNESS
- title: MDN Fetch API
  url: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
  authority: official
  supports:
  - LOAD-BOUNDARY
maturity: golden
curation:
  method: assisted-reviewed
  reviewer: Codex Architecture Governance review
  reviewed_at: '2026-07-28'
---

# Data Loading and Refresh

## Problem and intent

Choose when a client obtains data, what may be reused, and how freshness is restored without hiding stale or contradictory state from the user.

## Mechanism

Separate initial load, revalidation, and mutation. Give every cached result a freshness rule and an owner; cancel or supersede obsolete requests, and merge a response only when its resource key and request generation still match.

## Options

### Load on demand

- Fit: Cold or infrequent views where latency is acceptable.
- Avoid: Navigation must feel instant or the data is predictably needed.
- Cost: Visible loading latency and repeated origin work.
- Failure: Request waterfalls or empty states become the normal experience.
### Prefetch then revalidate

- Fit: Likely navigation and bounded, cacheable read models.
- Avoid: Data is sensitive, expensive, or unlikely to be consumed.
- Cost: Extra bandwidth, cache bookkeeping, and possible unused work.
- Failure: Unbounded prefetch amplifies load and returns stale snapshots.
### Push invalidation plus pull refresh

- Fit: Active clients need fast awareness but the server remains authoritative.
- Avoid: Clients cannot maintain subscriptions or tolerate reconnect logic.
- Cost: Subscription infrastructure and replay/version semantics.
- Failure: Missed invalidations leave a client stale unless reconnect triggers a full check.

## Fit when

At least one named option fits a measured quality scenario and the team can own its
required failure and recovery behavior.

## Avoid when

The choice is driven only by a technology name, hypothetical scale, or a problem
already solved by the current design.

## Required capabilities

Stable resource keys, freshness budgets, cancellation, version-aware merge rules, loading/error UI, and request/cache telemetry.

## Benefits

Makes perceived latency and staleness explicit while preventing late responses from overwriting newer client state.

## Costs and liabilities

More client states and network policy must be tested; prefetch and revalidation can increase origin traffic.

## Failure modes

Race between navigations, cache keys omitting tenant or authorization scope, retry storms, and background refresh silently replacing user edits.

## Alternatives

Compare the current design and the named options—Load on demand, Prefetch then revalidate, Push invalidation plus pull refresh—against the same
quality scenarios; do not compare feature lists without operating consequences.

## Migration and exit

Instrument the current load path, introduce one resource-keyed loader, add revalidation to a single high-value view, and retain a forced-refresh escape hatch until stale-rate and origin-load targets hold.

## Evidence to inspect

Navigation traces, request waterfalls, cache hit/stale rates, resource-key construction, abort handling, authorization scope, and tests for out-of-order responses.

## Evidence that changes the recommendation

Prefer on-demand loading when prefetch hit rate is low; prefer push invalidation only when measured freshness targets cannot be met by bounded revalidation.

## Quality trade-offs

Prefetch improves latency at bandwidth cost; revalidation improves freshness at origin-load cost; push improves timeliness at connection and recovery cost.

## Claim map

- LOAD-BOUNDARY: Initial loading, reuse, and revalidation are separate lifecycle decisions.
- CACHE-FRESHNESS: HTTP caches require explicit freshness and validation semantics.

## Volatile facts

Product versions, protocol/library support, service limits, pricing, licensing, and
security advisories must be rechecked in the cited official sources at decision time.
The mechanisms and decision criteria above are maintained separately from those facts.
