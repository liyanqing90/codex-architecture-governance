# Payment design note and runtime

The design note claims every payment uses a durable idempotency marker before
calling the provider. The executable path checks a processed-command store,
calls the provider, and records the command afterward. A crash after the
provider charge but before the marker is recorded can immediately charge the
customer twice.
