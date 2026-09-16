# Implementation Tasks: Close Parent When Sub-Tasks Finish

**Status:** Ready for sequencing  
**Date:** 2026-09-16  
**Source plan:** [plan.md](plan.md)  
**Source specification:** [specification.md](specification.md)

## Task Conventions

- `[ ]` means not started.
- Tasks are ordered by dependency within each phase.
- A task is complete only when its acceptance criteria pass and the result is recorded.
- Tasks marked **Conditional** are executed only when the Phase 0 architecture or daily-refresh decision requires them.

## Phase 0: Architecture and Scope Gate

### T-001: Choose implementation architecture

**Dependencies:** None  
**Owner:** Project owner and technical lead

Evaluate application-backed, native Jira Automation, and hybrid options against the constitution and plan. Select one implementation model.

**Acceptance criteria:** An approved architecture decision identifies the component responsible for triggers, evaluation, persistence, idempotency, Jira mutations, retries, and logs.

### T-002: Record architecture rationale and exceptions

**Dependencies:** T-001  
**Owner:** Technical lead

Document the selected architecture, tradeoffs, constraints, and any constitution exception.

**Acceptance criteria:** The decision record contains rationale, scope, owner, review date, and an explicit list of any constitution principles not satisfied directly.

### T-003: Assign feature ownership

**Dependencies:** T-001  
**Owner:** Project owner

Assign owners for Jira configuration, application implementation, production enablement, monitoring, and incident escalation.

**Acceptance criteria:** Every operational responsibility has one named owner and one escalation path in the project documentation.

### T-004: Decide daily refresh scope

**Dependencies:** T-001  
**Owner:** Project owner and technical lead

Decide whether the daily refresh is part of version 1 or deferred.

**Acceptance criteria:** The decision is recorded as `required` or `deferred`; if required, the decision includes the initial schedule owner and delivery milestone.

### T-005: Confirm Confluence boundary

**Dependencies:** T-001  
**Owner:** Technical lead

Confirm that this feature does not create or update Confluence content, or document the required Confluence behavior.

**Acceptance criteria:** The feature boundary explicitly states whether Confluence is excluded or lists the required Confluence contracts and acceptance tests.

### M-0: Approved Technical Direction

**Milestone acceptance criteria:** T-001 through T-005 are complete; architecture, ownership, daily refresh scope, and Confluence boundary are approved.

## Phase 1: Access and Workflow Discovery

### T-006: Verify Jira site and project access

**Dependencies:** T-003  
**Owner:** Jira administrator

Verify access to `https://epam.atlassian.net` and project `ARE` using the intended configuration account.

**Acceptance criteria:** The account can open project `ARE`, browse a representative parent and sub-task, and the evidence is recorded without exposing credentials.

### T-007: Verify rule actor permissions

**Dependencies:** T-006  
**Owner:** Jira administrator

Verify browse, issue-read, comment, transition, mention, notification, and execution-log permissions.

**Acceptance criteria:** A permission checklist records pass/fail evidence for every required permission and identifies an owner for each failure.

### T-008: Identify supported parent issue types

**Dependencies:** T-006  
**Owner:** Jira administrator and product owner

List the parent issue types included in the feature and exclude incompatible types.

**Acceptance criteria:** An explicit allowlist of supported parent issue types and an exclusion list are recorded.

### T-009: Confirm sub-task relationship behavior

**Dependencies:** T-006, T-008  
**Owner:** Jira administrator

Confirm the sub-task type, parent field, orphan behavior, and issue types that can contain sub-tasks.

**Acceptance criteria:** A representative sub-task exposes the expected parent reference, and orphaned or invalid relationships have documented behavior.

### T-010: Confirm Done status-category authority

**Dependencies:** T-008  
**Owner:** Jira administrator

Verify that the feature uses Jira’s Done status category rather than a hard-coded status name as the completion authority.

