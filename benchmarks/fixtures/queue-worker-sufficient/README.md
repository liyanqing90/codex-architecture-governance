# Queue worker is sufficient

A single team runs one API and one worker. Jobs are short, idempotent, and have
no branching, approval, compensation, or pause/resume requirement. The database
owns task status and the queue provides at-least-once delivery.

Expected decision: retain Web-Queue-Worker. Do not recommend microservices,
Temporal, or multiple agents.
