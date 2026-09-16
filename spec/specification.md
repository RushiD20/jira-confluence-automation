# Feature Specification: Close Parent When Sub-Tasks Finish

**Status:** Draft  
**Version:** 1.0.0  
**Date:** 2026-09-16  
**Target project:** Jira Cloud project `ARE`  
**Primary actor:** Jira Automation rule actor  
**Related constitution:** [constitution.md](constitution.md)

## 1. Overview

Create an idempotent Jira Cloud automation capability that keeps a parent issue's status aligned with the statuses of its sub-tasks. When every sub-task is in Jira's Done status category, the automation transitions the parent to `DONE`. If a completed sub-task later leaves the Done status category, the automation reopens the parent through the valid `ARE` workflow transition.

The capability must operate safely for event-driven transitions and an optional daily refresh. It must ignore out-of-scope issues, avoid duplicate actions, leave an audit trail, and provide an actionable notification when a required transition fails.

## 2. Goals

- Automatically close an eligible parent when all of its sub-tasks are Done.
- Reopen a Done parent when one of its sub-tasks leaves Done.
- Never close a parent that has no sub-tasks.
- Prevent duplicate transitions and duplicate idempotency comments.
- Provide searchable audit information for successful and failed evaluations.
- Notify the parent assignee when a required transition cannot be completed.
- Support controlled testing before production enablement.

## 3. Scope

### In scope

- Jira Cloud site `https://epam.atlassian.net`.
- Jira project `ARE`.
- Parent issue types that support sub-tasks.
- Jira sub-task issues with a parent.
- Event-driven evaluation after relevant sub-task transitions.
- Optional scheduled daily evaluation for missed events.
- Parent close and reopen transitions.
- Idempotency markers, diagnostic comments, and execution logging.
- Acceptance testing using a dedicated test parent and sub-tasks.

### Out of scope

- Changes to Jira workflows, statuses, permissions, or issue types.
- Processing issues outside project `ARE`.
- Closing parents solely because they have no sub-tasks.
- Replacing Jira's native issue history or execution logs.
- Automatic resolution of invalid or unavailable workflow transitions.
- Production rollout before access, permissions, workflow mappings, and acceptance tests are verified.

## 4. User Scenarios and Testing

### User Story 1: Close a parent after all sub-tasks finish

**Priority:** P1

As a project manager, I want a parent issue to transition to `DONE` automatically when every one of its sub-tasks reaches the Done status category, so that parent status reflects completed work without manual updates.

**Acceptance scenarios**

#### Scenario 1.1: Final sub-task reaches Done

- **Given** an issue belongs to project `ARE`, is a sub-task, and has a parent.
- **And** the parent has at least one sub-task.
- **And** all parent sub-tasks are in the Done status category after the transition.
- **And** the parent is not in the Done status category.
- **When** the sub-task transitions into the Done status category.
- **Then** the automation adds the close idempotency marker.
- **And** the automation transitions the parent using the validated `DONE` workflow transition.
- **And** the execution is recorded as successful.

#### Scenario 1.2: A remaining sub-task is not Done

- **Given** a sub-task transitions into the Done status category.
- **And** at least one other sub-task of the parent is not in the Done status category.
- **When** the automation evaluates the parent.
- **Then** the parent is not transitioned.
- **And** no close action is recorded as successful.
- **And** the evaluation is recorded as a deliberate no-op.

#### Scenario 1.3: Parent has no sub-tasks

- **Given** an eligible parent has no sub-tasks.
- **When** the automation evaluates the parent.
- **Then** the parent remains unchanged.
- **And** no close marker or transition is created.

### User Story 2: Reopen a parent when work resumes

**Priority:** P1

As a project manager, I want a Done parent to reopen when a sub-task leaves Done, so that incomplete work is visible again.

**Acceptance scenarios**

#### Scenario 2.1: Sub-task leaves Done

