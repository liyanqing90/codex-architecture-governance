# Orders and billing services

Orders and billing deploy independently but both perform read-modify-write
updates against the same account balance table. A coordinated release is not
required to reproduce the lost update. The balance is authoritative financial
state; the overwritten reservation or refund cannot be reconstructed from the
stored balance and crosses both service ownership boundaries.
