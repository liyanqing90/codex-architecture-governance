# Server-authoritative mobile cache

The app requires a network for edits. Its local store is an expiring display
cache and can be discarded at any time. Offline editing is explicitly not a
product requirement.

Expected decision: do not recommend an offline-first replica or CRDT.
