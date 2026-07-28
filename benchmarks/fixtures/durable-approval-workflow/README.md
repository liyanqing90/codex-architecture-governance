# Missing durable approval workflow

The process may wait days for approval. State lives only in memory, approval is
checked before parameters are later regenerated, and retries can call the
payment tool twice after a crash.