- **Given** an issue belongs to project `ARE`, is a sub-task, and has a parent.
- **And** the parent is currently in the Done status category.
- **And** the sub-task transitions from the Done status category to a non-Done status.
- **When** the automation evaluates the parent.
- **Then** the automation adds the reopen idempotency marker.
- **And** the automation performs the validated reopen transition.
- **And** the execution is recorded as successful.

#### Scenario 2.2: Parent is not Done

- **Given** a sub-task leaves the Done status category.
- **And** its parent is not in the Done status category.
- **When** the automation evaluates the parent.
- **Then** the parent is not transitioned.
- **And** the evaluation is recorded as a deliberate no-op.

### User Story 3: Retry safely without duplicate side effects

**Priority:** P1

As an operator, I want repeated events and scheduled refreshes to be safe, so that retries do not create duplicate transitions or comments.

**Acceptance scenarios**

#### Scenario 3.1: Close event is delivered more than once

- **Given** the parent is already in the Done status category.
- **When** the same close-triggering event is processed again.
- **Then** no additional transition is attempted.
- **And** no duplicate close marker is added.

#### Scenario 3.2: Daily refresh sees an already-correct parent

- **Given** all sub-tasks are Done and the parent is already in the target state.
- **When** the daily refresh evaluates the parent.
- **Then** the refresh performs no transition.
- **And** it does not duplicate an existing marker or diagnostic comment.

### User Story 4: Recover from a failed transition

**Priority:** P1

As the parent assignee, I want a clear diagnostic comment and notification when automation cannot transition the parent, so that I know what manual action is required.

**Acceptance scenarios**

#### Scenario 4.1: Close transition fails

- **Given** the close condition is satisfied.
- **And** the configured close transition is unavailable or fails.
- **When** the automation attempts the close action.
- **Then** it adds a diagnostic comment to the parent.
- **And** the comment identifies the satisfied sub-task condition.
- **And** the comment includes the attempted transition, failure reason when available, and required manual action.
- **And** the comment mentions the parent assignee.
- **And** Jira sends the corresponding notification.
- **And** the execution is recorded as failed.

#### Scenario 4.2: Reopen transition is unavailable

- **Given** a sub-task leaves Done while its parent is Done.
- **And** no valid reopen transition exists in the current `ARE` workflow.
- **When** the automation evaluates the parent.
- **Then** it does not invent or apply an unvalidated transition.
- **And** it adds a diagnostic comment with the missing-transition condition and required manual action.
- **And** it mentions and notifies the parent assignee.

### User Story 5: Ignore unrelated events

**Priority:** P1

As an administrator, I want unrelated issues and transitions ignored, so that the automation cannot change issues outside its intended scope.

**Acceptance scenarios**

- Issues outside project `ARE` produce no parent action.
- Non-sub-task issues produce no parent action.
- A sub-task without a parent produces no parent action.
- A sub-task entering a non-Done status does not trigger the close path.
- A sub-task leaving a non-Done status does not trigger the reopen path.

## 5. Functional Requirements

### Event qualification

- **FR-001:** The automation MUST process only issues in project `ARE`.
- **FR-002:** The automation MUST process only sub-task issue types with a parent.
- **FR-003:** The close path MUST trigger when a sub-task transitions into Jira's Done status category.
- **FR-004:** The reopen path MUST trigger when a sub-task transitions from Jira's Done status category to a non-Done status category.
- **FR-005:** The automation MUST support a scheduled daily refresh if the deployment enables that path.

### Close behavior

- **FR-006:** The automation MUST retrieve or evaluate all sub-tasks belonging to the parent.
- **FR-007:** The automation MUST confirm that the parent has at least one sub-task before considering closure.
- **FR-008:** The automation MUST transition the parent only when every sub-task is in the Done status category.
- **FR-009:** The automation MUST verify that the parent is not already in the Done status category before attempting closure.
- **FR-010:** The automation MUST use the validated workflow transition to move the parent to `DONE`.

### Reopen behavior

