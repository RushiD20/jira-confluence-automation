# Specification Clarifications and Senior Review

**Reviewed documents:** [constitution.md](constitution.md), [specification.md](specification.md)  
**Review date:** 2026-09-16  
**Review status:** Blocking clarifications remain; two findings are accepted as out of scope

## Accepted Out-of-Scope Decisions

The following review findings are intentionally outside this feature specification:

- Selecting native Jira Automation versus the React/Express/PostgreSQL application architecture. That choice belongs in the technical plan and must follow the constitution.
- Defining exact Jira transition IDs, names, status IDs, and workflow mappings. Those are implementation and deployment configuration details. The implementation must still validate that suitable close and reopen transitions are configured before production enablement.

This review identifies gaps, contradictions, and ambiguous requirements that should be resolved before implementation planning. Items are ordered by implementation risk rather than by document order.

## 1. Critical Gaps and Contradictions

### C-001: Implementation boundary is undefined

**Disposition:** Out of scope by decision; retain as a technical-planning concern.

**References:** Constitution Principles I, V, and VI; specification Sections 1, 3, and 6.

The constitution describes a React 18 + Vite frontend, Node.js + Express backend, and PostgreSQL 15 application. The specification describes a Jira Cloud Automation capability and only conditionally mentions application persistence: “If implemented as part of the application rather than only native Jira Automation.” These are materially different implementations with different security, retry, logging, testing, and deployment models. The implementation choice is intentionally deferred to the technical plan.

**Decision required during technical planning, not in this feature specification:** Choose one implementation model:

- Native Jira Automation only.
- Express/PostgreSQL service receiving Jira webhooks and running the business logic.
- A hybrid, with native rules forwarding events to the application.

The specification must identify which component owns triggers, state, idempotency, retries, comments, transitions, and operational logs.

### C-002: The constitution’s typed-service requirement is not mapped to the feature

**References:** Constitution Principle I; specification Sections 5 and 6.

The specification does not define the Jira client contract, service interface, error model, or request/response types required by the constitution if the feature is application-backed. It also does not explain how the constitution applies if native Jira Automation is selected.

**Decision required:** Define the owning service boundary and its contract, or record a constitution exception for a native-only implementation.

### C-003: PostgreSQL ownership and source of truth are unclear

**References:** Constitution Principle VI; specification Section 6.

The constitution requires PostgreSQL for durable application state that cannot be reconstructed from Atlassian APIs. The feature spec does not state whether execution records, idempotency keys, transition attempts, or workflow configuration are stored in PostgreSQL, Jira comments, Jira Automation logs, or a combination.

**Decision required:** Define persisted entities, ownership, retention, and recovery behavior. If native Jira Automation is the selected implementation, explicitly state why PostgreSQL is not used for this feature.

### C-004: Close target and reopen target are not concrete

**Disposition:** Out of scope by decision; retain as an implementation/deployment validation requirement.

**References:** Specification FR-010, FR-012, Sections 10 and 11.

`DONE` is used both as a status-like target and as a transition-like value, but Jira distinguishes status names, status IDs, status categories, and transition IDs. The exact close transition, target status, reopen transition, and reopen target status are unresolved.

**Decision required during implementation and deployment:** Configure and validate suitable transition IDs or stable names, target status IDs, and workflow scope for every eligible parent issue type. The feature contract does not prescribe those identifiers.

### C-005: Event-driven processing and daily refresh are contradictory in priority

**References:** Specification Overview, Scope, FR-005, AT-010, and Section 11.

The overview says the daily refresh is optional, while FR-005 says the automation MUST support it if enabled. The specification does not decide whether the refresh is required for production, what it repairs, or whether it evaluates every parent or only parents changed since the last run.

**Decision required:** Mark the daily refresh as required or out of scope for the first release. If required, define schedule, timezone, selection query, pagination, rate limits, ownership, and behavior for missed or already-processed events.

### C-006: Idempotency is not implementable atomically as specified

**References:** Constitution Principle II; specification FR-014 through FR-018 and the failure scenarios.

The spec requires adding a Jira comment before transitioning, while also requiring no duplicate comments or transitions on retries. A failure between the comment and transition, a timeout after a successful transition, or two concurrent events can leave the system unable to determine whether the side effect completed. A comment marker alone is not an atomic lock and can cause both duplicate comments and skipped recovery.

**Decision required:** Define a stable idempotency key, its source fields, the state machine for `received`, `evaluating`, `commented`, `transitioned`, and `failed`, and the behavior for ambiguous timeouts. Define whether concurrent evaluations use a database lock, Jira-side guard, or accepted eventual consistency.

### C-007: Concurrency and stale-read behavior are unspecified

**References:** Specification FR-006 through FR-010.

Two sub-tasks may transition around the same time. Each evaluation may read a different snapshot of the parent’s sub-tasks or available transitions. The spec does not state how simultaneous close/reopen evaluations are serialized, how a parent changing state during evaluation is handled, or whether a transition conflict is retried.

**Decision required:** Define concurrency control, re-read points before mutation, conflict handling, and the maximum retry count.

