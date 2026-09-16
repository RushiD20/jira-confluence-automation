# Implementation Plan: Close Parent When Sub-Tasks Finish

**Status:** Draft  
**Date:** 2026-09-16  
**Source specification:** [specification.md](specification.md)  
**Constitution:** [constitution.md](constitution.md)  
**Clarifications:** [clarify.md](clarify.md)

## 1. Plan Objective

Implement and safely roll out automation for Jira project `ARE` that:

- Transitions an eligible parent to its configured Done target when all sub-tasks are Done.
- Reopens a Done parent when a sub-task leaves Done.
- Ignores unrelated events and parents without sub-tasks.
- Prevents duplicate transitions, marker comments, and failure notifications.
- Produces searchable execution records and actionable failure comments.
- Passes controlled acceptance tests before production enablement.

The feature specification intentionally leaves the implementation model and exact Jira workflow identifiers to this plan and deployment configuration.

## 2. Delivery Strategy

Work proceeds through gated phases. A phase is complete only when its milestone exit criteria are met. No production configuration is enabled before the access, workflow, idempotency, testing, and ownership gates pass.

### Recommended architecture decision

Use the existing Node.js/Express/PostgreSQL application as the durable orchestration boundary unless the project owner explicitly approves a native Jira Automation implementation with a documented constitution exception. The application-backed option best satisfies the constitution’s requirements for typed service boundaries, durable idempotency, structured logs, retries, and independently testable business rules.

Native Jira Automation remains a valid alternative only if Phase 0 documents how it satisfies or formally excepts the constitution’s PostgreSQL, typed-service, and structured-observability requirements.

## 3. Phase Overview

| Phase | Name | Primary outcome | Milestone |
|---|---|---|---|
| 0 | Architecture and scope gate | Implementation ownership is selected and recorded | M0: Approved technical direction |
| 1 | Access and workflow discovery | Jira access, permissions, parent types, and workflow behavior are verified | M1: Integration prerequisites approved |
| 2 | Contracts and operational design | Event, state, idempotency, logging, retry, and configuration contracts are defined | M2: Design ready for implementation |
| 3 | Event qualification and evaluation | Close and reopen decision logic is implemented and unit-tested | M3: Core behavior complete |
| 4 | Side effects and reliability | Jira mutations, idempotency, retries, diagnostics, and audit records are safe | M4: Reliable automation complete |
| 5 | Integration and acceptance testing | Controlled Jira scenarios pass without duplicate side effects | M5: Release candidate approved |
| 6 | Deployment and controlled rollout | Automation is enabled safely for the agreed scope | M6: Production rollout complete |
| 7 | Operations and maintenance | Monitoring, ownership, and workflow-change procedures are active | M7: Operational handoff complete |

## 4. Phase 0: Architecture and Scope Gate

### Objectives

Resolve the implementation boundary that the feature specification intentionally leaves open.

### Tasks

1. Review the constitution and choose one implementation model:
   - Application-backed orchestration using the Node.js/Express service and PostgreSQL.
   - Native Jira Automation only.
   - Hybrid event forwarding and orchestration.
2. Record the decision, owner, rationale, and any constitution exception.
3. Assign ownership for Jira configuration, application code, production enablement, and operational monitoring.
4. Confirm whether the daily refresh is part of version 1 or deferred.
5. Confirm whether Confluence is unrelated to this feature and document that boundary.

### Milestone M0: Approved technical direction

Exit criteria:

- Architecture decision record is approved.
- Component ownership for triggers, evaluation, persistence, side effects, and logs is explicit.
- Any constitution exception includes rationale, scope, owner, and review date.
- Daily refresh scope is marked required or deferred.
- Operational owners are named.

## 5. Phase 1: Access and Workflow Discovery

### Objectives

Verify the external conditions required to configure and test the feature. Exact transition identifiers are deployment details, but they must be discovered and validated before rollout.

### Tasks

