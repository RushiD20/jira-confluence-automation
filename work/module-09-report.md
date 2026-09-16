# Module 09 Completion Report

## Tracked Files
.env
.vscode/settings.json
PROJECT_IDEAS.md
WEEKLY_STATUS_REPORT_TEMPLATE.md
backlog.md
calculator/main.py
calculator/operations.py
hello.txt
project_spec.md
some-file.txt

## Backlog Commit History
002ea20 (HEAD -> master) Add implementation backlog for Jira parent automation

## backlog.md Contents
# Jira Automation Implementation Backlog

This backlog translates the requirements in `project_spec.md` into a concrete, execution-ready plan for implementing the `Close Parent When Sub-Tasks Finish` Jira Cloud Automation rule for project `ARE`.

## Phase 1: Setup

- [ ] Confirm Jira access and project permissions for the rule actor in project `ARE`.
- [ ] Verify the current browser session has access to `https://epam.atlassian.net` and the `ARE` project; escalate if access is still restricted.
- [ ] Identify the parent issue types and sub-task issue type used in `ARE` and confirm which parent issues should be included.
- [ ] Review the current `ARE` workflow and document all relevant statuses, including the Done status category and any reopen transition options.
- [ ] Confirm the exact `DONE` transition name for parent issues and the exact reopen transition used when a parent in `DONE` is reopened.
- [ ] Validate that the automation rule actor can browse issues, add comments, transition issues, and notify users in `ARE`.
- [ ] Confirm the issue assignee can be mentioned and notified by Jira Automation comments.
- [ ] Define the test parent issue and sub-task setup to use for validation before production rollout.
- [ ] Set up a dedicated test environment or sandbox parent issue in `ARE` with several sub-tasks in different statuses.
- [ ] Create a working list of status values and transition names for the rule builder so the smart values and conditions are mapped correctly during configuration.
- [ ] Document the rule naming convention and rule ownership, including who will monitor execution logs and manage workflow changes.

## Phase 2: Core Features

- [ ] Build the close-parent automation path for the trigger: sub-task transitioned into the Done status category.
- [ ] Add conditions to confirm the issue belongs to project `ARE`.
- [ ] Add conditions to confirm the issue is a sub-task with a parent issue.
- [ ] Add a branch to the parent issue and confirm the parent has at least one sub-task.
- [ ] Retrieve or evaluate all sub-tasks for the parent and confirm all are in Jira's Done status category.
- [ ] Add a guard to ensure the parent is not already in the Done status category before attempting a transition.
- [ ] Add the idempotency marker comment before any close action using a distinctive searchable format such as `[Automation] Evaluated sub-tasks and transitioning parent to DONE.`
- [ ] Transition the parent issue to `DONE` using the validated workflow transition.
- [ ] Build the reopen-parent automation path for the trigger: sub-task leaves the Done status category.
- [ ] Add conditions to confirm the issue belongs to project `ARE` and is a sub-task with a parent issue.
- [ ] Add a condition to confirm the parent is currently in the Done status category before reopening.
- [ ] Add the idempotency marker comment before the reopen action using a searchable format such as `[Automation] A sub-task left Done; evaluating parent reopen transition.`
- [ ] Identify and use the supported reopen transition for a parent in `DONE` and verify the target status is valid in the `ARE` workflow.
- [ ] Prevent the rule from acting on parents with no sub-tasks.
- [ ] Ensure the automation ignores non-`ARE` issues and non-sub-task issue types.
- [ ] Add a guard to avoid duplicate transitions or marker comments when the parent is already in the target state.
- [ ] Implement the logic to detect a sub-task leaving Done and reopen the parent only when appropriate.
- [ ] Ensure the rule checks the parent state before each automation action so redundant transitions are not triggered.
- [ ] Define the exact failure-handling comment text and required fields: attempted transition, failure reason, required manual action, and parent assignee mention.
- [ ] Add the diagnostic comment pattern for failed parent transitions, including the assignee mention and notification requirement.
- [ ] Capture the failure reason when available and pass it into the comment body.
- [ ] Include the sub-task condition status in the diagnostic comment so the reason for the action is clearly visible in the parent issue history.
- [ ] Build a safe fallback path when the workflow does not include a valid reopen transition or close transition.
- [ ] Ensure the rule does not close a parent when any sub-task is outside the Done status category.
- [ ] Validate that daily refresh logic, if used, does not duplicate transitions or comments when the parent is already in the correct state.

## Phase 3: Integration

