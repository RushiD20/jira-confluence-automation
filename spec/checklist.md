# Specification Implementation Checklist

**Reviewed:** [specification.md](specification.md)  
**Implementation:** [API server](../jira-parent-automation/apps/api/src/server.ts), [automation route](../jira-parent-automation/apps/api/src/routes/automation.routes.ts), [frontend](../jira-parent-automation/apps/web/src/App.tsx)  
**Review date:** 2026-09-16

## Status Definitions

- **Verified:** Implemented and exercised successfully in the current workspace.
- **Partial:** Some behavior exists, but the complete requirement is not implemented or verified.
- **Not implemented:** No production implementation exists for the requirement.
- **Blocked:** The requirement depends on Jira, PostgreSQL, Docker, credentials, or workflow configuration that is unavailable.

## Executive Result

**Overall status: Partial, not production-ready.**

The current implementation provides a compilable Express API with a pure evaluation endpoint and a React/Vite control-room screen. The evaluator correctly classifies the basic close, partial-completion, reopen, out-of-project, non-sub-task, and orphan cases. It does not yet perform Jira mutations or provide durable state, so the feature’s central automation behavior remains unimplemented.

### Verification executed

- API `npm run build`: passed.
- Frontend `npm run build`: passed.
- `POST /api/automation/evaluate` matrix: passed for close, partial/no-op, reopen, out-of-project, non-sub-task, and orphan cases.
- `/health`: previously returned `200` with `status: ok`.
- PostgreSQL/Docker verification: blocked because Docker Desktop’s Linux engine was stopped; no database connection was established.
- Live Jira verification: not run; no Jira client or credentials are configured.

## 1. Goals and Scope

| Requirement | Implemented? | Does it work? | Evidence and gap |
|---|---|---|---|
| Automatically close an eligible parent when all sub-tasks are Done | Partial | Classification works; Jira close does not | Route returns `action: close` and `reason: all_sub_tasks_done`; no Jira transition is called. |
| Reopen a Done parent when a sub-task leaves Done | Partial | Classification works; Jira reopen does not | Route returns `action: reopen`; no Jira transition is called. |
| Never close a parent with no sub-tasks | Partial | Evaluator returns no-op | No-op logic exists, but no external parent is changed because no external mutation exists. |
| Prevent duplicate transitions and idempotency comments | Not implemented | Not tested | No idempotency key, persistence, locking, marker lookup, or comment writer exists. |
| Provide searchable audit information | Not implemented | Not tested | No execution store or structured execution log exists. |
| Notify the parent assignee on failed transition | Not implemented | Not tested | No Jira comment, mention, notification, or failure path exists. |
| Support controlled testing before production enablement | Partial | Local evaluator is testable | Build and local endpoint checks work, but no Jira fixture, integration suite, or rollout gate exists. |
| Process only Jira project `ARE` | Partial | Verified for evaluator input | `projectKey !== ARE` returns `ignored`; request schema validation is incomplete. |
| Process supported parent issue types only | Partial | Not verifiable against Jira | Only `issueType === sub-task` is checked; there is no configured parent-type allowlist. |
| Process sub-tasks with a parent | Partial | Orphan input is ignored | `parentKey` is required for eligibility, but relationship is not fetched or verified from Jira. |
| Event-driven transition processing | Not implemented | Not tested | No webhook, Jira trigger, or event intake route exists. |
| Optional daily refresh | Not implemented | Not tested | No scheduler or refresh job exists. |
| Avoid production rollout before prerequisites pass | Partial | Not applicable | No deployment automation or enable/disable control exists; this is currently a process requirement only. |

## 2. User Stories and Acceptance Scenarios

### User Story 1: Close parent after all sub-tasks finish

| Scenario | Implemented? | Does it work? | Evidence and gap |
|---|---|---|---|
| Final sub-task reaches Done and all parent sub-tasks are Done | Partial | Verified as classification only | The evaluator returns `close`; marker creation, Jira transition, and execution success recording are absent. |
| A remaining sub-task is not Done | Partial | Verified | Matrix returned `noop / sub_tasks_not_all_done`; no-op execution record is absent. |
| Parent has no sub-tasks | Partial | Verified | Empty `parentSubTasks` returns `noop / parent_has_no_sub_tasks`; no Jira-side guarantee exists. |

### User Story 2: Reopen parent when work resumes