1. Verify access to `https://epam.atlassian.net` and project `ARE`.
2. Confirm the rule actor or integration identity can browse issues, read parent/sub-task relationships, add comments, transition parents, and notify assignees.
3. List all eligible parent issue types and exclude types with incompatible lifecycle rules.
4. Confirm the sub-task issue type and parent relationship behavior.
5. Identify the Done status category as the authoritative completion signal.
6. Identify a suitable close transition and target Done status for each supported parent type.
7. Identify a suitable reopen transition and target status for each supported parent type.
8. Confirm how Jira Automation exposes transition source/destination status and parent sub-tasks.
9. Confirm Jira comment mention syntax and notification behavior for assigned users.
10. Record workflow and permission evidence in implementation documentation.

### Milestone M1: Integration prerequisites approved

Exit criteria:

- Project and workflow access is verified by the responsible owner.
- Eligible parent types and sub-task behavior are documented.
- Close and reopen transitions are validated in the current workflow for each supported type.
- Required permissions and notification behavior are demonstrated.
- Any unavailable prerequisite has an owner and a blocking status.

## 6. Phase 2: Contracts and Operational Design

### Objectives

Define the behavior needed to satisfy the constitution and make retries, failures, and operations testable.

### Tasks

1. Define the inbound event contract, including event ID, issue key, parent key, source status category, destination status category, timestamp, and correlation ID.
2. Define the evaluation result model:
   - `action_required`
   - `success`
   - `noop`
   - `ignored`
   - `retryable_failure`
   - `terminal_failure`
   - `partial_success`
3. Define the idempotency key from stable event and target-parent fields.
4. Define the idempotency state machine and handling for ambiguous external-call timeouts.
5. Define per-parent concurrency control and re-read points before mutation.
6. Define exact close, reopen, and diagnostic comment templates with stable markers.
7. Define diagnostic-comment and notification deduplication rules.
8. Define retry classes, exponential backoff, jitter, maximum attempts, `Retry-After` handling, and terminal recovery behavior.
9. Define the execution log schema, including correlation ID, idempotency key, parent key, trigger, decision, outcome, attempt count, error class, and timestamps.
10. Define configuration for project key, status categories, transition mappings, schedule, retry limits, and marker templates.
11. Define secret handling, Jira authentication, log redaction, retention, and access control.
12. Define the test fixture model and live-Jira versus mocked integration boundaries.

### Application-backed deliverables

- Typed Jira client contract.
- Evaluation service contract.
- Idempotency repository contract.
- Execution log repository contract.
- Configuration schema with startup validation.
- Database migration for execution/idempotency state, if required by the architecture decision.

### Native Jira Automation deliverables

- Rule or rule-pair design showing triggers, conditions, branches, actions, and error paths.
- Documented limitations and approved constitution exceptions.
- Searchable marker and execution-log strategy using Jira-supported capabilities.
- Explicit retry and duplicate-prevention behavior supported by the rule builder.

### Milestone M2: Design ready for implementation

Exit criteria:

- Event, evaluation, idempotency, retry, comment, notification, and logging contracts are approved.
- Concurrency and partial-side-effect behavior is documented.
- Configuration and secret requirements are defined.
- Test fixtures and acceptance-environment reset procedures are reproducible.

## 7. Phase 3: Event Qualification and Evaluation

### Objectives

Implement the pure decision logic that determines whether a parent should close, reopen, remain unchanged, or be ignored.

### Tasks

1. Implement project, issue-type, parent, and transition qualification.
2. Implement retrieval of the complete parent sub-task set, including pagination or an explicit native-rule equivalent.
3. Treat Jira’s Done status category as the completion authority.
4. Return a no-op when the parent has no sub-tasks.
5. Return a no-op when any sub-task is not Done during close evaluation.
6. Return a no-op when the parent is already Done during close evaluation.
7. Return a no-op when the parent is not Done during reopen evaluation.
8. Trigger close only for a transition into Done.
9. Trigger reopen only for a transition from Done to non-Done.
10. Return an ignored result for non-`ARE`, non-sub-task, orphaned, or otherwise out-of-scope events.
11. Add unit tests for every acceptance scenario and edge-case table row.

### Milestone M3: Core behavior complete

Exit criteria:

- Decision logic has no direct UI or route-handler dependencies.
- Unit tests cover close, reopen, no-op, ignored, and malformed-input paths.
- All test cases assert both decision and reason.
- No external mutation occurs in the evaluation layer.