- **FR-011:** The automation MUST confirm that the parent is currently in the Done status category before attempting a reopen.
- **FR-012:** The automation MUST use the validated `ARE` workflow reopen transition and target status.
- **FR-013:** The automation MUST not attempt a reopen when no valid transition is available; it MUST follow the failure-handling behavior instead.

### Idempotency and auditability

- **FR-014:** Before a close action, the automation MUST use a distinctive searchable marker such as `[Automation] Evaluated sub-tasks and transitioning parent to DONE.`
- **FR-015:** Before a reopen action, the automation MUST use a distinctive searchable marker such as `[Automation] A sub-task left Done; evaluating parent reopen transition.`
- **FR-016:** The automation MUST avoid duplicate marker comments when the same action has already been evaluated or the parent is already in the target state.
- **FR-017:** Repeated events and scheduled refreshes MUST NOT cause duplicate transitions.
- **FR-018:** Each execution MUST record its trigger, target parent, action or no-op result, and failure reason when applicable.

### Failure handling

- **FR-019:** When a required transition fails or is unavailable, the automation MUST add a diagnostic comment to the parent.
- **FR-020:** The diagnostic comment MUST include the condition that was met, attempted transition, failure reason when available, and required manual action.
- **FR-021:** The diagnostic comment MUST mention the parent assignee using Jira-supported mention syntax.
- **FR-022:** The failure path MUST cause Jira to notify the mentioned assignee when notification is supported by the configured comment action.

## 6. Data and External Contracts

### Jira issue data required

The automation requires access to:

- Project key and issue key.
- Issue type and sub-task classification.
- Parent issue reference.
- Parent and sub-task statuses and status categories.
- Complete parent sub-task collection.
- Parent assignee identity.
- Available workflow transitions.
- Transition result and error details.
- Issue comments sufficient to detect existing automation markers.

### Required permissions

The rule actor MUST be able to:

- Browse issues in project `ARE`.
- Read parent and sub-task status and relationship data.
- Add comments to parent issues.
- Transition parent issues to `DONE`.
- Execute the supported reopen transition.
- Mention and notify the parent assignee.
- Read execution information needed for operational diagnosis.

### Persistence and logs

If implemented as part of the application rather than only native Jira Automation, durable execution state MUST use PostgreSQL 15 and MUST preserve idempotency keys and outcomes. Sensitive credentials and tokens MUST never be persisted in ordinary logs or comments.

## 7. Non-Functional Requirements

- **NFR-001 Reliability:** A transient Jira failure MUST fail visibly and leave enough information for retry or manual recovery.
- **NFR-002 Idempotency:** Retrying an execution with the same logical event MUST produce at most one intended transition and one corresponding marker.
- **NFR-003 Security:** Secrets MUST be supplied through protected configuration and MUST NOT be exposed in logs, comments, or frontend code.
- **NFR-004 Observability:** Operators MUST be able to distinguish successful actions, deliberate no-ops, and failures.
- **NFR-005 Testability:** Business rules MUST be testable without requiring production Jira credentials.
- **NFR-006 Maintainability:** Status categories and transition identifiers MUST be configurable or documented so workflow changes can be revalidated.
- **NFR-007 Operational safety:** The automation MUST remain disabled during major workflow changes until the acceptance suite passes again.

## 8. Error and Edge-Case Behavior

| Condition | Required behavior |
|---|---|
| Parent has no sub-tasks | No-op; do not close or add a close marker. |
| One or more sub-tasks are not Done | No-op; keep the parent unchanged. |
| Parent already Done during close evaluation | No-op; do not duplicate transition or marker. |
| Parent not Done during reopen evaluation | No-op; do not reopen. |
| Issue is outside `ARE` | Ignore without changing any issue. |
| Issue is not a sub-task | Ignore without changing any issue. |
| Sub-task has no parent | Ignore without changing any issue. |
| Close transition missing or fails | Add diagnostic comment, mention assignee, notify when supported, and log failure. |
| Reopen transition missing or fails | Add diagnostic comment, mention assignee, notify when supported, and log failure. |
| Jira response is rate-limited or transiently unavailable | Record failure details and make the operation safely retryable. |
| Assignee is unavailable for mention | Record the notification limitation in the diagnostic result and retain the manual recovery instruction. |

