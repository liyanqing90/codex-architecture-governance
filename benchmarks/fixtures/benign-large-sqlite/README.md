# Benign large SQLite fixture

Single-user desktop catalog. SQLite is the declared authoritative local store.
The generated lookup table is intentionally large, read-only, and rebuilt
atomically. No network sync, concurrent writers, or scale requirement exists.

Expected behavior: do not create an architecture finding from file size or
SQLite alone.