## 2. High-Priority Gaps

### H-001: Eligible parent issue types are not identified

**References:** Specification Scope and FR-002.

“Parent issue types that support sub-tasks” may include different workflows and transition IDs. The specification does not identify the allowed issue types or whether all `ARE` parent types are included.

**Decision required:** List the included parent issue types and explicitly exclude any types with different lifecycle rules.

### H-002: Done status-category semantics are incomplete

**References:** Specification Overview, FR-003, FR-004, and FR-008.

The spec relies on Jira’s Done status category but does not define how transitions with multiple status changes, deleted sub-tasks, archived issues, or unavailable sub-task records are handled. It also does not state whether resolution, status name, or status category is authoritative.

**Decision required:** Declare status category as the sole authority, define the handling of missing/archived sub-tasks, and specify whether resolution is changed or validated.

### H-003: Failure handling can create duplicate diagnostic comments

**References:** Constitution Principle II; specification FR-019 through FR-022 and Error and Edge-Case Behavior.

The specification prevents duplicate marker comments but does not define deduplication for diagnostic comments. Repeated retries could notify the assignee repeatedly for the same unresolved failure.

**Decision required:** Define a failure idempotency key, comment marker, notification frequency, and whether a new comment is created only when the failure reason changes or a retry threshold is reached.

### H-004: Comment formats are not normative

**References:** Specification FR-014, FR-015, and FR-020.

The marker examples use “such as,” and the diagnostic comment has required content but no exact template, machine-readable fields, or maximum size. This makes duplicate detection, testing, and support tooling ambiguous.

**Decision required:** Provide exact close, reopen, and failure templates, including stable identifiers, timestamps, issue keys, transition IDs, and safe error text. Define escaping and truncation rules.

### H-005: Notification behavior is not guaranteed by the requirement

**References:** Specification FR-021, FR-022, Error and Edge-Case Behavior.

“Mention and notify” depends on Jira Cloud comment format, account identity, notification settings, and whether the assignee is active or assignable. “When notification is supported” weakens the acceptance requirement and can make AT-006 impossible to pass consistently.

**Decision required:** Define the supported mention syntax, required notification guarantee, behavior for inactive/unassigned users, and an alternate escalation channel if Jira cannot notify the assignee.

### H-006: Authentication and webhook security are missing from the feature spec

**References:** Constitution Principle IV; specification Sections 3 and 6.

If an Express service or webhook is used, the spec does not define webhook signature validation, authentication, replay protection, authorization, or payload schema validation. If native Jira Automation is used, the spec should state that these controls are delegated to Jira and identify the rule security model.

**Decision required:** Specify the inbound trigger mechanism and its security controls, including secret rotation, replay window, and unauthorized-request behavior.

### H-007: Retry and rate-limit policy is incomplete

**References:** Constitution Technology Standards; specification NFR-001, Error and Edge-Case Behavior.

The spec says transient failures must be retryable but does not define which failures are retryable, backoff, jitter, maximum attempts, dead-letter/manual-review behavior, or Jira rate-limit handling.

**Decision required:** Define retry classes for 429, 5xx, network timeouts, permission errors, invalid transitions, and validation failures. Define `Retry-After` handling and the terminal failure state.

### H-008: Execution log contract is undefined

**References:** Constitution Principle III; specification FR-018, NFR-004, AT-009.

The required execution record has no schema, storage location, correlation ID format, severity, retention period, access control, or searchable fields. “Visible in execution logs” is not a testable interface.

**Decision required:** Define the log/event schema, destination, retention, redaction rules, and how operators query or export records.

### H-009: Partial side-effect outcomes are not defined

**References:** Specification FR-014 through FR-022.

The spec does not define behavior when adding the marker succeeds but the transition fails, the transition succeeds but the response times out, the diagnostic comment fails, or the comment is added but notification fails.

**Decision required:** Define reconciliation behavior for each partial outcome and whether a retry may safely re-read Jira state before adding comments or transitioning.

### H-010: Access and environment assumptions conflict with rollout readiness

**References:** Specification Scope, Section 11, and the source project documentation.

The project documentation records an Atlassian access dependency, but the feature spec treats project and workflow availability as a clarification rather than a release gate with an owner and evidence.

**Decision required:** Assign an owner, define the evidence required for access and permissions, and make access verification a prerequisite to configuration and acceptance testing.

## 3. Medium-Priority Gaps

### M-001: Scheduled refresh scope and timezone are missing

The spec does not define the refresh time, timezone, daylight-saving behavior, maximum runtime, pagination, or whether refresh runs overlap. It also does not define how many parent issues may be evaluated in one run.

### M-002: Parent and sub-task deletion, archival, and permissions are missing

The behavior is undefined when the parent or sub-task is deleted, archived, hidden from the rule actor, moved between projects, or returned incompletely by Jira. Decide whether to ignore, fail, or alert for each case.

### M-003: Assignee changes during processing are missing

The specification reads the parent assignee for failure notification but does not define whether to use the assignee at event time or failure time, or what to do when the parent is unassigned.