## 9. Success Criteria

The feature is successful when:

1. A parent with multiple sub-tasks moves to `DONE` only after the final sub-task reaches Done.
2. A parent remains unchanged while any sub-task is not Done.
3. A parent with no sub-tasks remains unchanged.
4. A Done parent reopens through the approved workflow transition when a sub-task leaves Done.
5. Duplicate events and daily refreshes do not create duplicate transitions or marker comments.
6. Failed transitions create complete diagnostic comments and notify the parent assignee where supported.
7. Issues outside `ARE`, non-sub-task issues, and orphan sub-tasks are ignored.
8. Successful, no-op, and failed evaluations are visible in execution logs.
9. The complete acceptance suite passes against a dedicated test parent before production enablement.

## 10. Acceptance Test Matrix

| ID | Test | Expected result |
|---|---|---|
| AT-001 | Complete one of several sub-tasks | Parent remains unchanged. |
| AT-002 | Complete the final remaining sub-task | Parent transitions to `DONE`. |
| AT-003 | Evaluate a parent with no sub-tasks | No action occurs. |
| AT-004 | Move a sub-task out of Done while parent is Done | Parent follows the approved reopen transition. |
| AT-005 | Replay a close or reopen event | No duplicate transition or marker comment. |
| AT-006 | Force an invalid or failing transition | Diagnostic comment and assignee notification are produced. |
| AT-007 | Trigger from a project other than `ARE` | Event is ignored. |
| AT-008 | Trigger from a non-sub-task issue | Event is ignored. |
| AT-009 | Review execution records | Successes, no-ops, and failures are distinguishable. |
| AT-010 | Run the daily refresh against already-correct parents | No duplicate side effects occur. |

## 11. Dependencies and Clarifications

The following items MUST be confirmed before implementation or production enablement:

- Exact Jira workflow transition name or ID that moves an eligible parent to `DONE`.
- Exact reopen transition name or ID and target status for parents currently in `DONE`.
- Exact Jira Automation conditions and smart values available in the current rule builder.
- Correct evaluation method for determining whether all parent sub-tasks are Done.
- Jira-supported syntax for mentioning the parent assignee from the automation comment action.
- Whether the configured comment action sends the required notification.
- Rule actor permissions in project `ARE`.
- Availability of the Jira project and workflow to the configuring account.
- Whether the daily refresh is required in addition to event-driven triggers.
- Owner responsible for reviewing execution logs and approving workflow-dependent changes.

## 12. Rollout and Maintenance

1. Configure the rule only after the dependencies and clarifications are confirmed.
2. Validate it against a dedicated test parent with several sub-tasks in mixed statuses.
3. Run every acceptance test in the matrix and inspect Jira execution logs and issue history.
4. Obtain project-owner approval before enabling the rule for all applicable parents.
5. Monitor successful and failed executions after rollout.
6. Revalidate the rule whenever statuses, transitions, issue types, permissions, or notification behavior changes.
7. Disable the rule during major workflow migrations until the acceptance tests pass again.

## 13. Definition of Done

- [ ] Close and reopen paths are configured using confirmed `ARE` workflow transitions.
- [ ] Project, issue-type, parent, and status-category guards are verified.
- [ ] No-sub-task and partially-complete parent behavior is verified.
- [ ] Idempotency prevents duplicate transitions and marker comments.
- [ ] Failure comments contain all required diagnostic information.
- [ ] Parent-assignee mention and notification behavior is verified.
- [ ] Event-driven and daily-refresh behavior are tested, if both are enabled.
- [ ] Execution logs distinguish success, no-op, and failure outcomes.
- [ ] Acceptance test matrix passes in the controlled test setup.
- [ ] Documentation and operational ownership are recorded before production rollout.
