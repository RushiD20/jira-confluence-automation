# Module 08 Completion Report

## Tracked Files
```text
.env
.vscode/settings.json
PROJECT_IDEAS.md
WEEKLY_STATUS_REPORT_TEMPLATE.md
calculator/main.py
calculator/operations.py
hello.txt
project_spec.md
some-file.txt
```

## Spec Commit History
```text
a005b60 (HEAD -> master) Add Jira parent sub-task automation specification
```

## project_spec.md Contents
```markdown
# Technical Specification: Close Parent When Sub-Tasks Finish

## 1. Overview

Build a Jira Cloud Automation rule for the `ARE` project. The automation manages parent issue status based on the status of its sub-tasks for a project manager responsible for a team of 15 people.

## 2. Goals

- Automatically transition a parent issue to `DONE` when all of its sub-tasks reach Jira's Done status category.
- Reopen the parent automatically if a previously completed sub-task leaves Jira's Done status category.
- Avoid acting on parent issues that have no sub-tasks.
- Provide an audit trail and notify the responsible project manager when an automatic transition fails.

## 3. Scope

- Platform: Jira Cloud
- Site: `https://epam.atlassian.net`
- Project: `ARE`
- Issue scope: All parent issue types with sub-tasks
- Implementation: Jira Cloud Automation rule
- Rule name: `Close Parent When Sub-Tasks Finish`
- Rule actor: Jira Automation rule actor

The rule actor must have permission to browse issues, add comments, transition parent issues, and notify users in project `ARE`.

## 3.1 Data Refresh Frequency

- Refresh frequency: Daily
- The automation should perform its status evaluation once per day as a scheduled data refresh.
- Event-driven close and reopen triggers remain responsible for reacting to sub-task transitions between scheduled refreshes.
- The daily refresh must not duplicate transitions or comments when the parent is already in the correct state.

## 4. Functional Requirements

### 4.1 Close Parent

When a sub-task transitions into Jira's Done status category:

1. Confirm the issue belongs to project `ARE`.
2. Confirm the issue is a sub-task with a parent.
3. Retrieve the parent issue's sub-tasks.
4. Confirm the parent has at least one sub-task.
5. Confirm every sub-task is in Jira's Done status category.
6. Confirm the parent is not in the Done status category.
7. Check the parent status and add an idempotency marker comment before acting.
8. Transition the parent issue to `DONE`.

The rule must not close a parent when any sub-task remains outside the Done status category.

### 4.2 Reopen Parent

When a sub-task leaves Jira's Done status category:

1. Confirm the issue belongs to project `ARE` and is a sub-task with a parent.
2. Confirm the parent is currently in the Done status category.
3. Check the parent status and add an idempotency marker comment before acting.
4. Transition the parent through the workflow's supported reopen transition.

The target reopen status must be confirmed against the `ARE` workflow during implementation. If the workflow has no valid reopen transition, follow the failure-handling requirements.

### 4.3 Parent Issues Without Sub-Tasks

Do nothing when a parent has no sub-tasks. The automation must not close a parent solely because it has no sub-tasks.

### 4.4 Failure Handling

If a required parent transition fails or is unavailable:

- Add a detailed diagnostic comment to the parent.
- Include that the sub-task condition was met, the attempted transition, the failure reason when available, and the required manual action.
- Mention the parent issue's assignee in the comment.
- Ensure Jira sends the corresponding notification to the mentioned assignee.

Suggested failure comment:

> All sub-tasks meet the required status condition, but the parent could not be transitioned to the requested status. Attempted transition: `<transition>`. Reason: `<error details>`. Please review the workflow and update the parent manually. @`<parent assignee>`

## 5. Idempotency and Duplicate Prevention

Before performing a close or reopen action, the rule must check the parent status and add a marker comment identifying the automation action. The rule must not repeat the same transition or create duplicate marker comments when the parent is already in the target state.

Suggested marker formats:

- Close: `[Automation] Evaluated sub-tasks and transitioning parent to DONE.`
- Reopen: `[Automation] A sub-task left Done; evaluating parent reopen transition.`

The implementation should use a distinctive, searchable marker so rule execution can be diagnosed without relying only on execution history.

## 6. Rule Design

Use two event paths in the Jira Automation rule, or two coordinated rules if Jira's rule builder makes the paths clearer:

### Close path

- Trigger: Issue transitioned
- Condition: Project is `ARE`
- Condition: Issue type is Sub-task
- Condition: Destination status is in the Done status category
- Branch: Parent
- Condition: Parent has one or more sub-tasks
- Condition: All parent sub-tasks are in the Done status category
- Condition: Parent is not in the Done status category
- Action: Add marker comment
- Action: Transition parent to `DONE`
- Error path: Add diagnostic comment and mention the parent assignee

### Reopen path

- Trigger: Issue transitioned
- Condition: Project is `ARE`
- Condition: Issue type is Sub-task
- Condition: Source status was in the Done status category and destination status is not
- Branch: Parent
- Condition: Parent is in the Done status category
- Action: Add marker comment
- Action: Transition parent through the supported reopen transition
- Error path: Add diagnostic comment and mention the parent assignee

The exact Jira Automation condition names and smart values must be mapped to the current Jira Cloud rule builder during configuration.

## 7. Workflow Dependencies

Before enabling the rule, verify:

- `DONE` is a valid parent transition in the `ARE` workflow.
- A valid reopen transition exists for a parent in `DONE`.
- The rule actor can execute both transitions.
- The parent assignee can be mentioned and notified.
- The workflow's statuses are correctly mapped to Jira's Done status category.

## 8. Testing and Rollout

Use a dedicated test parent issue with several sub-tasks in project `ARE`.

Acceptance tests:

1. Completing one of several sub-tasks does not close the parent.
2. Completing the final remaining sub-task transitions the parent to `DONE`.
3. A parent with no sub-tasks is unchanged.
4. A sub-task leaving Done reopens a parent currently in `DONE`.
5. Repeated events do not create duplicate transitions or marker comments.
6. A failed transition creates the detailed diagnostic comment and mentions the parent assignee.
7. Issues outside project `ARE` are ignored.
8. Non-sub-task issues are ignored.
9. The rule execution log records successful and failed runs.

After the dedicated test passes, enable the rule for all applicable parent issues in `ARE`.

## 9. Monitoring and Maintenance

- Review automation execution logs after rollout and periodically thereafter.
- Monitor failed transitions and workflow changes.
- Revalidate the rule when `ARE` statuses, issue types, permissions, or workflows change.
- Keep the rule disabled during major workflow migrations until the acceptance tests pass again.

## 10. Open Implementation Checks

- Confirm the exact Jira workflow transition name for moving a parent to `DONE`.
- Confirm the exact reopen transition and target status.
- Confirm how the Jira Cloud rule builder evaluates all sub-tasks for the parent.
- Confirm the parent assignee mention syntax supported by the configured Jira Automation action.
- Confirm that the current browser account has access to project `ARE`; the current session is on an Atlassian request-access page.
```