### M-004: Transition selection is underspecified

If multiple valid transitions lead to the desired status, the selection rule is not defined. The spec should require an explicit transition ID or deterministic selection and should reject ambiguous configuration.

### M-005: Jira API pagination and payload limits are missing

“Retrieve or evaluate all sub-tasks” does not define pagination, maximum sub-task count, fields requested, timeout, or behavior when Jira returns partial data.

### M-006: Configuration management is missing

The spec does not define where project key, site URL, transition IDs, status category IDs, schedule, retry settings, and marker templates are configured, validated, and versioned.

### M-007: Test doubles and integration test boundaries are missing

The constitution requires unit and integration tests, but the specification does not define Jira client mocks, fixture payloads, contract tests, database fixtures, or which tests require a live Jira sandbox. It also does not define how to test notification behavior without sending real notifications.

### M-008: Acceptance test data is not reproducible

The test parent, sub-task keys, starting statuses, workflow, assignee, and reset procedure are not specified. Without a deterministic fixture and cleanup strategy, the acceptance matrix cannot be repeated reliably.

### M-009: No performance or operational targets are defined

There are no targets for event-to-transition latency, scheduled refresh completion, API calls per evaluation, concurrent executions, or maximum recovery time.

### M-010: Rule ownership and escalation are missing

The spec mentions an owner only as an unresolved dependency. It does not name who enables/disables the rule, reviews failures, approves workflow changes, or handles unresolved notifications.

### M-011: Security and privacy details are incomplete

The spec prohibits exposing secrets but does not define Jira token storage, least-privilege scopes, log redaction for issue content and user identifiers, audit access, or retention requirements for personal data.

### M-012: The application-facing behavior is absent

If this feature belongs to the React/Express application, the specification defines no backend endpoints, frontend workflow, authorization model, execution-log view, manual retry action, or user-facing states. The constitution’s frontend and API requirements therefore cannot be validated from this specification.

## 4. Lower-Priority Ambiguities

### L-001: Terminology is inconsistent

The document uses “close,” “transition to `DONE`,” “Done status,” “Done status category,” “parent status,” and “reopen” without a glossary. Add definitions for status, status category, transition, parent, sub-task, close action, reopen action, no-op, and execution.

### L-002: “Successful execution” is not defined

It is unclear whether an execution is successful when the condition is evaluated successfully but no transition is needed, when a comment succeeds but a transition fails, or only when the desired parent status is observed after the transition.

### L-003: “No-op” and “ignored” are not consistently distinguished

Some cases are called no-ops and others are ignored. Define whether both are logged, whether they have different metrics, and whether out-of-scope events are auditable.

### L-004: Transition verification after mutation is missing

The specification requires a transition attempt but does not require re-reading the parent to verify the final status. Add postcondition verification and define behavior if Jira reports success but the status remains unchanged.

### L-005: Notification failure is not a separate outcome

The acceptance criteria treat notification as part of transition failure but do not define whether a successful transition with failed notification is success, partial success, or failure requiring escalation.

### L-006: Date and time representation are unspecified

Execution logs, comments, idempotency keys, and scheduled refreshes need a timezone and timestamp format. Use UTC for stored and machine-readable values unless a Jira-local display timezone is explicitly required.

### L-007: Change compatibility is not defined

The spec does not say how existing manual transitions, other Jira Automation rules, or workflow post-functions interact with this automation. Conflicting automations could cause loops or repeated reopen/close events.

### L-008: Rollback and disable behavior are incomplete

The rollout section says to disable during workflow migrations but does not define how to stop in-flight work, reconcile pending idempotency records, or roll back a partially enabled rule.

### L-009: Confluence is not addressed

The constitution applies to Jira/Confluence automation, but this feature specification has no Confluence behavior. State explicitly that Confluence is not involved in this feature or define any required page/comment synchronization.

## 5. Recommended Clarification Order

Resolve these decisions in order because later choices depend on earlier ones:

1. Define the implementation model in the technical plan; this feature specification does not select it.
2. Define the idempotency and concurrency model, including partial failures.
3. Decide whether daily refresh is required and specify its schedule and scope.
4. Define authentication, permissions, retry policy, logging schema, and notification guarantees.
5. Define reproducible test fixtures and live-Jira versus mocked test boundaries.
6. Configure and validate suitable workflow transitions during implementation and deployment.
7. Add application API/UI requirements if the feature is implemented through the React/Express/PostgreSQL system.
8. Assign operational ownership, escalation, rollout, and rollback procedures.

## 6. Suggested Decisions to Record

Before moving to a technical plan, the specification should contain explicit answers to at least these questions:

- Which system is the source of truth for execution state and idempotency, as determined by the technical plan?
- What evidence will confirm that suitable close and reopen transitions are configured before production enablement?
- Is the daily refresh part of version 1, and what is its schedule and timezone?
- What happens when two events target the same parent concurrently?
- What happens after an external call times out with an unknown result?
- How are repeated failure notifications deduplicated?
- Where can an operator inspect logs and retry or reconcile a failed execution?
- What evidence is required before the rule is enabled in production?
