# Payment approval process

The process may wait days for approval. State lives only in memory, approval is
checked before parameters are later regenerated, and retries can call the
payment tool twice after a crash. The charge is an immediate, irreversible
financial side effect: approval must bind its exact parameters, and recovery
must not repeat it.
