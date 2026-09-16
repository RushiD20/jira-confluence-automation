# Jira/Confluence Automation Constitution

**Version:** 1.0.0  
**Ratified:** 2026-09-16  
**Last Amended:** 2026-09-16

## Purpose

This constitution defines the engineering principles and delivery standards for the Jira/Confluence automation project. It applies to the React frontend, Express backend, PostgreSQL persistence layer, integrations with Atlassian services, and supporting automation jobs.

## Core Principles

### I. Contract-First Integration

All Jira and Confluence interactions MUST be defined behind typed service boundaries. Atlassian API calls MUST be isolated from UI components and route handlers, with explicit request and response types, timeout handling, and actionable error classification. External API behavior MUST be verified against the target Jira or Confluence workflow before production rollout.

### II. Idempotent Automation

Every automation operation MUST be safe to retry. Repeated webhooks, scheduled jobs, or client requests MUST NOT create duplicate transitions, comments, pages, notifications, or other side effects. Operations that change external state MUST use stable idempotency keys, status checks, or equivalent duplicate-prevention mechanisms.

### III. Observable and Auditable Behavior

User-visible and automated actions MUST produce sufficient structured logs to identify the operation, target resource, outcome, correlation or idempotency key, and failure reason without exposing secrets. Important state changes MUST leave an audit trail in the appropriate system. Failed actions MUST provide a clear manual recovery path.

### IV. Secure by Default

Credentials, tokens, cookies, and personal data MUST NOT be committed to source control or written to ordinary logs. Secrets MUST be supplied through environment configuration or an approved secret store. Backend authorization MUST be enforced server-side, and frontend controls MUST NOT be treated as security boundaries. Webhook endpoints MUST validate authenticity when supported and MUST reject malformed or unauthorized requests.

### V. Layered Architecture

The React 18 + Vite frontend MUST communicate with the Node.js + Express backend through documented API contracts. Route handlers MUST remain thin; business rules belong in backend services or domain modules. Persistence MUST be accessed through a dedicated data-access boundary. Jira and Confluence clients MUST remain replaceable and independently testable.

### VI. PostgreSQL as the System of Record

PostgreSQL 15, provisioned through Docker for local development and repeatable testing, MUST be used for durable application state that cannot be reliably reconstructed from Atlassian APIs. Schema changes MUST be versioned and reversible where practical. Database writes MUST preserve consistency through transactions or explicit compensating behavior, and indexes MUST support production query patterns.

### VII. Testable Delivery

Each feature MUST have acceptance criteria before implementation. Business rules MUST have focused automated tests, including success, failure, retry, permission, and no-op cases where applicable. Integration tests MUST cover database and Atlassian boundaries using controlled fixtures or mocks. A change MUST NOT be considered complete until its relevant tests and validation checks pass.

### VIII. Explicit Operational States

The system MUST represent loading, success, empty, partial, unauthorized, rate-limited, and failure states explicitly. Automation MUST distinguish a deliberate no-op from an error. User-facing messages MUST be actionable and MUST NOT expose implementation details or sensitive information.

### IX. Small, Reviewable Changes

Changes SHOULD be organized around one coherent behavior or capability. New implementation MUST follow existing project conventions unless a documented architectural decision justifies a change. Generated files, unrelated refactors, and speculative abstractions MUST be kept out of feature changes.

## Technology Standards

- **Frontend:** React 18 with Vite. Components MUST be accessible, responsive, and free of direct Atlassian credentials or server-side secrets.
- **Backend:** Node.js with Express. Runtime configuration MUST be validated at startup, and asynchronous failures MUST reach centralized error handling.
- **Database:** PostgreSQL 15 via Docker Compose for local development and integration testing. Local setup MUST be reproducible from repository configuration.
- **External systems:** Jira Cloud and Confluence APIs. API limits, transient failures, permission failures, and workflow-specific transition constraints MUST be handled deliberately.
- **Quality gates:** Type checking, linting, focused unit tests, integration tests for changed boundaries, and build verification MUST run before merge when configured for the affected package.

## Delivery Workflow

Every substantial change follows this sequence:

1. Define user-visible behavior and acceptance criteria.
2. Clarify permissions, workflow assumptions, data ownership, and failure behavior.
3. Produce a technical plan covering frontend, backend, database, and integration boundaries as applicable.
4. Break the plan into independently verifiable tasks.
5. Implement with tests and structured observability.
6. Validate the acceptance criteria and document unresolved external dependencies.

## Governance

This constitution is the highest-level engineering standard for the project. Feature specifications, implementation plans, and code reviews MUST comply with it or record an explicit exception. Exceptions require a written rationale, scope, owner, and expiration or review date. When documents conflict, this constitution takes precedence unless it is formally amended.

Amendments require a version update, a concise rationale, and review by the project maintainers. New or changed principles MUST be reflected in relevant templates, tests, and development documentation. Reviewers SHOULD reject changes that weaken idempotency, security, observability, or testability without an approved exception.