- [ ] Map the Jira Automation rule builder conditions to the exact current Jira Cloud editor names and smart values used in `ARE`.
- [ ] Create the close path rule or automation branch in Jira Cloud Automation.
- [ ] Configure the trigger for issue transition events.
- [ ] Configure project and issue-type conditions for `ARE` and sub-task detection.
- [ ] Add the destination-status-in-Done condition for the close path.
- [ ] Add the branch to parent and evaluate the parent's sub-task set.
- [ ] Configure the all-sub-tasks-in-Done condition and not-in-Done parent condition.
- [ ] Add the marker comment action and close transition action.
- [ ] Add the error path to create a diagnostic comment if the parent transition fails.
- [ ] Create the reopen path rule or automation branch in Jira Cloud Automation.
- [ ] Configure the trigger for transitions where the source status was in Done and the destination status is not Done.
- [ ] Add the parent-in-Done condition and the parent branch logic.
- [ ] Add the marker comment action and reopen transition action.
- [ ] Add the error path to create a diagnostic comment and mention the parent assignee when reopen fails.
- [ ] Verify smart values for the parent issue, assignee, current status, and transition result are supported by the configured Jira Automation environment.
- [ ] Configure the scheduled daily refresh if the rule design includes a periodic status evaluation to catch missed transitions.
- [ ] Make sure the daily refresh is idempotent and does not reapply the same transition or duplicate comments.
- [ ] Document which rule path performs event-driven updates and which path handles scheduled refresh, if both are implemented.
- [ ] Confirm that comments will notify the assignee when the automation mentions them with the correct Jira syntax.
- [ ] Validate the rule actor has enough permissions to execute both the close and reopen transitions without manual approval.
- [ ] Record the exact transition IDs or names used in the automation so they can be revalidated later if the workflow changes.

## Phase 4: Testing

- [ ] Create a dedicated test parent issue in project `ARE` with several sub-tasks in different status combinations.
- [ ] Validate acceptance test 1: completing one of several sub-tasks does not close the parent.
- [ ] Validate acceptance test 2: completing the final remaining sub-task transitions the parent to `DONE`.
- [ ] Validate acceptance test 3: a parent with no sub-tasks remains unchanged.
- [ ] Validate acceptance test 4: a sub-task leaving Done reopens a parent currently in `DONE`.
- [ ] Validate acceptance test 5: repeated events do not duplicate transitions or marker comments.
- [ ] Validate acceptance test 6: a failed transition creates the diagnostic comment and mentions the parent assignee.
- [ ] Validate acceptance test 7: issues outside project `ARE` are ignored.
- [ ] Validate acceptance test 8: non-sub-task issues are ignored.
- [ ] Validate acceptance test 9: the rule execution log records both successful and failed runs.
- [ ] Run a controlled test sequence with each transition and confirm the parent issue status matches the expectation after each event.
- [ ] Test the no-sub-task edge case and confirm the rule does nothing instead of closing the parent.
- [ ] Test the reopen path when the sub-task leaves Done and confirm the parent is moved back to the valid workflow status through the reopen transition.
- [ ] Test duplication behavior by re-triggering the same event and confirming the automation does not add duplicate comments or repeat transitions.
- [ ] Simulate a workflow failure or invalid transition and confirm the diagnostic comment is created with all required details.
- [ ] Check the audit trail for both successful and failed rule executions and verify the comments are searchable.
- [ ] Review rule execution logs for false positives, workflow mapping problems, and unintended transitions.
- [ ] Prepare a sign-off checklist before enabling the rule beyond the test issue.
- [ ] Validate the schedule-based refresh path, if enabled, against the same idempotency and duplicate-prevention expectations.
- [ ] Confirm the automation remains disabled during major workflow changes until validation is complete.

## Phase 5: Documentation

- [ ] Write a concise rule configuration guide describing the trigger, conditions, parent branch logic, and action order.
- [ ] Document the exact workflow dependencies for the project, including the valid `DONE` transition, the reopen transition, and target status.
- [ ] Add a section describing the idempotency markers and how they help diagnose rule execution.
- [ ] Document the failure-handling comment template and the notification requirement for the assignee.
- [ ] Document the acceptance tests and the expected behavior for every edge case.
- [ ] Add a runbook for operational monitoring, including how to review automation logs, spot failures, and verify workflow changes.
- [ ] Record the owner responsible for monitoring the rule after rollout.
- [ ] Create a change log or implementation notes file covering the initial rollout and any future workflow updates.
- [ ] Add a troubleshooting section for common issues such as invalid transitions, missing permissions, and mismatched statuses.
- [ ] Record the current access dependency and the requirement that the current browser account must have project access before any live configuration is attempted.
- [ ] Capture a final rollout checklist for moving from test validation to production enablement.
- [ ] Review documentation for clarity and keep the instructions aligned with the actual Jira Automation configuration used in the project.

## Definition of Done

- [ ] All close and reopen automation actions are configured and tested in `ARE`.
- [ ] Idempotency and duplicate-prevention checks are working.
- [ ] Failure comments and assignee notifications are functional.
- [ ] The automation ignores non-`ARE` and non-sub-task issues correctly.
- [ ] The rule logs successful and failed runs for review.
- [ ] Documentation is complete and can be used by the project owner to maintain and troubleshoot the rule.