**Acceptance criteria:** The configured status-category identifier or native-rule condition is recorded, and at least one Done and non-Done status are verified.

### T-011: Validate close transition configuration

**Dependencies:** T-008, T-010  
**Owner:** Jira administrator

For every supported parent type, identify and validate a transition to the configured Done target.

**Acceptance criteria:** Each supported parent type has one unambiguous close transition, target status, and permission check recorded in deployment configuration documentation.

### T-012: Validate reopen transition configuration

**Dependencies:** T-008, T-010  
**Owner:** Jira administrator

For every supported parent type, identify and validate a transition from Done to the approved reopen target.

**Acceptance criteria:** Each supported parent type has one unambiguous reopen transition, target status, and permission check recorded in deployment configuration documentation.

### T-013: Validate transition event data

**Dependencies:** T-006, T-010  
**Owner:** Technical implementer

Confirm the selected trigger mechanism exposes issue key, project, issue type, parent, source status category, destination status category, event ID, and event timestamp.

**Acceptance criteria:** A captured test payload or native-rule mapping demonstrates every required field and documents unavailable fields.

### T-014: Validate comment mention and notification behavior

**Dependencies:** T-007  
**Owner:** Jira administrator

Confirm the supported assignee mention syntax and whether the configured comment action notifies the assignee.

**Acceptance criteria:** A controlled test comment reaches the intended test user, and behavior for unassigned or inactive assignees is documented.

### T-015: Record integration prerequisites

**Dependencies:** T-006 through T-014  
**Owner:** Technical lead

Consolidate access, workflow, issue-type, transition, event, and notification evidence.

**Acceptance criteria:** The prerequisite record shows all required checks passing or identifies explicitly approved blockers with owners and next actions.

### M-1: Integration Prerequisites Approved

**Milestone acceptance criteria:** T-006 through T-015 are complete; access, permissions, supported issue types, event data, and workflow configuration are approved.

## Phase 2: Contracts and Operational Design

### T-016: Define inbound event contract

**Dependencies:** T-001, T-013  
**Owner:** Technical implementer

Define the event schema, validation rules, event ID, issue and parent keys, status categories, timestamp, source, and correlation ID.

**Acceptance criteria:** Valid and invalid example payloads are documented, and malformed events have an explicit rejection outcome.

### T-017: Define evaluation result model

**Dependencies:** T-016  
**Owner:** Technical implementer

Define `action_required`, `success`, `noop`, `ignored`, `retryable_failure`, `terminal_failure`, and `partial_success` with required fields.

**Acceptance criteria:** Every result has a machine-readable code, human-readable reason, target parent when known, and logging behavior.

### T-018: Define idempotency key

**Dependencies:** T-016, T-017  
**Owner:** Technical implementer

Define stable idempotency keys for close actions, reopen actions, scheduled evaluations, and diagnostic notifications.

**Acceptance criteria:** The key derivation is deterministic, collision-resistant for the target scope, and covered by duplicate-event examples.

### T-019: Define idempotency state machine

**Dependencies:** T-018  
**Owner:** Technical implementer

Define states and transitions for received, evaluating, marker-written, transition-attempted, transitioned, failed, and reconciled executions.

**Acceptance criteria:** The design specifies retry behavior for every state, including an external-call timeout with unknown outcome.

### T-020: Define concurrency strategy

**Dependencies:** T-019  
**Owner:** Technical implementer

Define per-parent locking or serialization, re-read points, conflict handling, and maximum concurrent work.

**Acceptance criteria:** Two simultaneous events for one parent have a deterministic outcome with at most one intended transition and one marker.

### T-021: Define comment templates

**Dependencies:** T-014, T-019  
**Owner:** Technical implementer and product owner

Define exact close, reopen, diagnostic, and manual-recovery comment templates with stable markers.

**Acceptance criteria:** Templates include required identifiers and safe error text, have duplicate-detection rules, and pass examples for close, reopen, and failure cases.

### T-022: Define retry and rate-limit policy

