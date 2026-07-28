#!/usr/bin/env python3
# ruff: noqa: E501
"""Generate the target architecture's curated supplemental knowledge entries."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import yaml

AZURE = (
    "Azure Architecture Center",
    "https://learn.microsoft.com/en-us/azure/architecture/",
)
AZURE_STYLES = (
    "Azure Architecture Styles",
    "https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/",
)
AZURE_PATTERNS = (
    "Azure Cloud Design Patterns",
    "https://learn.microsoft.com/en-us/azure/architecture/patterns/",
)
AWS = (
    "AWS Well-Architected Framework",
    "https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html",
)
ISO = (
    "ISO/IEC 25010:2023",
    "https://www.iso.org/standard/78176.html",
)
ANDROID_OFFLINE = (
    "Android Offline-first Guidance",
    "https://developer.android.com/topic/architecture/data-layer/offline-first",
)
OPENAI_AGENTS = (
    "OpenAI Agents SDK",
    "https://openai.github.io/openai-agents-python/",
)


@dataclass(frozen=True)
class Seed:
    kind: str
    id: str
    title: str
    domains: tuple[str, ...]
    triggers: tuple[str, ...]
    intent: str
    fit: str
    avoid: str
    source: tuple[str, str] = AZURE
    quality: tuple[str, ...] = ("maintainability",)


FOUNDATIONS = (
    Seed(
        "foundation",
        "quality-attributes",
        "Quality Attributes",
        ("cross-cutting",),
        ("quality", "scenario", "slo"),
        "Translate business outcomes into prioritized, measurable quality scenarios before comparing structures or technologies.",
        "A decision changes reliability, security, performance, cost, delivery, or another system quality.",
        "The requested work is purely mechanical and has no architecture trade-off.",
        ISO,
        ("reliability", "security", "performance-efficiency", "maintainability"),
    ),
    Seed(
        "foundation",
        "tradeoff-analysis",
        "Architecture Trade-off Analysis",
        ("cross-cutting",),
        ("tradeoff", "option", "decision"),
        "Compare how each viable option improves, degrades, or leaves unchanged every priority quality attribute.",
        "Two or more viable approaches make different quality, cost, or operating compromises.",
        "One option is mandatory by an authorized immutable constraint and no implementation choice remains.",
        AWS,
    ),
    Seed(
        "foundation",
        "architecture-principles",
        "Architecture Principles",
        ("cross-cutting",),
        ("principle", "boundary", "simplicity"),
        "Use proportionality, explicit ownership, compatibility, reversibility, and evidence as decision constraints rather than slogans.",
        "A review needs stable rules that apply across technologies and domains.",
        "A principle is being used to override direct repository or runtime evidence.",
        AZURE,
    ),
    Seed(
        "foundation",
        "evidence-reasoning",
        "Evidence Reasoning",
        ("cross-cutting",),
        ("evidence", "inference", "unknown"),
        "Separate observed facts, bounded inferences, unknowns, and counter-evidence so confidence follows proof strength.",
        "A model claim could affect severity, remediation, policy, or technology selection.",
        "No decision or claim is being made from the inspected material.",
        AZURE,
    ),
    Seed(
        "foundation",
        "proportional-design",
        "Proportional Architecture Design",
        ("cross-cutting",),
        ("simple", "overdesign", "stage"),
        "Choose the least complex mechanism that satisfies current quality scenarios, team capability, and credible evolution needs.",
        "A proposed platform or distributed mechanism adds operational or cognitive load.",
        "Regulatory or physical isolation mandates the more complex boundary.",
        AWS,
    ),
    Seed(
        "foundation",
        "technology-selection",
        "Technology Selection",
        ("cross-cutting",),
        ("framework", "platform", "adopt"),
        "Select technology from required capabilities, operational ownership, compatibility, exit cost, and current official evidence.",
        "A project is considering adding, replacing, or standardizing a framework, store, runtime, or managed service.",
        "The technology is already an immutable constraint and only compliant use is under review.",
        AZURE,
    ),
    Seed(
        "foundation",
        "system-boundaries",
        "System Boundaries",
        ("cross-cutting",),
        ("module", "ownership", "contract"),
        "Define boundaries from responsibility, authority, data ownership, contracts, deployment, and team accountability.",
        "Change propagation or failure isolation depends on where a responsibility is owned.",
        "Directory names are the only available signal and no owning behavior can be traced.",
        AZURE_STYLES,
    ),
    Seed(
        "foundation",
        "data-ownership",
        "Data Ownership",
        ("data",),
        ("writer", "authority", "lifecycle"),
        "Assign one authoritative owner for writes, schema evolution, lifecycle, access policy, recovery, and derived copies.",
        "Multiple components read or write durable business state.",
        "The data is ephemeral and wholly contained within one operation.",
        AZURE,
    ),
    Seed(
        "foundation",
        "evolutionary-architecture",
        "Evolutionary Architecture",
        ("delivery", "cross-cutting"),
        ("migration", "reversible", "fitness"),
        "Evolve through compatible slices, executable fitness functions, observable checkpoints, and explicit contraction gates.",
        "The target cannot be introduced safely in one atomic deployment.",
        "A disposable prototype has no persisted or public contract and replacement is cheaper than migration.",
        AZURE,
    ),
)

DECISIONS = (
    Seed(
        "decision-guide",
        "monolith-vs-microservices",
        "Monolith vs Microservices",
        ("backend-api", "distributed-systems"),
        ("monolith", "microservices", "services"),
        "Choose deployment and ownership boundaries from team autonomy, independent release, scaling, isolation, and operations evidence.",
        "A single deployment creates a proven organizational or operational constraint.",
        "Service separation is proposed only because the codebase is large or microservices appear more advanced.",
        AZURE_STYLES,
    ),
    Seed(
        "decision-guide",
        "layered-vs-modular-monolith",
        "Layered vs Modular Monolith",
        ("backend-api",),
        ("layered", "modular", "monolith"),
        "Choose horizontal layering or domain modules from change locality, ownership, transaction, and boundary-enforcement needs.",
        "One deployment remains appropriate but business changes increasingly cross horizontal layers.",
        "The application is simple CRUD with no stable domain modules.",
        AZURE_STYLES,
    ),
    Seed(
        "decision-guide",
        "sync-vs-async",
        "Synchronous vs Asynchronous Integration",
        ("backend-api", "distributed-systems"),
        ("sync", "async", "queue"),
        "Choose temporal coupling from result timing, ownership, delivery, ordering, retries, idempotency, and recovery.",
        "A cross-boundary interaction can complete immediately or continue after the caller returns.",
        "An in-process call inside one owner is sufficient.",
        AZURE,
    ),
    Seed(
        "decision-guide",
        "request-vs-background-job",
        "Request vs Background Job",
        ("backend-api", "reliability"),
        ("request", "background", "job"),
        "Move work out of a request only when duration, resource isolation, retry, cancellation, or recovery requires durable state.",
        "Work may exceed request deadlines or must survive client and process interruption.",
        "The operation is short, bounded, and the caller requires its immediate result.",
        AZURE,
    ),
    Seed(
        "decision-guide",
        "rest-vs-graphql-vs-grpc",
        "REST vs GraphQL vs gRPC",
        ("backend-api",),
        ("rest", "graphql", "grpc"),
        "Select an interface style from consumer diversity, query shape, streaming, latency, schema tooling, browser reach, and compatibility.",
        "A new public or cross-service interface has multiple plausible protocols.",
        "Protocol preference is the only differentiator.",
        AZURE,
    ),
    Seed(
        "decision-guide",
        "cache-strategy",
        "Cache Strategy",
        ("frontend", "backend-api", "data"),
        ("cache", "ttl", "invalidation"),
        "Choose cache location and invalidation from repeated cost, acceptable staleness, authority, failure behavior, and measured hit potential.",
        "Repeated reads or computation are materially expensive and bounded staleness is acceptable.",
        "No repeated cost or measurable latency and capacity problem exists.",
        AZURE_PATTERNS,
        ("performance-efficiency", "reliability"),
    ),
    Seed(
        "decision-guide",
        "data-loading-and-refresh",
        "Data Loading and Refresh",
        ("frontend", "backend-api"),
        ("prefetch", "refresh", "stale"),
        "Classify first-render, secondary, and user-triggered data before choosing blocking load, prefetch, refetch, or stale refresh.",
        "A client must balance first-render speed with freshness and consistency.",
        "All data is static build-time content.",
        AZURE,
    ),
    Seed(
        "decision-guide",
        "polling-vs-sse-vs-websocket",
        "Polling vs SSE vs WebSocket",
        ("frontend", "backend-api", "real-time"),
        ("polling", "sse", "websocket"),
        "Select update transport from direction, frequency, client count, missed-event recovery, infrastructure, and freshness targets.",
        "Server-created state changes must reach active clients.",
        "Updates are rare and user-triggered refresh meets the requirement.",
        AZURE,
    ),
    Seed(
        "decision-guide",
        "ssr-vs-csr-vs-ssg",
        "SSR vs CSR vs SSG",
        ("frontend",),
        ("ssr", "csr", "ssg"),
        "Choose rendering per route from personalization, freshness, discoverability, first-render, hosting, and hydration cost.",
        "A web surface mixes public content, personalized state, and interactive application behavior.",
        "One rendering mode is mandated and its limitations already satisfy every route.",
        AZURE,
    ),
    Seed(
        "decision-guide",
        "state-management",
        "Client State Management",
        ("frontend", "mobile"),
        ("state", "store", "server-state"),
        "Separate local UI, form, URL, server, and persisted domain state before selecting a shared store.",
        "State crosses components, routes, sessions, or offline boundaries.",
        "Component-local state already has one owner and no cross-boundary consumer.",
        AZURE,
    ),
    Seed(
        "decision-guide",
        "database-selection",
        "Database Selection",
        ("data",),
        ("database", "sql", "storage"),
        "Select the least complex authoritative store from integrity, query, consistency, scale, lifecycle, recovery, and operations.",
        "Current storage cannot meet a verified access or quality scenario.",
        "A new database is proposed only for fashion or hypothetical scale.",
        AZURE,
    ),
    Seed(
        "decision-guide",
        "message-system-selection",
        "Message System Selection",
        ("distributed-systems",),
        ("queue", "stream", "pubsub"),
        "Choose queue, pub-sub, or replayable stream from consumer semantics, ordering, retention, throughput, and operations.",
        "Asynchronous work or integration is proven necessary.",
        "A direct owned call or database-backed job satisfies the flow.",
        AZURE,
    ),
    Seed(
        "decision-guide",
        "relational-vs-document-vs-graph",
        "Relational vs Document vs Graph",
        ("data",),
        ("relational", "document", "graph"),
        "Match storage model to invariants and dominant access paths while preserving authority, migration, and operational simplicity.",
        "Relationships, aggregate documents, or graph traversal create materially different access needs.",
        "A relational schema already meets integrity and query needs.",
        AZURE,
    ),
    Seed(
        "decision-guide",
        "local-first-vs-server-first",
        "Local-first vs Server-first",
        ("mobile", "data"),
        ("offline", "local-first", "server-first"),
        "Choose authority and replica semantics from offline creation, conflict, device lifecycle, privacy, migration, and recovery.",
        "A client must work through prolonged disconnection or multi-device editing.",
        "Connectivity is required and server authority plus cache meets the experience.",
        ANDROID_OFFLINE,
    ),
    Seed(
        "decision-guide",
        "optimistic-vs-pessimistic-update",
        "Optimistic vs Pessimistic Update",
        ("frontend", "mobile", "data"),
        ("optimistic", "conflict", "rollback"),
        "Choose feedback timing from conflict probability, effect reversibility, authority, error impact, and compensation UX.",
        "User-perceived latency matters and writes may be presented before authority confirms them.",
        "The action is high-impact, irreversible, or conflicts are common.",
        AZURE,
    ),
    Seed(
        "decision-guide",
        "workflow-vs-agent",
        "Workflow vs Agent",
        ("ai-agent",),
        ("workflow", "agent", "deterministic"),
        "Use deterministic code or workflow unless open-ended model planning produces a measured benefit under bounded authority.",
        "Some steps may require model judgment, tools, loops, or human interruption.",
        "The sequence and decisions are fully deterministic.",
        OPENAI_AGENTS,
    ),
    Seed(
        "decision-guide",
        "single-agent-vs-multi-agent",
        "Single Agent vs Multi-agent",
        ("ai-agent",),
        ("single-agent", "multi-agent", "handoff"),
        "Add agents only for distinct authority, context, ownership, or evaluation boundaries that one agent cannot safely serve.",
        "One agent may be overloaded by genuinely separate specialist contexts or handoff authority.",
        "Multiple personas merely divide a deterministic workflow.",
        OPENAI_AGENTS,
    ),
    Seed(
        "decision-guide",
        "build-vs-adopt",
        "Build vs Adopt",
        ("cross-cutting",),
        ("build", "buy", "adopt"),
        "Compare custom implementation with library, platform, and managed service using differentiation, maturity, cost, control, and exit.",
        "A capability can be built internally or adopted from an external dependency.",
        "Procurement, licensing, or an immutable platform standard already decides the boundary.",
        AWS,
    ),
)

STYLES = (
    Seed(
        "architecture-style",
        "clean-architecture",
        "Clean Architecture",
        ("backend-api",),
        ("clean", "ports", "adapters"),
        "Keep durable domain policy independent from delivery, storage, and framework details through inward dependency direction.",
        "Core business rules are complex, long-lived, and tested independently of volatile adapters.",
        "Simple CRUD would gain interfaces and mapping without a credible replacement or isolation need.",
        AZURE_STYLES,
    ),
    Seed(
        "architecture-style",
        "multi-tenant-saas",
        "Multi-tenant SaaS Architecture",
        ("multi-tenant-saas",),
        ("tenant", "saas", "isolation"),
        "Share selected runtime capabilities while making tenant identity, data isolation, noisy-neighbor control, and lifecycle explicit.",
        "Multiple customers use one product and require governed isolation and cost attribution.",
        "Every customer requires a physically separate product lifecycle or regulation forbids sharing.",
        AZURE_STYLES,
    ),
)

PATTERNS = (
    Seed(
        "pattern",
        "stale-while-revalidate",
        "Stale While Revalidate",
        ("frontend", "backend-api"),
        ("stale", "refresh", "cache"),
        "Serve bounded stale data immediately while refreshing authority in the background and surfacing update failures.",
        "Read latency matters and short staleness is acceptable.",
        "The flow requires strict read-after-write or safety-critical freshness.",
        AZURE_PATTERNS,
        ("performance-efficiency", "reliability"),
    ),
    Seed(
        "pattern",
        "retry-with-backoff",
        "Retry with Backoff",
        ("reliability",),
        ("retry", "backoff", "jitter"),
        "Recover transient failures with bounded attempts, exponential delay, jitter, deadline propagation, and idempotent effects.",
        "A dependency exposes transient failures and retry success is measurable.",
        "Failures are permanent, overload-related without load shedding, or effects are not idempotent.",
        AZURE_PATTERNS,
        ("reliability",),
    ),
    Seed(
        "pattern",
        "load-shedding",
        "Load Shedding",
        ("reliability", "performance"),
        ("overload", "shed", "capacity"),
        "Reject or degrade lower-priority work before saturation consumes resources needed by critical flows.",
        "Capacity has a known saturation point and traffic can be prioritized.",
        "All work is equally critical and no safe rejection or degradation response exists.",
        AWS,
        ("reliability", "performance-efficiency"),
    ),
    Seed(
        "pattern",
        "cursor-pagination",
        "Cursor Pagination",
        ("backend-api", "data"),
        ("cursor", "pagination", "ordering"),
        "Page through a stable ordered key so cost and consistency do not degrade with deep offsets.",
        "Collections are large or mutate while clients traverse them.",
        "The result set is small and random page access is a hard requirement.",
        AZURE_PATTERNS,
        ("performance-efficiency", "reliability"),
    ),
    Seed(
        "pattern",
        "api-aggregation",
        "API Aggregation",
        ("backend-api", "frontend"),
        ("aggregation", "fanout", "bff"),
        "Aggregate consumer-specific reads at an owned boundary with deadlines, partial-result semantics, and fan-out limits.",
        "A client otherwise performs repeated high-latency calls across owned services.",
        "Aggregation would hide ownership or create an unbounded synchronous dependency chain.",
        AZURE_PATTERNS,
    ),
)

TECHNOLOGIES = (
    ("react", "React", ("frontend",), ("react", "jsx"), "https://react.dev/"),
    (
        "nextjs",
        "Next.js",
        ("frontend",),
        ("nextjs", "ssr", "rsc"),
        "https://nextjs.org/docs",
    ),
    ("vue", "Vue", ("frontend",), ("vue", "spa"), "https://vuejs.org/guide/"),
    (
        "astro",
        "Astro",
        ("frontend",),
        ("astro", "ssg", "islands"),
        "https://docs.astro.build/",
    ),
    (
        "vite",
        "Vite",
        ("frontend", "delivery"),
        ("vite", "bundler"),
        "https://vite.dev/guide/",
    ),
    (
        "fastapi",
        "FastAPI",
        ("backend-api",),
        ("fastapi", "asgi"),
        "https://fastapi.tiangolo.com/",
    ),
    (
        "django",
        "Django",
        ("backend-api",),
        ("django", "orm"),
        "https://docs.djangoproject.com/",
    ),
    (
        "nestjs",
        "NestJS",
        ("backend-api",),
        ("nestjs", "node"),
        "https://docs.nestjs.com/",
    ),
    (
        "spring-boot",
        "Spring Boot",
        ("backend-api",),
        ("spring", "java"),
        "https://docs.spring.io/spring-boot/index.html",
    ),
    (
        "aspnet-core",
        "ASP.NET Core",
        ("backend-api",),
        ("aspnet", "dotnet"),
        "https://learn.microsoft.com/en-us/aspnet/core/",
    ),
    (
        "sqlite",
        "SQLite",
        ("data", "mobile"),
        ("sqlite", "embedded"),
        "https://www.sqlite.org/docs.html",
    ),
    ("redis", "Redis", ("data",), ("redis", "cache"), "https://redis.io/docs/latest/"),
    (
        "nats",
        "NATS",
        ("distributed-systems",),
        ("nats", "messaging"),
        "https://docs.nats.io/",
    ),
    (
        "redis-streams",
        "Redis Streams",
        ("distributed-systems", "data"),
        ("redis", "streams"),
        "https://redis.io/docs/latest/develop/data-types/streams/",
    ),
    (
        "docker",
        "Docker",
        ("delivery",),
        ("docker", "container"),
        "https://docs.docker.com/",
    ),
    (
        "nginx",
        "NGINX",
        ("delivery", "backend-api"),
        ("nginx", "proxy"),
        "https://nginx.org/en/docs/",
    ),
    (
        "caddy",
        "Caddy",
        ("delivery", "backend-api"),
        ("caddy", "proxy"),
        "https://caddyserver.com/docs/",
    ),
)

REFERENCES = (
    Seed(
        "reference-architecture",
        "react-fastapi-postgresql",
        "React + FastAPI + PostgreSQL",
        ("frontend", "backend-api", "data"),
        ("react", "fastapi", "postgresql"),
        "Use a browser client, one API ownership boundary, and one transactional authority as a low-operations product baseline.",
        "A small team owns an interactive web product with relational integrity and no proven independent deployment need.",
        "Offline-first, extreme independent scaling, or multiple autonomous product teams are hard requirements.",
        AZURE,
    ),
    Seed(
        "reference-architecture",
        "real-time-task-status",
        "Real-time Task Status System",
        ("frontend", "backend-api", "real-time"),
        ("task", "status", "sse"),
        "Persist task state durably and deliver resumable notifications while keeping the status API authoritative.",
        "Long-running tasks need fresh progress in active clients and reconnect recovery.",
        "Work finishes within the request or manual refresh meets the product target.",
        AZURE,
    ),
    Seed(
        "reference-architecture",
        "server-first-mobile-client",
        "Server-first Mobile Client",
        ("mobile", "data"),
        ("mobile", "server-first", "cache"),
        "Keep the server authoritative while the client uses bounded display cache, explicit retries, and lifecycle-safe refresh.",
        "Online operation is required and full offline editing has no product value.",
        "Prolonged offline creation and conflict-aware synchronization are core capabilities.",
        ANDROID_OFFLINE,
    ),
    Seed(
        "reference-architecture",
        "multi-tenant-knowledge-base",
        "Multi-tenant Knowledge Base",
        ("multi-tenant-saas", "ai-agent", "data"),
        ("tenant", "retrieval", "knowledge"),
        "Separate tenant authority, ingestion, retrieval indexes, deletion, model context, and evidence provenance.",
        "Multiple tenants store and retrieve private knowledge through model-assisted workflows.",
        "All data is public or each tenant has a physically isolated deployment.",
        AZURE,
    ),
)

MIGRATIONS = (
    Seed(
        "migration-guide",
        "polling-to-sse",
        "Polling to SSE",
        ("frontend", "backend-api", "real-time"),
        ("polling", "sse", "migration"),
        "Add resumable server events beside the existing status endpoint, canary clients, and retain polling as recovery during the compatibility window.",
        "Polling load or freshness misses are measured and updates are server-to-client.",
        "Updates are rare or bidirectional communication is required.",
        AZURE,
    ),
    Seed(
        "migration-guide",
        "synchronous-to-background-job",
        "Synchronous Request to Background Job",
        ("backend-api", "reliability"),
        ("request", "job", "migration"),
        "Introduce durable job identity, idempotent execution, status reads, cancellation, and compatibility for existing callers.",
        "Request deadlines or process interruption cause failed long-running work.",
        "The operation is short and the caller requires an atomic result.",
        AZURE,
    ),
    Seed(
        "migration-guide",
        "direct-write-to-outbox",
        "Direct Write to Transactional Outbox",
        ("data", "distributed-systems"),
        ("outbox", "dual-write", "migration"),
        "Write business state and an outbound record in one local transaction, then publish idempotently with observable lag.",
        "A database change and message publish can diverge under partial failure.",
        "No integration event is required or the store cannot support a local atomic record.",
        AZURE_PATTERNS,
    ),
    Seed(
        "migration-guide",
        "offset-to-cursor-pagination",
        "Offset to Cursor Pagination",
        ("backend-api", "data"),
        ("offset", "cursor", "migration"),
        "Add cursor requests and responses alongside offsets, stabilize ordering, migrate consumers, then contract the old contract.",
        "Deep pages are costly or concurrent writes cause missing and duplicate records.",
        "Random numeric page access remains a hard consumer requirement.",
        AZURE,
    ),
    Seed(
        "migration-guide",
        "client-only-to-hybrid-rendering",
        "Client-only to Hybrid Rendering",
        ("frontend",),
        ("csr", "ssr", "migration"),
        "Move only routes with verified first-render or discovery needs to server or static rendering while preserving client interactivity.",
        "Selected routes have measurable first-render, sharing, or indexing problems.",
        "The application is authenticated and highly interactive with no public content need.",
        AZURE,
    ),
    Seed(
        "migration-guide",
        "server-first-to-offline-capable",
        "Server-first to Offline-capable",
        ("mobile", "data"),
        ("offline", "sync", "migration"),
        "Progress from display cache to local writes, outbox, cursors, tombstones, conflicts, and recovery through separately verified stages.",
        "Offline behavior is a proven product requirement and authority semantics are agreed.",
        "A cache and retry meet the weak-network experience.",
        ANDROID_OFFLINE,
    ),
)

ANTI_PATTERNS = (
    Seed(
        "anti-pattern",
        "distributed-monolith",
        "Distributed Monolith",
        ("distributed-systems",),
        ("distributed", "monolith", "coupling"),
        "Detect separately deployed services that must change, release, or recover together because boundaries and contracts remain shared.",
        "Services show coordinated deploys, synchronous cycles, or shared ownership.",
        "A temporary migration compatibility window has an owner and contraction gate.",
        AZURE,
    ),
    Seed(
        "anti-pattern",
        "shared-database-microservices",
        "Shared Database Microservices",
        ("distributed-systems", "data"),
        ("shared", "database", "writers"),
        "Detect services that bypass contracts through shared tables or schema authority.",
        "Multiple services independently write the same business state.",
        "One service owns writes and others use a governed read replica or view.",
        AZURE,
    ),
    Seed(
        "anti-pattern",
        "redis-everywhere",
        "Redis Everywhere",
        ("data",),
        ("redis", "cache", "authority"),
        "Detect Redis used as default database, queue, lock, cache, and coordination layer without separate semantics and recovery.",
        "One volatile system accumulates unrelated authoritative responsibilities.",
        "Each use has explicit ownership, durability, limits, recovery, and a simpler fit than alternatives.",
        AZURE,
    ),
    Seed(
        "anti-pattern",
        "queue-as-default",
        "Queue as Default",
        ("distributed-systems",),
        ("queue", "async", "default"),
        "Detect asynchronous boundaries added without latency, isolation, buffering, or ownership evidence.",
        "Simple owned calls become messages by convention.",
        "Queue semantics solve a traced deadline, load, or failure-path need.",
        AZURE,
    ),
    Seed(
        "anti-pattern",
        "websocket-for-rare-updates",
        "WebSocket for Rare Updates",
        ("frontend", "real-time"),
        ("websocket", "updates", "rare"),
        "Detect bidirectional connection complexity where refresh, polling, or SSE meets freshness.",
        "Updates are rare and mostly server-to-client.",
        "High-frequency bidirectional interaction is measured and reconnect semantics are owned.",
        AZURE,
    ),
    Seed(
        "anti-pattern",
        "cache-without-invalidation",
        "Cache without Invalidation",
        ("data", "performance"),
        ("cache", "invalidation", "stale"),
        "Detect a cache introduced without authority, staleness budget, invalidation, failure, or rebuild semantics.",
        "Cached values affect behavior but expiry and invalidation are undefined.",
        "Immutable content or content-addressed keys make invalidation unnecessary.",
        AZURE_PATTERNS,
    ),
    Seed(
        "anti-pattern",
        "repository-layer-everywhere",
        "Repository Layer Everywhere",
        ("backend-api", "data"),
        ("repository", "abstraction", "crud"),
        "Detect interfaces and mapping layers that add ceremony without isolation, testing, or replacement value.",
        "Every CRUD access receives an abstract repository by rule.",
        "Domain policy or multiple adapters need a real port boundary.",
        AZURE,
    ),
    Seed(
        "anti-pattern",
        "event-sourcing-for-crud",
        "Event Sourcing for CRUD",
        ("data", "distributed-systems"),
        ("event-sourcing", "crud", "history"),
        "Detect event sourcing adopted without temporal, audit, replay, or domain value sufficient for its versioning cost.",
        "Ordinary record updates are represented as events only for perceived sophistication.",
        "The event history is itself authoritative business data with governed evolution.",
        AZURE,
    ),
    Seed(
        "anti-pattern",
        "multi-agent-for-workflow",
        "Multi-agent for Deterministic Workflow",
        ("ai-agent",),
        ("multi-agent", "workflow", "deterministic"),
        "Detect agent coordination used where a typed deterministic workflow provides clearer control, recovery, and evaluation.",
        "Agent roles only mirror fixed processing steps.",
        "Each agent has a distinct context or authority boundary and measured outcome benefit.",
        OPENAI_AGENTS,
    ),
    Seed(
        "anti-pattern",
        "premature-generic-platform",
        "Premature Generic Platform",
        ("delivery", "portfolio"),
        ("platform", "generic", "premature"),
        "Detect a shared platform built before stable repeated semantics, consumers, ownership, and service-level expectations exist.",
        "A single product's local capability is generalized for hypothetical reuse.",
        "Multiple consumers share stable contracts and can fund independent platform ownership.",
        AWS,
    ),
)

CASES = (
    Seed(
        "case-study",
        "small-team-modular-saas",
        "Small-team Modular SaaS Decision",
        ("backend-api", "multi-tenant-saas"),
        ("modular", "saas", "small-team"),
        "Show why one small team selected a modular monolith over broad microservices while preserving extraction seams.",
        "A comparable product has one team, frequent change, relational transactions, and constrained operations.",
        "Independent regulated deployments or autonomous service teams dominate the comparison.",
        AZURE_STYLES,
    ),
    Seed(
        "case-study",
        "queue-worker-before-workflow",
        "Queue Worker before Durable Workflow",
        ("backend-api", "reliability"),
        ("queue", "worker", "workflow"),
        "Show why short idempotent AI jobs used a queue and database status before adopting a workflow runtime.",
        "Jobs are bounded, have no human pause, and can restart from one durable state.",
        "Days-long timers, signals, approvals, or compensation are present.",
        AZURE,
    ),
    Seed(
        "case-study",
        "sse-task-progress",
        "SSE Task Progress Delivery",
        ("frontend", "real-time"),
        ("sse", "task", "progress"),
        "Show how an authoritative status API plus resumable SSE improved freshness without WebSocket bidirectionality.",
        "Clients only receive server-created progress and can refetch after gaps.",
        "Clients require high-frequency bidirectional collaboration.",
        AZURE,
    ),
    Seed(
        "case-study",
        "sqlite-is-appropriate",
        "SQLite Is Appropriate",
        ("data", "mobile"),
        ("sqlite", "false-positive", "local"),
        "Show that an embedded single-writer store can satisfy integrity, deployment, backup, and scale for its actual boundary.",
        "A local or single-node owner has bounded concurrency and simple operations.",
        "Multiple independent writers or horizontal write scaling are required.",
        ("SQLite Documentation", "https://www.sqlite.org/whentouse.html"),
    ),
    Seed(
        "case-study",
        "single-agent-is-sufficient",
        "Single Agent Is Sufficient",
        ("ai-agent",),
        ("single-agent", "multi-agent", "false-positive"),
        "Show how one bounded agent with typed tools and deterministic policy outperformed an unproven multi-agent split in simplicity and control.",
        "One context and authority boundary serves the task.",
        "Specialists require isolated context, permissions, ownership, or independent evaluation.",
        OPENAI_AGENTS,
    ),
    Seed(
        "case-study",
        "server-cache-not-local-first",
        "Server Cache without Local-first",
        ("mobile", "data"),
        ("cache", "server-first", "offline"),
        "Show how server authority plus bounded client cache met weak-network reads without creating conflict-aware replicas.",
        "Offline editing is not required and cached display is sufficient.",
        "Users must create and reconcile durable edits during prolonged disconnection.",
        ANDROID_OFFLINE,
    ),
)


def technology_seeds() -> tuple[Seed, ...]:
    return tuple(
        Seed(
            "technology-profile",
            entry_id,
            title,
            domains,
            triggers,
            f"Use {title} only for capabilities established by current official documentation and matched to a verified project requirement.",
            f"The project's language, runtime, deployment, and team constraints match {title}'s operating model.",
            f"A simpler existing dependency meets the requirement or the team cannot own {title}'s lifecycle and failure modes.",
            (f"{title} Documentation", url),
        )
        for entry_id, title, domains, triggers, url in TECHNOLOGIES
    )


ALL_SEEDS = (
    FOUNDATIONS
    + DECISIONS
    + STYLES
    + PATTERNS
    + technology_seeds()
    + REFERENCES
    + MIGRATIONS
    + ANTI_PATTERNS
    + CASES
)

DIRECTORIES = {
    "foundation": ("foundations", "foundation"),
    "decision-guide": ("decision-guides", "decision"),
    "architecture-style": ("architecture-styles", "style"),
    "pattern": ("patterns", "pattern"),
    "technology-profile": ("technology-profiles", "technology"),
    "reference-architecture": ("reference-architectures", "reference"),
    "migration-guide": ("migration-guides", "migration"),
    "anti-pattern": ("anti-patterns", "anti-pattern"),
    "case-study": ("case-studies", "case-study"),
}


class GenerationError(RuntimeError):
    """Unsafe target-knowledge generation."""


def render(seed: Seed) -> str:
    directory, prefix = DIRECTORIES[seed.kind]
    del directory
    metadata = {
        "id": f"{prefix}.{seed.id}",
        "kind": seed.kind,
        "version": "1.0.0",
        "status": "active",
        "domains": list(seed.domains),
        "triggers": list(seed.triggers),
        "quality_attributes": list(seed.quality),
        "related": [],
        "last_reviewed": "2026-07-28",
        "review_after_days": 90 if seed.kind == "technology-profile" else 365,
        "source_policy": (
            "official-docs-required"
            if seed.kind == "technology-profile"
            else "stable-principles-plus-official-docs"
        ),
        "sources": [
            {
                "title": seed.source[0],
                "url": seed.source[1],
                "authority": "standard" if seed.source == ISO else "official",
            }
        ],
    }
    if seed.kind == "technology-profile":
        metadata["dynamic_facts"] = True
        metadata["version_range"] = (
            "Current supported stable releases; verify official documentation "
            "before a project decision."
        )
    body = f"""# {seed.title}

