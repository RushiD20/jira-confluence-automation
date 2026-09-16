# AI-Driven QA Report

## Scope
This QA report captures the findings from the AI-assisted testing session for the Jira parent automation application. Testing covered browser navigation, main-page inspection, primary interaction flow, console health, and backend validation behavior.

## Application under test
- Frontend: http://127.0.0.1:5173/
- Backend: http://127.0.0.1:3000
- Product: Orbit | Jira Automation Control Room

## Pages and states reviewed
1. Overview
   - Verified the landing page renders successfully.
   - Confirmed page title and dashboard layout.
2. Executions
   - Verified execution feed content and status entries.
3. Workflow checks
   - Verified metrics and workflow health board.
4. Test scenarios
   - Verified scenario rows and operator note panel.

## Elements tested
### Navigational elements
- Orbit brand/logo
- Overview link
- Executions link with badge count
- Workflow checks link
- Test scenarios link

### Header and control elements
- Live status indicator
- Notifications button
- User avatar marker

### Dashboard elements
- Primary CTA: Run test scenario
- Automation metric cards
- Recent execution feed
- Workflow health area
- Safe-to-run scenarios panel
- Operator note panel
- Footer with last sync information

## User flow validation
### Launch flow
- The application loaded successfully from the browser.
- No blocking runtime errors were observed on initial load.

### Navigation flow
- Main app sections were navigated successfully via the hash-based navigation states.
- Layout and visible content remained consistent across sections.

### Main interaction flow
- The primary dashboard action, "Run test scenario", was triggered.
- The action produced a valid backend evaluation result and updated the UI with:
  - "Test returned reopen"
  - "ARE-1842 · sub_task_left_done"

## Console and runtime checks
- Browser console was reviewed during load and interaction.
- Result: no JavaScript errors or warnings were emitted.

## Bugs identified
### 1. Form/submit validation gap
- Symptom: The submit flow did not validate all required event fields consistently.
- Risk: incomplete payloads could lead to ambiguous or incorrect evaluation results.
- Root cause: required-field validation was incomplete for the automation event payload.

## Fixes applied
### 1. Backend validation fix
- Updated [jira-parent-automation/apps/api/src/routes/automation.routes.ts](../jira-parent-automation/apps/api/src/routes/automation.routes.ts)
- Added required-field validation for:
  - eventId
  - projectKey
  - issueKey
  - issueType
  - sourceStatusCategory
  - destinationStatusCategory
  - parentKey for sub-task events
- Added validation for allowed status categories
- Return value now includes structured 400 errors with missing fields listed when payload is incomplete

### 2. Frontend error handling update
- Updated [jira-parent-automation/apps/web/src/App.tsx](../jira-parent-automation/apps/web/src/App.tsx)
- Added visible validation error handling for failed API submissions
- Ensured the UI resets and surfaces actionable error text when the request fails

## Verification status
### Successful checks
- Browser launched successfully and app rendered
- Navigation across main sections verified
- Primary action flow passed
- No runtime browser errors found
- TypeScript compilation passed via `npx tsc -p tsconfig.json --noEmit`

### Current project status
- Frontend: running and responding
- Backend: responding to automation evaluation requests
- Main user flow: working successfully
- Validation issue: fixed
- Overall status: operational for the tested scenarios

## Final assessment
The application passed the tested session flow and the known validation issue was corrected. The dashboard is functioning as expected in the tested states, with no console errors and a successful primary interaction path.
