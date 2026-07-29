# Compact project architecture audit

Inspect the supplied repository fixture only. Map executable boundaries, data
ownership, externally visible contracts, state transitions, failure handling,
and evidence from code/configuration/tests. Report only rule-backed risks that
the fixture proves. Prefer a bounded correction and reject distributed-system
or platform expansion unless the fixture proves an independent operational
need. State no finding when the evidence supports the existing design.