## Problem and intent

{seed.intent}

## Mechanism

Apply the mechanism at its owning boundary, keep authority and contracts explicit, and bind the choice to measurable scenarios rather than technology presence.

## Fit when

{seed.fit}

## Avoid when

{seed.avoid}

## Required capabilities

An accountable owner, explicit compatibility and failure semantics, proportional tests, observable outcomes, and an affordable operating model are required.

## Benefits

The choice addresses the stated problem while keeping the reason, protected qualities, and governing evidence reviewable.

## Costs and liabilities

It adds implementation, migration, cognitive, and operational costs that must be compared with keeping the current design.

## Failure modes

It fails when adopted from naming, popularity, or hypothetical scale without ownership, negative-path behavior, and acceptance evidence.

## Alternatives

Keep the current architecture with a local correction, or select the next simpler mechanism that satisfies the same quality scenario.

## Migration and exit

Introduce the new behavior behind a compatible boundary, observe a bounded cohort, preserve rollback, and remove the old path only after consumers and data are verified.

## Evidence to inspect

Inspect the product scenario, owning code and configuration, consumers, persisted contracts, tests, runtime evidence when applicable, team capability, and cost boundary.

## Evidence that changes the recommendation

A simpler option meeting the same measurable outcome, missing operational ownership, incompatible consumers, or contrary runtime evidence changes the recommendation.