**Dependencies:** T-017, T-019  
**Owner:** Technical implementer

Classify 429, 5xx, network timeout, permission, validation, and invalid-transition errors. Define backoff, jitter, maximum attempts, `Retry-After`, and terminal handling.

**Acceptance criteria:** A policy table maps every error class to retry, reconciliation, escalation, or terminal-failure behavior.

### T-023: Define execution log contract

**Dependencies:** T-017, T-018  
**Owner:** Technical implementer and operations owner

Define log fields, correlation IDs, outcome values, error classification, timestamps, redaction, retention, and access control.

**Acceptance criteria:** A sample log record supports searching by parent key, event ID, idempotency key, outcome, and time range without exposing secrets.

### T-024: Define runtime configuration

**Dependencies:** T-011, T-012, T-022  
**Owner:** Technical implementer

Define project key, status-category configuration, transition mappings, schedule, retry limits, marker templates, and environment validation.

**Acceptance criteria:** Configuration has documented required fields, safe defaults, startup validation, and a non-secret example file.

### T-025: Define security and privacy controls

**Dependencies:** T-016, T-023, T-024  
**Owner:** Technical lead

Define credential storage, least-privilege access, webhook authentication if applicable, replay protection, redaction, and audit access.

**Acceptance criteria:** The design states how unauthorized input, secret rotation, sensitive log fields, and retention are handled.

### T-026: Define test fixture and environment strategy

**Dependencies:** T-016 through T-025  
**Owner:** Test lead

Define mocked Jira payloads, database fixtures, live-Jira scenarios, notification isolation, and environment reset procedures.

**Acceptance criteria:** A new tester can recreate the controlled test setup from the documented fixture and reset instructions.

### M-2: Design Ready for Implementation

**Milestone acceptance criteria:** T-016 through T-026 are approved; contracts, idempotency, reliability, security, logging, configuration, and test strategy are complete.

## Phase 3: Event Qualification and Evaluation

### T-027: Implement input validation and scope guards

**Dependencies:** T-016, T-017  
**Owner:** Application implementer or rule configurator

Implement project, issue-type, parent, event-direction, and required-field validation.

**Acceptance criteria:** Out-of-scope, malformed, non-sub-task, orphaned, and unsupported events return the documented ignored or rejected result without side effects.

### T-028: Implement complete sub-task evaluation

**Dependencies:** T-009, T-010, T-016  
**Owner:** Application implementer or rule configurator

Retrieve or evaluate the complete parent sub-task collection, including pagination or the native-rule equivalent.

**Acceptance criteria:** A parent with multiple pages of sub-tasks is evaluated using all sub-tasks, and incomplete data cannot produce a false close.

### T-029: Implement close decision logic

**Dependencies:** T-027, T-028  
**Owner:** Application implementer or rule configurator

Implement the all-Done, at-least-one-sub-task, and parent-not-Done guards.

**Acceptance criteria:** The evaluator requests a close only when every sub-task is Done, at least one sub-task exists, and the parent is not Done.

### T-030: Implement reopen decision logic

**Dependencies:** T-027, T-028  
**Owner:** Application implementer or rule configurator

Implement the source-Done-to-non-Done and parent-currently-Done guards.

**Acceptance criteria:** The evaluator requests a reopen only when the triggering sub-task leaves Done and its parent is currently Done.

### T-031: Implement no-op and ignored reasons

**Dependencies:** T-029, T-030  
**Owner:** Application implementer or rule configurator

Return explicit reasons for no sub-tasks, incomplete sub-tasks, parent already Done, parent not Done, and out-of-scope events.

**Acceptance criteria:** Every no-op and ignored result includes a stable reason code and is distinguishable in tests and logs.

### T-032: Add decision-layer unit tests

**Dependencies:** T-027 through T-031  
**Owner:** Test lead

Test all user scenarios, edge-case rows, malformed input, and transition-direction combinations without external mutations.

