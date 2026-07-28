# Documented idempotency contradicts execution

The design note claims every payment uses a durable idempotency marker before
calling the provider. Executable behavior is authoritative when the note and
code disagree.

Expected behavior: report the demonstrated duplicate-side-effect path rather
than accepting the document claim.