## Quality trade-offs

Prioritize {", ".join(seed.quality)} while explicitly recording effects on reliability, security, performance, maintainability, delivery speed, cost, and cognitive load.

## Volatile facts

Versions, support status, compatibility, security advisories, licensing, pricing, and service limits require current official confirmation; they are not timeless architecture facts.
"""
    return (
        "---\n"
        + yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True, width=88)
        + "---\n\n"
        + body
    )


def generate(root: Path, *, check: bool) -> int:
    seen: set[str] = set()
    count = 0
    for seed in ALL_SEEDS:
        directory, prefix = DIRECTORIES[seed.kind]
        canonical_id = f"{prefix}.{seed.id}"
        if canonical_id in seen:
            raise GenerationError(f"Duplicate target knowledge seed {canonical_id}")
        seen.add(canonical_id)
        path = root / directory / f"{seed.id}.md"
        expected = render(seed)
        if path.exists():
            if path.read_text(encoding="utf-8") != expected:
                raise GenerationError(f"Generated knowledge drift: {path}")
        elif check:
            raise GenerationError(f"Missing generated knowledge: {path}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8")
        count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        count = generate(args.root.resolve(), check=args.check)
    except (GenerationError, OSError) as exc:
        print(f"Target knowledge generation failed: {exc}")
        return 2
    print(f"Target knowledge: {count} entries {'checked' if args.check else 'written'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