**Acceptance criteria:** Unit tests pass and assert both the result code and reason for close, reopen, no-op, ignored, and invalid inputs.

### M-3: Core Behavior Complete

**Milestone acceptance criteria:** T-027 through T-032 are complete; evaluation is isolated from side effects and all decision tests pass.

## Phase 4: Side Effects and Reliability

### T-033: Implement pre-mutation re-read

**Dependencies:** T-019, T-029, T-030  
**Owner:** Application implementer or rule configurator

Re-read the parent and relevant sub-tasks immediately before a Jira mutation.

**Acceptance criteria:** A stale initial evaluation cannot transition a parent after the current Jira state no longer satisfies the decision.

### T-034: Implement idempotency and concurrency guard

**Dependencies:** T-018 through T-020  
**Owner:** Application implementer or rule configurator

Acquire the selected per-parent guard and reject or coalesce duplicate logical events.

**Acceptance criteria:** Concurrent duplicate events produce at most one intended transition and one marker, and the final execution records explain the coalescing.

### T-035: Implement execution registration

**Dependencies:** T-019, T-023, T-034  
**Owner:** Application implementer or rule configurator

Register execution attempts and state changes in PostgreSQL or the approved native Jira mechanism.

**Acceptance criteria:** Every accepted event has a traceable execution record with its idempotency key and current state.

### T-036: Implement marker comment handling

**Dependencies:** T-021, T-034  
**Owner:** Application implementer or rule configurator

Write and detect exact close and reopen markers according to the approved ordering and deduplication rules.

**Acceptance criteria:** A retry detects an existing matching marker and does not create a duplicate marker for the same logical action.

### T-037: Implement Jira transition execution

**Dependencies:** T-011, T-012, T-033 through T-036  
**Owner:** Application implementer or rule configurator

Execute the configured close or reopen transition through the selected Jira integration boundary.

**Acceptance criteria:** A qualifying close or reopen decision invokes only its configured transition and records the external result.

### T-038: Implement post-transition verification

**Dependencies:** T-037  
**Owner:** Application implementer or rule configurator

Re-read the parent after a successful transition response and verify the expected status category or target status.

**Acceptance criteria:** Execution is marked successful only when the expected postcondition is observed; an inconsistent result is classified and recoverable.

### T-039: Implement diagnostic comments and notifications

**Dependencies:** T-014, T-021, T-037  
**Owner:** Application implementer or rule configurator

Handle missing/failed transitions with deduplicated diagnostic comments, assignee mentions, and notification results.

**Acceptance criteria:** A forced transition failure creates the exact diagnostic comment once per failure key, records notification outcome, and provides manual recovery instructions.

### T-040: Implement retry and reconciliation handling

**Dependencies:** T-019, T-022, T-037, T-038  
**Owner:** Application implementer

Apply bounded retries and reconcile Jira state after ambiguous timeouts before retrying mutations.

**Acceptance criteria:** 429 and transient 5xx responses follow the policy, while permission and invalid-transition errors do not retry indefinitely.

### T-041: Implement redacted structured logging

**Dependencies:** T-023, T-025, T-035  
**Owner:** Application implementer

Emit searchable logs for success, no-op, ignored, retryable failure, terminal failure, and partial success.

**Acceptance criteria:** Logs include required correlation fields and contain no credentials, tokens, or unapproved sensitive issue content.

### T-042: Implement daily refresh

**Dependencies:** T-004, T-028 through T-041  
**Owner:** Application implementer or rule configurator  
**Condition:** Execute only if daily refresh is required.

Implement the scheduled parent selection, pagination, overlap prevention, UTC timestamps, and reuse of the event evaluation path.

**Acceptance criteria:** An enabled refresh evaluates the configured scope, records run and parent outcomes, and produces no duplicate side effects for already-correct parents.

### T-043: Add reliability and integration tests

**Dependencies:** T-033 through T-042  
**Owner:** Test lead

