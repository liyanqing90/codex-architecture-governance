# Account balance updates

The API and worker independently perform read-modify-write updates to the same
account balance without version checks or a shared transaction owner. A retry
can interleave the operations and silently lose an update. This balance is
authoritative financial state; the overwritten credit or debit cannot be
reconstructed from the stored balance and requires manual reconciliation.
