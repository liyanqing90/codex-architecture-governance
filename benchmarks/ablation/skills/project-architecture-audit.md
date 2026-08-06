# Compact project architecture audit

Use the supplied repository fixture only. Start with the compact operational
kernel, then project-stable context, then run-specific facts and selected
Knowledge metadata. Read full source evidence only when it drives a candidate,
resolves ambiguity, or supplies an explicit source-backed trade-off; verify the
recorded source hash before reading it. Map executable boundaries, data
ownership, externally visible contracts, state transitions, failure handling,
and evidence from code/configuration/tests. Report only rule-backed risks that
the fixture proves. Preserve candidate versus inference versus unknown, and
never treat context size or optional telemetry as Gate evidence.
