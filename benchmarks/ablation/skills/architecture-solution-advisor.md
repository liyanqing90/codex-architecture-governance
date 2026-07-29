# Compact architecture solution decision

Choose the least-complex option supported by the fixture. Compare keep-current
or a local correction, the smallest viable structural improvement, and one
materially different alternative. Do not recommend microservices without
independent deployment and ownership, durable workflow where queue plus
durable state is enough, offline-first where server authority plus cache fits,
or multi-agent orchestration where one agent or a fixed workflow fits. Explain
the selected option, rejected options, trade-offs, and reversible slices.
