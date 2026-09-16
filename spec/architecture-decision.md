# Architecture Decision: Jira Parent Automation

**Decision ID:** ADR-001  
**Status:** Approved  
**Date:** 2026-09-16  
**Approved by:** Project owner  
**Scope:** Close Parent When Sub-Tasks Finish  
**Related task:** T-001 in [tasks.md](tasks.md)

## Decision

Use an **application-backed orchestration architecture** for the Jira parent-status automation.

The Node.js/Express backend owns event intake, business-rule evaluation, idempotency, concurrency control, retries, Jira mutations, and structured execution records. PostgreSQL 15 is the durable store for execution state and idempotency state. The React 18 + Vite frontend is an operator-facing client only and does not hold Jira credentials or perform Jira mutations directly.

Native Jira Automation is not the selected implementation for this feature. A native or hybrid implementation requires a separate architecture review and an approved constitution exception before it is used.

## Component Ownership

| Capability | Owner |
|---|---|
| Event intake and validation | Node.js/Express backend |
| Close/reopen decision logic | Backend domain/evaluation service |
| Jira API calls | Typed backend Jira client service |
| Idempotency and concurrency state | PostgreSQL 15 through a dedicated repository boundary |
| Retry and reconciliation | Backend orchestration service |
| Execution and audit records | Backend logging service and PostgreSQL execution store |
| Operator-facing status and diagnostics | React 18 + Vite frontend through documented backend APIs |
| External workflow and permission configuration | Jira administrator and deployment configuration |
| Database provisioning for local development and integration tests | Docker Compose with PostgreSQL 15 |

## Boundary Rules

- The frontend MUST communicate with the backend through documented API contracts.
- Jira and Confluence credentials MUST remain server-side.
- Jira API calls MUST pass through the typed Jira client boundary.
- Business rules MUST remain outside Express route handlers.
- Durable execution and idempotency state MUST use PostgreSQL rather than frontend state or unstructured logs.
- The backend MUST validate inbound events, authenticate the source, and reject malformed or unauthorized requests.
- Exact Jira transition IDs and workflow mappings remain deployment configuration and will be validated during the workflow-discovery phase.

## Implementation Consequences

- Application-backed implementation tasks are required for the Jira client, inbound route, authentication, PostgreSQL migrations, repositories, retry handling, and execution logging.
- The system must provide controlled local and integration environments using Docker Compose and PostgreSQL 15.
- Native Jira Automation rule configuration is deferred and must not be enabled for this feature without a new approved decision.
- Detailed tradeoffs, constitution compliance evidence, and any required exception record are addressed by Task T-002.