Test concurrency, retries, timeouts, partial side effects, rate limits, permission failures, missing data, reassignment, and ambiguous mappings.

**Acceptance criteria:** Tests pass for each required failure path or an approved exception records the remaining risk and manual control.

### M-4: Reliable Automation Complete

**Milestone acceptance criteria:** T-033 through T-043 are complete; mutations are idempotent, concurrency-safe, postcondition-verified, retry-aware, observable, and tested.

## Phase 5: Integration and Acceptance Testing

### T-044: Provision controlled test parent

**Dependencies:** T-015, T-026  
**Owner:** Test lead and Jira administrator

Create or select a dedicated `ARE` parent, sub-tasks, assignee, statuses, and reset procedure.

**Acceptance criteria:** The fixture has documented issue keys, parent type, workflow, starting states, test user, and a repeatable reset process.

### T-045: Isolate interfering automations

**Dependencies:** T-044  
**Owner:** Jira administrator

Disable unrelated automations for the test scope or document their expected effects.

**Acceptance criteria:** The test run identifies all active rules affecting the fixture and demonstrates that results are attributable to this feature.

### T-046: Run close-path acceptance tests

**Dependencies:** T-044, T-045, M-4  
**Owner:** Test lead

Run partial completion, final completion, no-sub-task, already-Done, and out-of-scope close scenarios.

**Acceptance criteria:** All close-path expectations in AT-001 through AT-003 and AT-007 through AT-008 pass with matching issue history and logs.

### T-047: Run reopen-path acceptance tests

**Dependencies:** T-044, T-045, M-4  
**Owner:** Test lead

Move a sub-task out of Done and verify the parent reopen behavior and no-op cases.

**Acceptance criteria:** AT-004 passes, and a sub-task leaving Done with a parent that is not Done produces no transition.

### T-048: Run duplicate and failure acceptance tests

**Dependencies:** T-044, T-045, M-4  
**Owner:** Test lead

Replay events, force transition failures, and inspect comments, notifications, and logs.

**Acceptance criteria:** AT-005, AT-006, and AT-009 pass without duplicate transitions, markers, or failure notifications.

### T-049: Run daily refresh acceptance test

**Dependencies:** T-004, T-042, T-044  
**Owner:** Test lead  
**Condition:** Execute only if daily refresh is enabled.

Run the refresh against already-correct and actionable parents.

**Acceptance criteria:** AT-010 passes, overlapping refresh behavior is safe, and run-level metrics are recorded.

### T-050: Obtain release-candidate sign-off

**Dependencies:** T-046 through T-049  
**Owner:** Project owner

Review test evidence, open exceptions, logs, issue history, and rollback readiness.

**Acceptance criteria:** The project owner signs off the release candidate or records blocking failures and required remediation.

### M-5: Release Candidate Approved

**Milestone acceptance criteria:** T-044 through T-050 are complete; all required acceptance tests pass, reliability risks are resolved or approved, and sign-off is recorded.

## Phase 6: Deployment and Controlled Rollout

### T-051: Validate production configuration

**Dependencies:** M-5  
**Owner:** Technical implementer and Jira administrator

Validate secrets, project key, status categories, transition mappings, retry settings, and notification configuration without exposing secret values.

**Acceptance criteria:** Production configuration validation passes and the deployed configuration version is recorded.

### T-052: Deploy application and database changes

**Dependencies:** T-051  
**Owner:** Application implementer  
**Condition:** Execute only for application-backed or hybrid architecture.

Deploy code, migrations, and runtime configuration using the approved release procedure.

**Acceptance criteria:** Health checks pass, migrations are applied successfully, and the service can read validated configuration.

### T-053: Configure native Jira rule or webhook integration

**Dependencies:** T-051  
**Owner:** Jira administrator  
**Condition:** Execute for native or hybrid architecture as applicable.

Configure triggers, conditions, branches, actions, error paths, and security settings.