| Scenario | Implemented? | Does it work? | Evidence and gap |
|---|---|---|---|
| Sub-task leaves Done while parent is Done | Partial | Verified as classification only | Matrix returned `reopen / sub_task_left_done`; no reopen transition or success record exists. |
| Parent is not Done | Partial | Not fully verified | The route condition prevents reopen when `parentStatusCategory` is not `done`, but a dedicated endpoint test was not recorded in this run. |

### User Story 3: Retry safely without duplicate side effects

| Scenario | Implemented? | Does it work? | Evidence and gap |
|---|---|---|---|
| Repeated close event produces no duplicate transition or marker | Not implemented | Not tested | No state, idempotency key, or marker handling exists. |
| Daily refresh does not duplicate effects | Not implemented | Not tested | No daily refresh exists. |

### User Story 4: Recover from failed transition

| Scenario | Implemented? | Does it work? | Evidence and gap |
|---|---|---|---|
| Close transition failure creates diagnostic comment and notification | Not implemented | Not tested | No Jira mutation or failure handler exists. |
| Missing reopen transition creates diagnostic comment and notification | Not implemented | Not tested | No transition lookup, diagnostic comment, or notification path exists. |

### User Story 5: Ignore unrelated events

| Scenario | Implemented? | Does it work? | Evidence and gap |
|---|---|---|---|
| Issue outside `ARE` is ignored | Partial | Verified | Matrix returned `ignored / issue_outside_project`. |
| Non-sub-task is ignored | Partial | Verified | Matrix returned `ignored / issue_not_eligible_sub_task`. |
| Sub-task without parent is ignored | Partial | Verified | Matrix returned `ignored / issue_not_eligible_sub_task`. |
| Sub-task enters non-Done status without close | Partial | Logic present, not separately tested | Final fallback is `noop`; no dedicated recorded case. |
| Sub-task leaves non-Done status without reopen | Partial | Logic present, not separately tested | Final fallback is `noop`; no dedicated recorded case. |

## 3. Functional Requirements

| ID | Requirement | Implemented? | Does it work? | Evidence and gap |
|---|---|---|---|---|
| FR-001 | Process only project `ARE` | Partial | Verified in evaluator | Constant and guard exist; no authenticated Jira event intake exists. |
| FR-002 | Process only sub-tasks with a parent | Partial | Verified for supplied payloads | Guard exists; no Jira relationship lookup or full schema validation exists. |
| FR-003 | Close path triggers on transition into Done | Partial | Verified in evaluator | Destination Done is checked; no event trigger or transition occurs. |
| FR-004 | Reopen path triggers from Done to non-Done | Partial | Verified in evaluator | Source/destination and parent status conditions exist; no event trigger or Jira transition occurs. |
| FR-005 | Support optional daily refresh | Not implemented | Not tested | No job, scheduler, parent selection, overlap prevention, or refresh log exists. |
| FR-006 | Retrieve/evaluate all parent sub-tasks | Partial | Only caller-supplied list is evaluated | `parentSubTasks` is accepted from the request; no Jira retrieval or pagination exists. |
| FR-007 | Require at least one sub-task before close | Partial | Verified | Empty list returns `parent_has_no_sub_tasks`; no external close path exists. |
| FR-008 | Close only when every sub-task is Done | Partial | Verified | `some(statusCategory !== done)` returns no-op; no Jira mutation exists. |
| FR-009 | Verify parent is not Done before close | Partial | Logic present | Close guard checks `parentStatusCategory !== done`; no live parent re-read exists. |
| FR-010 | Use configured validated close transition | Not implemented | Not tested | No transition configuration or Jira client exists. |
| FR-011 | Verify parent is Done before reopen | Partial | Logic present | Reopen guard checks `parentStatusCategory === done`; no live parent re-read exists. |
| FR-012 | Use configured validated reopen transition | Not implemented | Not tested | No transition configuration or Jira client exists. |
| FR-013 | Handle missing reopen transition through failure path | Not implemented | Not tested | No transition discovery or failure path exists. |
| FR-014 | Use distinctive close marker | Not implemented | Not tested | No comment writer or marker template implementation exists. |
| FR-015 | Use distinctive reopen marker | Not implemented | Not tested | No comment writer or marker template implementation exists. |
| FR-016 | Avoid duplicate marker comments | Not implemented | Not tested | No comment lookup or idempotency state exists. |
| FR-017 | Repeated events/refreshes do not duplicate transitions | Not implemented | Not tested | No mutation, persistence, locking, or scheduler exists. |
| FR-018 | Record trigger, parent, result, and failure | Not implemented | Not tested | Endpoint returns a result but does not persist or log an execution record. |
| FR-019 | Add diagnostic comment on transition failure | Not implemented | Not tested | No Jira comment integration exists. |
| FR-020 | Include condition, transition, reason, and manual action | Not implemented | Not tested | No diagnostic template exists. |
| FR-021 | Mention parent assignee | Not implemented | Not tested | No assignee lookup or Jira mention support exists. |
| FR-022 | Notify mentioned assignee when supported | Not implemented | Not tested | No comment/notification integration exists. |

