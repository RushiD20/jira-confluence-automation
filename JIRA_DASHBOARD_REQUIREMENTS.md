# Jira Dashboard Requirements

## 1. Objective

Create a Jira Cloud dashboard that shows the engineering team's sprint delivery progress for the current active sprint.

## 2. Platform and Access

- Platform: Jira Cloud
- Atlassian site: `https://epam.atlassian.net`
- Dashboard creator: The requesting user
- Dashboard visibility: Private; visible only to the requesting user
- Implementation approach: Jira's built-in dashboard gadgets
- Refresh interval: Every 15 minutes

## 3. Scope

- Project: `ARE`
- Board: The team's primary Scrum board
- Sprint selection: Current active sprint only
- Filter name: `ARE Current Sprint Delivery`
- Filter: Create a new saved filter for the dashboard
- Issue types: Stories, tasks, and bugs
- Exclude epics and subtasks from the main progress totals
- Sort order: Priority, then status

## 4. Progress Measurement

- Primary metric: Story Points
- Completed work: Issues in Jira's Done status category
- Progress bar: Compare completed story points with elapsed sprint time
- Unestimated issues: Exclude them from story-point totals but include them in issue counts
- Unestimated work: Show a warning so missing estimates remain visible

## 5. Dashboard Content

- Sprint progress bar showing completed versus total estimated story points
- Issue status breakdown for stories, tasks, and bugs
- Blocked-items list with relevant issue details
- Clear `No active sprint` message when no active sprint exists

## 6. Blocker Detection

Use Jira's status category to identify blocked work, subject to confirmation that the team's workflow maps blocked work appropriately.

## 7. Open Implementation Detail

The dashboard should use Jira's built-in gadgets and filters. Exact gadget availability and configuration may depend on the permissions and features enabled in the `ARE` Jira project.

## 8. Access Dependency

The current browser session reached an Atlassian request-access page for the Jira site. Dashboard configuration cannot proceed until the user has access to the `ARE` Jira project and primary Scrum board.