**Acceptance criteria:** The configured rule or integration matches the approved design and remains disabled until the rollout checklist is approved.

### T-054: Execute controlled rollout

**Dependencies:** T-050 through T-053  
**Owner:** Project owner and operations owner

Enable the automation for the test parent or smallest agreed scope and observe representative close, no-op, reopen, and failure cases.

**Acceptance criteria:** Controlled rollout produces expected Jira states, comments, notifications, and execution records with no duplicate side effects.

### T-055: Expand to production scope

**Dependencies:** T-054  
**Owner:** Project owner

Enable the automation for all approved eligible `ARE` parents.

**Acceptance criteria:** Production enablement approval is recorded, the final scope is documented, and monitoring is active before expansion.

### T-056: Verify rollback and disablement

**Dependencies:** T-054  
**Owner:** Operations owner

Exercise or tabletop the procedure for disabling triggers, reconciling in-flight executions, restoring configuration, and recording manual recovery.

**Acceptance criteria:** The rollback procedure identifies who acts, what is disabled, how ambiguous executions are reconciled, and where the incident is recorded.

### M-6: Production Rollout Complete

**Milestone acceptance criteria:** T-051 through T-056 are complete; controlled rollout is clean, production approval is recorded, monitoring is active, and rollback is verified.

## Phase 7: Operations and Maintenance

### T-057: Publish operations runbook

**Dependencies:** M-6  
**Owner:** Operations owner

Document monitoring queries, common failures, retry/reconciliation actions, notification failures, and escalation contacts.

**Acceptance criteria:** An operator can diagnose a success, no-op, duplicate, rate-limit, permission, transition, and notification failure using the runbook.

### T-058: Establish monitoring review cadence

**Dependencies:** T-057  
**Owner:** Operations owner

Set the review cadence and thresholds for failures, retries, unresolved notifications, rate limits, and refresh failures.

**Acceptance criteria:** A scheduled review exists with named participants, alert thresholds, and an escalation path.

### T-059: Maintain workflow-change validation

**Dependencies:** T-057  
**Owner:** Jira administrator

Define revalidation after status, transition, issue-type, permission, notification, or automation changes.

**Acceptance criteria:** A workflow change checklist requires disabling the automation where appropriate and rerunning the relevant acceptance tests before re-enablement.

### T-060: Manage retention and secret rotation

**Dependencies:** T-023, T-025, T-057  
**Owner:** Operations owner and security owner

Apply execution-record retention, idempotency cleanup, log-redaction review, and credential rotation procedures.

**Acceptance criteria:** Retention and rotation dates are documented, completed actions are auditable, and no expired credential or stale record remains active beyond policy.

### T-061: Complete operational handoff

**Dependencies:** T-057 through T-060  
**Owner:** Project owner

Review monitoring, ownership, incident response, test fixture maintenance, and workflow-change procedures.

**Acceptance criteria:** The named operations owner accepts the handoff and the first post-rollout review is scheduled.

### M-7: Operational Handoff Complete

**Milestone acceptance criteria:** T-057 through T-061 are complete; runbook, monitoring, ownership, retention, and change-management processes are active.

## Definition of Done

The implementation is complete only when:

- [ ] The architecture and any constitution exception are approved.
- [ ] Jira access, permissions, supported parent types, event data, and workflow configuration are verified.
- [ ] Contracts for events, results, idempotency, retries, comments, logs, configuration, and security are approved.
- [ ] Close, reopen, no-op, ignored, and malformed-input behavior is implemented and unit-tested.
- [ ] Jira mutations are idempotent, concurrency-safe, postcondition-verified, and retry-aware.
- [ ] Diagnostic comments, assignee notifications, and execution records meet the approved contracts.
- [ ] Required integration, reliability, and acceptance tests pass.
- [ ] Production rollout is controlled, observable, approved, and reversible.
- [ ] Operations ownership, monitoring, runbook, retention, and workflow-change validation are active.