## 4. Data, Security, and Non-Functional Requirements

| Requirement | Implemented? | Does it work? | Evidence and gap |
|---|---|---|---|
| Jira issue data contract | Not implemented | Not tested | Shared TypeScript types exist for a synthetic event, but no Jira response contract/client exists. |
| Required Jira permissions | Blocked | Not tested | Requires Jira account, project access, and rule/integration identity. |
| PostgreSQL durable execution state | Not implemented | Blocked | No schema, migration, repository, or database connection exists; Docker engine was unavailable. |
| Structured searchable logs | Not implemented | Not tested | `console.error` is the only server-side error output; no structured execution logging exists. |
| NFR-001 transient failures visible and recoverable | Not implemented | Not tested | No Jira calls, error classes, retry policy, or reconciliation exists. |
| NFR-002 at-most-one transition and marker | Not implemented | Not tested | No idempotency or concurrency implementation exists. |
| NFR-003 protected secrets | Partial | Not verified | Frontend has no Jira credentials; backend has no Jira credentials yet. Inbound authentication and secret storage are absent. |
| NFR-004 distinguish success/no-op/failure | Partial | Partially verified | Evaluator returns `close`, `reopen`, `noop`, and `ignored`; no success/failure execution lifecycle exists. |
| NFR-005 business rules testable without production credentials | Partial | Verified locally | Pure evaluator is locally testable; no automated test files or test runner cover it. |
| NFR-006 configurable status/transition mappings | Not implemented | Not tested | Only project key is a constant; status and transition mappings are not configurable. |
| NFR-007 disabled during workflow changes | Not implemented | Not tested | No enable/disable mechanism or deployment control exists. |
| React/Vite frontend boundary | Partial | Build verified | Frontend is a dashboard and calls the evaluator through Vite proxy; most displayed metrics and executions are static mock data. |
| Express backend boundary | Partial | Build and endpoint verified | Express server and routes work locally; domain/service, Jira, database, and auth layers are absent. |
| PostgreSQL 15 via Docker | Partial | Blocked | Compose service definition exists, but Docker Desktop Linux engine was stopped and database access was not verified. |
| Accessibility/responsive operator states | Partial | Build verified | Responsive CSS and basic labels exist; loading/error state is limited to the test button and offline pill, with no accessibility test. |

## 5. Error and Edge-Case Table

| Condition | Implemented? | Does it work? | Evidence and gap |
|---|---|---|---|
| Parent has no sub-tasks | Partial | Verified in evaluator | Returns no-op; no external action path exists. |
| Some sub-tasks are not Done | Partial | Verified | Returns no-op for supplied list. |
| Parent already Done during close | Partial | Logic present | Returns fallback no-op; no dedicated recorded test. |
| Parent not Done during reopen | Partial | Logic present | Returns fallback no-op; no dedicated recorded test. |
| Issue outside `ARE` | Partial | Verified | Returns ignored. |
| Issue not a sub-task | Partial | Verified | Returns ignored. |
| Sub-task has no parent | Partial | Verified | Returns ignored. |
| Close transition missing/fails | Not implemented | Not tested | No transition invocation or failure handling. |
| Reopen transition missing/fails | Not implemented | Not tested | No transition invocation or failure handling. |
| Jira rate-limited/transiently unavailable | Not implemented | Not tested | No Jira client or retry mechanism. |
| Assignee unavailable for mention | Not implemented | Not tested | No assignee lookup or notification path. |
| Malformed JSON body | Partial | Not verified | Express JSON middleware exists, but no dedicated malformed-JSON test was recorded. |
| Missing required event fields | Partial | Verified narrowly | `eventId` and `projectKey` are checked; all other required fields are not validated at runtime. |
| Unknown enum values | Not implemented | Not tested | TypeScript types are erased at runtime; arbitrary status categories can pass the cast. |

