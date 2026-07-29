---
id: decision.polling-vs-sse-vs-websocket
kind: decision-guide
version: 2.0.0
status: active
domains:
- frontend
- backend-api
- real-time
triggers:
- polling
- sse
- websocket
quality_attributes:
- maintainability
related:
- decision.data-loading-and-refresh
- decision.message-system-selection
last_reviewed: '2026-07-28'
review_after_days: 365
source_policy: stable-principles-plus-official-docs
sources:
- title: MDN Server-sent events
  url: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
  authority: official
  supports:
  - SSE-DIRECTION
- title: MDN WebSocket API
  url: https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API
  authority: official
  supports:
  - WS-DUPLEX
maturity: golden
curation:
  method: assisted-reviewed
  reviewer: Codex Architecture Governance review
  reviewed_at: '2026-07-28'
---

# Polling vs SSE vs WebSocket

## Problem and intent

Select an update channel from direction, freshness, connection count, recovery, proxy behavior, and interaction semantics.

## Mechanism

Keep the durable state behind a normal resource contract. The live channel carries versions or event IDs; reconnect either resumes from a cursor or performs a full resource refresh.

## Options

### Bounded polling

- Fit: Updates are infrequent and seconds-to-minutes freshness is enough.
- Avoid: Request volume or freshness makes repeated empty responses unaffordable.
- Cost: Repeated requests and synchronized-client spikes.
- Failure: Fixed intervals overload the origin or miss required freshness.
### Server-Sent Events

- Fit: Browser clients need ordered, server-to-client text events over HTTP.
- Avoid: Binary data or client-to-server streaming is central.
- Cost: Long-lived connections, heartbeat, cursor, and proxy tuning.
- Failure: Reconnect without a replay cursor loses updates or duplicates side effects.
### WebSocket

- Fit: Low-latency bidirectional messages are a product requirement.
- Avoid: Ordinary HTTP requests or one-way push satisfy the flow.
- Cost: Connection state, backpressure, authentication refresh, and fleet fan-out.
- Failure: Slow consumers exhaust buffers or connection routing loses session state.

## Fit when

At least one named option fits a measured quality scenario and the team can own its
required failure and recovery behavior.

## Avoid when

The choice is driven only by a technology name, hypothetical scale, or a problem
already solved by the current design.

## Required capabilities

Measured freshness, connection budget, authentication renewal, heartbeat, backoff with jitter, replay or resync, backpressure, and connection/event metrics.

## Benefits

Matches transport complexity to the actual direction and latency requirement rather than to a vague real-time label.

## Costs and liabilities

Moving from polling to a persistent channel adds stateful operations and recovery behavior.

## Failure modes

Reconnect storms, missed cursors, duplicate event application, proxy idle timeouts, slow consumers, and authorization changes not reaching an open connection.

## Alternatives

Compare the current design and the named options—Bounded polling, Server-Sent Events, WebSocket—against the same
quality scenarios; do not compare feature lists without operating consequences.

## Migration and exit

Start with bounded polling and ETags when sufficient; add SSE for one-way freshness or WebSocket for proven two-way needs, keeping a full-refresh endpoint as the recovery authority.

## Evidence to inspect

Update frequency, tolerated staleness, concurrent-client forecast, message direction and size, proxy/load-balancer limits, reconnect traces, and event idempotency tests.

## Evidence that changes the recommendation

A one-way flow favors SSE over WebSocket; low change frequency favors polling; binary or interactive bidirectional traffic can justify WebSocket.

## Quality trade-offs

Lower latency costs persistent connections, recovery machinery, and more complex capacity planning.

## Claim map

- SSE-DIRECTION: SSE provides server-to-client event delivery through EventSource.
- WS-DUPLEX: WebSocket provides a two-way interactive session.

## Volatile facts

Product versions, protocol/library support, service limits, pricing, licensing, and
security advisories must be rechecked in the cited official sources at decision time.
The mechanisms and decision criteria above are maintained separately from those facts.
