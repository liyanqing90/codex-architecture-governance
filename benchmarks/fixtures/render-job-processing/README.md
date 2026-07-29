# Render job processing

A single team runs one API and one worker. Jobs are short, idempotent, and have
no branching, approval, compensation, or pause/resume requirement. The database
owns task status and the queue provides at-least-once delivery.