## 8. Phase 4: Side Effects and Reliability

### Objectives

Connect the decision logic to Jira while preserving idempotency, auditability, and recoverability.

### Tasks

1. Re-read the parent and relevant sub-tasks immediately before mutation.
2. Acquire the per-parent idempotency/concurrency guard.
3. Check for an existing matching action or diagnostic marker.
4. Persist or register the execution attempt using the selected idempotency strategy.
5. Add the exact close or reopen marker before the transition when required by the configured design.
6. Execute the configured and validated Jira transition.
7. Re-read the parent and verify the expected postcondition.
8. Record success only after the expected state is confirmed.
9. Handle missing transitions and transition failures through the diagnostic-comment path.
10. Deduplicate diagnostic comments and notifications for repeated failures.
11. Classify transient, permission, validation, rate-limit, and terminal errors.
12. Apply bounded retries with backoff for retryable failures.
13. Reconcile ambiguous timeouts by reading current Jira state before retrying a mutation.
14. Ensure secrets and sensitive issue data are redacted from logs.
15. Add integration tests using Jira client mocks and database fixtures where applicable.

### Daily refresh path

If Phase 0 includes the daily refresh:

1. Define the parent selection query and pagination.
2. Use the same evaluation and idempotency services as event-driven processing.
3. Prevent overlapping refresh runs.
4. Use UTC for stored timestamps and document the operational timezone.
5. Record run-level and parent-level outcomes.
6. Ensure already-correct parents produce no duplicate side effects.

### Milestone M4: Reliable automation complete

Exit criteria:

- Close and reopen side effects are idempotent under retries.
- Concurrent evaluations cannot create duplicate transitions or markers.
- Partial failures and ambiguous timeouts have defined recovery behavior.
- Expected postconditions are verified after transitions.
- Structured execution records are searchable and redacted.
- Automated unit and integration tests pass.

## 9. Phase 5: Integration and Acceptance Testing

### Objectives

Prove the feature against a controlled Jira setup before production enablement.

### Test preparation

1. Create or select a dedicated `ARE` test parent.
2. Create several sub-tasks with known initial statuses.
3. Record parent type, workflow, assignee, issue keys, and reset procedure.
4. Disable unrelated automations that could interfere with the test or document their expected interactions.
5. Ensure test credentials and notifications cannot affect unintended users.

### Required acceptance tests

- Complete one of several sub-tasks; parent remains unchanged.
- Complete the final remaining sub-task; parent moves to the configured Done target.
- Evaluate a parent with no sub-tasks; no action occurs.
- Move a sub-task out of Done while parent is Done; parent follows the configured reopen transition.
- Replay the same event; no duplicate transition or marker occurs.
- Trigger a failing or unavailable transition; diagnostic comment and notification behavior match the contract.
- Trigger from a project other than `ARE`; event is ignored.
- Trigger from a non-sub-task; event is ignored.
- Review logs; success, no-op, ignored, retryable failure, and terminal failure are distinguishable.
- Run the daily refresh, if enabled, against already-correct parents; no duplicate side effects occur.

### Additional reliability tests

- Two qualifying events for the same parent arrive concurrently.
- Jira returns a timeout after a transition may have succeeded.
- Marker comment succeeds but transition fails.
- Transition succeeds but diagnostic or notification follow-up fails.
- Jira returns 429 and honors `Retry-After`.
- Jira returns a permission error.
- Parent or sub-task data is missing, archived, deleted, or incomplete.
- The parent is reassigned while an execution is in progress.
- A workflow mapping is missing or ambiguous.

### Milestone M5: Release candidate approved

Exit criteria:

- All acceptance tests pass in the controlled environment.
- Reliability and failure-path tests pass or have approved exceptions.
- Jira issue history and execution records match expected outcomes.
- No duplicate transitions, markers, or notifications are observed.
- Project owner signs off on the release candidate.

## 10. Phase 6: Deployment and Controlled Rollout

### Objectives

Enable the automation with a reversible, observable rollout.

### Tasks