## 6. Acceptance Test Matrix

| ID | Acceptance test | Implemented? | Does it work? | Current evidence |
|---|---|---|---|---|
| AT-001 | Complete one of several sub-tasks; parent unchanged | Partial | Evaluator behavior likely works | Partial payload matrix was run and returned no-op; no parent exists to verify unchanged state. |
| AT-002 | Complete final sub-task; parent transitions to Done | Partial | Classification works; transition unverified | Close matrix returned `close`; no Jira parent transition occurs. |
| AT-003 | Parent with no sub-tasks unchanged | Partial | Evaluator no-op works | Empty list path exists; no Jira parent state to verify. |
| AT-004 | Sub-task leaves Done; parent reopens | Partial | Classification works; transition unverified | Reopen endpoint test returned expected action in prior verification. |
| AT-005 | Replayed event creates no duplicates | Not implemented | Not tested | No persistent state or duplicate check. |
| AT-006 | Failed transition produces diagnostic comment and notification | Not implemented | Not tested | No Jira integration or failure injection. |
| AT-007 | Other project ignored | Partial | Verified | Matrix returned ignored. |
| AT-008 | Non-sub-task ignored | Partial | Verified | Matrix returned ignored. |
| AT-009 | Logs distinguish outcomes | Not implemented | Not tested | No execution log store or query surface. |
| AT-010 | Daily refresh has no duplicate effects | Not implemented | Not tested | No daily refresh. |

## 7. Dependencies and Rollout

| Requirement | Implemented? | Does it work? | Evidence and gap |
|---|---|---|---|
| Close transition configured per supported parent type | Not implemented | Blocked | No Jira workflow discovery or mapping artifact is wired into runtime. |
| Reopen transition configured per supported parent type | Not implemented | Blocked | No Jira workflow discovery or mapping artifact is wired into runtime. |
| Jira Automation conditions/smart values confirmed | Not implemented | Blocked/not applicable to selected API path | No native Jira rule is configured. |
| All-sub-task evaluation method confirmed | Partial | Local list logic works | Jira retrieval method and pagination are absent. |
| Assignee mention syntax confirmed | Not implemented | Blocked | Requires Jira configuration access. |
| Rule/integration permissions confirmed | Not implemented | Blocked | Requires Jira account and project access. |
| Controlled test parent and mixed-status fixture | Not implemented | Blocked | No live Jira fixture is configured. |
| Acceptance suite passes before rollout | Not implemented | Not tested | No automated or live Jira acceptance suite exists. |
| Monitoring after rollout | Not implemented | Not tested | No production rollout or monitoring surface exists. |
| Revalidate after workflow changes | Not implemented | Not tested | No operational runbook or automated drift check exists. |

## 8. Missing Artifacts and Implementation Work

The following artifacts are required to close the gaps:

1. Typed Jira client and response/error contracts.
2. Authenticated webhook or event intake route with payload validation and replay protection.
3. PostgreSQL 15 schema/migrations for idempotency and execution records.
4. Idempotency repository and per-parent concurrency strategy.
5. Jira service for issue reads, transition discovery/execution, comments, and assignee lookup.
6. Retry, rate-limit, timeout, and ambiguous-outcome reconciliation policy implementation.
7. Exact close, reopen, and diagnostic comment templates.
8. Structured execution log schema, persistence, redaction, retention, and query endpoint/UI.
9. Daily refresh job, if enabled for version 1.
10. Automated unit, integration, reliability, and acceptance tests.
11. Live Jira test fixture and reset procedure.
12. Versioned workflow mapping/configuration artifact with startup validation.
13. Production authentication, secret management, monitoring, and rollback controls.
14. Frontend API-backed execution history and workflow checks; current dashboard data is mostly static.

## 9. Readiness Decision

**Not ready for production.** The current implementation is suitable as an early API/UI prototype and a locally verified decision-classification slice. It is not yet an implementation of the Jira automation feature because it has no Jira side effects, durable state, authentication, retries, notifications, execution logs, or acceptance environment.

The next implementation gate should be the approved application architecture’s integration foundation: typed Jira client, authenticated event intake, PostgreSQL migrations/repositories, and idempotency/concurrency design before adding transition mutations.
