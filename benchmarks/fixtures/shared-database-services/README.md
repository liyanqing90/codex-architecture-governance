# Services with conflicting data ownership

Orders and billing deploy independently but both perform read-modify-write
updates against the same account balance table. A coordinated release is not
required to reproduce the lost update.

Expected behavior: report ownership and transaction-boundary risks. The mere
presence of services is not the finding.