1. Validate production configuration without logging secrets.
2. Confirm project access, rule actor permissions, workflow mappings, and notification behavior again.
3. Deploy application changes and database migrations, if selected.
4. Configure the native rule or webhook integration, if selected.
5. Keep the automation disabled until the final checklist is approved.
6. Enable it first for the dedicated test parent or smallest agreed scope.
7. Monitor the first successful close, no-op, reopen, and failure-recovery cases.
8. Compare execution records with Jira issue history.
9. Expand to all eligible `ARE` parents only after the controlled rollout is clean.
10. Record the deployed configuration version and workflow mapping evidence.

### Rollback and disablement

- Disable event triggers and scheduled refresh before changing workflow mappings.
- Stop new processing while allowing or cancelling in-flight work according to the selected architecture.
- Reconcile pending idempotency records and ambiguous external calls by reading Jira state.
- Restore the last known-good configuration or application version.
- Record the reason, affected parents, and manual recovery actions.

### Milestone M6: Production rollout complete

Exit criteria:

- Production enablement is approved by the project owner.
- Initial controlled rollout is successful.
- Monitoring and escalation contacts are active.
- Rollback and disable procedures have been verified.
- Final configuration and workflow evidence are recorded.

## 11. Phase 7: Operations and Maintenance

### Objectives

Keep the automation reliable as Jira workflows, permissions, and integrations change.

### Tasks

1. Review successful, no-op, ignored, and failed execution records on an agreed cadence.
2. Monitor rate limits, retries, unresolved failures, and notification failures.
3. Maintain the test fixture and rerun the acceptance suite after workflow changes.
4. Revalidate transitions, status categories, issue types, permissions, and mention behavior after Jira changes.
5. Keep the automation disabled during major workflow migrations.
6. Document incidents, manual recoveries, and configuration changes.
7. Review secret rotation and access permissions.
8. Retire stale idempotency records according to the retention policy.

### Milestone M7: Operational handoff complete

Exit criteria:

- Named owner and escalation path are documented.
- Monitoring queries or dashboards are available.
- Runbook covers common failures and manual recovery.
- Workflow-change revalidation procedure is agreed.
- First post-rollout review is complete.

## 12. Cross-Phase Quality Gates

Every implementation change MUST satisfy the following gates before advancing:

- Specification behavior and acceptance criteria remain traceable to the implementation.
- Type checking, linting, focused unit tests, integration tests, and build checks pass where applicable.
- No secrets or sensitive issue content are exposed in source, comments, or ordinary logs.
- Jira mutations are behind the approved service or rule boundary.
- No-op, ignored, success, retryable failure, terminal failure, and partial-success outcomes are distinguishable.
- Idempotency and concurrency tests cover repeated and simultaneous events.
- Documentation is updated when configuration, workflows, permissions, or operational ownership changes.

## 13. Key Deliverables

- Architecture decision and any constitution exception.
- Workflow and permission validation record.
- Typed integration and evaluation contracts, or native-rule configuration document.
- Idempotency, retry, logging, and comment-template design.
- Configuration schema and deployment instructions.
- Database migration and repository implementation, if application-backed.
- Unit, integration, reliability, and acceptance test artifacts.
- Controlled rollout checklist and rollback procedure.
- Operations runbook and ownership record.

## 14. Open Plan Decisions

These items must be resolved at the indicated phase:

| Decision | Owner phase | Required outcome |
|---|---|---|
| Native, application-backed, or hybrid implementation | Phase 0 | Approved architecture decision |
| Daily refresh in version 1 | Phase 0 | Required or deferred |
| Eligible parent issue types | Phase 1 | Explicit allowlist |
| Close and reopen transition mappings | Phase 1 / deployment | Validated configuration |
| Idempotency store and concurrency strategy | Phase 2 | Approved state machine and locking model |
| Retry and rate-limit policy | Phase 2 | Error classification and bounded retry rules |
| Execution log destination and retention | Phase 2 | Searchable, redacted log contract |
| Acceptance test fixture and reset process | Phase 2 / Phase 5 | Reproducible test setup |
| Production owner and escalation path | Phase 0 / Phase 6 | Named operational ownership |
