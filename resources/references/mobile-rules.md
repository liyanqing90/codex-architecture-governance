# Mobile architecture rule set

Assess these rules in addition to applicable project rules.

| Rule ID | Domain | Invariant to inspect |
|---|---|---|
| `MOBILE.STATE.001` | State ownership | Each user-visible state has one owner and a lifecycle appropriate to views, scenes, processes, and accounts. |
| `MOBILE.LOCAL.001` | Local persistence | Local data has explicit authority, integrity constraints, error handling, and backup behavior. |
| `MOBILE.OFFLINE.001` | Offline behavior | Reads and writes have defined behavior without connectivity and communicate freshness truthfully. |
| `MOBILE.SYNC.001` | Synchronization | Identity, ordering, conflict resolution, tombstones, retry, and reconciliation are explicit. |
| `MOBILE.MIGRATION.001` | Data migration | Every supported persisted version can migrate safely with failure detection and recovery. |
| `MOBILE.NETWORK.001` | Networking | Requests have cancellation, timeout, authentication refresh, retry ownership, and typed errors. |
| `MOBILE.CACHE.001` | Caching | Cache keys, scope, freshness, invalidation, storage limits, and privacy are deliberate. |
| `MOBILE.BACKGROUND.001` | Background work | Work tolerates suspension, expiration, relaunch, duplication, and operating-system scheduling constraints. |
| `MOBILE.NOTIFICATION.001` | Notifications | Scheduling, deduplication, cancellation, reconciliation, permissions, timezones, and calendars preserve reminder semantics. |
| `MOBILE.UI.001` | UI/domain boundary | Views coordinate presentation; authoritative domain rules remain testable outside UI lifecycle. |
| `MOBILE.CONCURRENCY.001` | Concurrency | UI isolation, actors/threads, cancellation, and shared mutable state are explicit. |
| `MOBILE.PRIVACY.001` | Privacy | Permissions are minimally scoped and sensitive data is protected in storage, logs, analytics, backups, and screenshots. |
| `MOBILE.LIFECYCLE.001` | Lifecycle | Cold launch, account change, background/foreground, termination, and restoration cannot corrupt or silently discard state. |
| `MOBILE.RESOURCE.001` | Resources | Battery, network, storage, memory, and background budgets match actual product needs. |
| `MOBILE.TEST.001` | Testability | Migrations, synchronization, notifications, and critical domain rules have deterministic seams. |
| `MOBILE.RELEASE.001` | Release evolution | Client/server compatibility supports staggered adoption and App Store rollback constraints. |

## Platform notes

- For SwiftUI, inspect observation ownership, dependency injection, task cancellation, actor isolation, and navigation restoration.
- For Core Data or SwiftData, inspect model versions, store migration, context ownership, merge policy, uniqueness, and error surfaces.
- For notifications, distinguish locally scheduled and remotely delivered flows.
- Do not require a server for a valid local-only product. Review against declared synchronization and recovery needs.
