# Task and Specification Analysis

**Reviewed:** [specification.md](specification.md), [plan.md](plan.md), [tasks.md](tasks.md), [clarify.md](clarify.md)  
**Review date:** 2026-09-16  
**Scope:** Complexity, risks, dependencies, traceability, and missing artifacts

## 1. Executive Summary

The task backlog is well aligned with the plan’s seven phases and covers the principal behavior: close, reopen, no-op, ignore, idempotency, failure handling, acceptance testing, rollout, and operations. The highest-risk work is concentrated in architecture selection, Jira workflow behavior, idempotency under concurrency, partial external-call outcomes, and production permissions.

The backlog is not yet implementation-ready for an application-backed architecture because several concrete implementation artifacts are only implied. Native Jira Automation has the opposite risk: the constitution’s typed services, PostgreSQL durability, retry behavior, and structured logging requirements may require an explicit exception or a hybrid design.

**Overall assessment:** High complexity, high integration risk, and conditional readiness. Phase 0 and Phase 2 decisions should be completed before coding begins.

## 2. Complexity Scale

- **Low:** Narrow documentation, configuration, or verification work with limited branching.
- **Medium:** Bounded implementation or testing work with one major integration boundary.
- **High:** Cross-system behavior involving concurrency, external mutations, retries, permissions, data integrity, or production rollout.

## 3. Task-by-Task Assessment

### Phase 0: Architecture and Scope Gate

| Task | Complexity | Primary risks | Dependencies |
|---|---|---|---|
| T-001 Choose implementation architecture | High | Choosing native Jira Automation may conflict with constitution requirements; hybrid ownership may duplicate side effects. | None |
| T-002 Record architecture rationale and exceptions | Medium | Exception may omit affected principles, expiry, or compensating controls. | T-001 |
| T-003 Assign feature ownership | Low | Ownership may be named but lack escalation authority or Jira access. | T-001 |
| T-004 Decide daily refresh scope | Medium | Optional refresh affects task dependencies, test scope, scheduling, and operational load. | T-001 |
| T-005 Confirm Confluence boundary | Low | Hidden Jira-to-Confluence expectations could surface later. | T-001 |

**Phase assessment:** T-001 is the critical gate. T-004 must explicitly change downstream milestone rules when refresh is deferred.

### Phase 1: Access and Workflow Discovery

| Task | Complexity | Primary risks | Dependencies |
|---|---|---|---|
| T-006 Verify Jira site and project access | Medium | Existing access restrictions may block all live validation. | T-003 |
| T-007 Verify rule actor permissions | High | Permission differences between browsing, transitioning, commenting, and notifying can invalidate tests. | T-006 |
| T-008 Identify supported parent issue types | Medium | Different parent types may use different workflows or lifecycle rules. | T-006 |
| T-009 Confirm sub-task relationship behavior | Medium | Orphaned, archived, or cross-project relationships may not behave as assumed. | T-006, T-008 |
| T-010 Confirm Done status-category authority | Medium | Status category, status name, resolution, and workflow post-functions may diverge. | T-008 |
| T-011 Validate close transition configuration | High | Transition availability and target status can vary by issue type and permission. | T-008, T-010 |
| T-012 Validate reopen transition configuration | High | Some workflows may have no valid reopen path or may require additional fields. | T-008, T-010 |
| T-013 Validate transition event data | High | The selected trigger may not expose all fields needed for deterministic idempotency. | T-006, T-010 |
| T-014 Validate comment mention and notification behavior | High | Jira mention syntax, inactive users, notification settings, and comment permissions may differ. | T-007 |
| T-015 Record integration prerequisites | Medium | Evidence may become stale or fail to identify the blocking owner. | T-006 through T-014 |

**Phase assessment:** T-011 through T-014 are externally dependent and should produce durable evidence, not informal confirmation. T-006 is a release blocker if project access is unavailable.

### Phase 2: Contracts and Operational Design

| Task | Complexity | Primary risks | Dependencies |
|---|---|---|---|
| T-016 Define inbound event contract | High | Missing fields or unstable event IDs can make replay protection and correlation unreliable. | T-001, T-013 |
| T-017 Define evaluation result model | Medium | `success`, `noop`, `ignored`, and `partial_success` can be interpreted inconsistently. | T-016 |
| T-018 Define idempotency key | High | Keys that are too broad suppress valid work; keys that are too narrow permit duplicates. | T-016, T-017 |
| T-019 Define idempotency state machine | High | External side effects are not atomic; unknown outcomes require reconciliation. | T-018 |
| T-020 Define concurrency strategy | High | Jira reads and mutations can race across workers, rules, or scheduled refreshes. | T-019 |
| T-021 Define comment templates | Medium | Templates must be machine-detectable, safe, size-bounded, and compatible with Jira markup. | T-014, T-019 |
| T-022 Define retry and rate-limit policy | High | Incorrect retries can duplicate transitions or amplify Jira outages. | T-017, T-019 |
| T-023 Define execution log contract | Medium | Logs may expose issue content or fail to support operational queries. | T-017, T-018 |
| T-024 Define runtime configuration | Medium | Invalid mappings or unsafe defaults can cause broad incorrect transitions. | T-011, T-012, T-022 |
| T-025 Define security and privacy controls | High | Webhook replay, token leakage, excessive scopes, and personal-data retention are material risks. | T-016, T-023, T-024 |
| T-026 Define test fixture and environment strategy | Medium | Live Jira tests may be non-repeatable or notify unintended users. | T-016 through T-025 |

**Phase assessment:** T-018 through T-020 form the highest technical-risk cluster. T-025 depends on the architecture decision and must branch clearly for native Jira Automation versus an Express endpoint.

### Phase 3: Event Qualification and Evaluation

| Task | Complexity | Primary risks | Dependencies |
|---|---|---|---|
| T-027 Implement input validation and scope guards | Medium | Malformed or incomplete events could trigger unintended mutations. | T-016, T-017 |
| T-028 Implement complete sub-task evaluation | High | Pagination, incomplete responses, deleted issues, and stale reads can cause false closure. | T-009, T-010, T-016 |
| T-029 Implement close decision logic | Medium | A wrong parent or status-category interpretation can close active work. | T-027, T-028 |
| T-030 Implement reopen decision logic | Medium | Reopen events may be missed or generated for a parent that is no longer Done. | T-027, T-028 |
| T-031 Implement no-op and ignored reasons | Low | Inconsistent reason codes make logs and metrics unreliable. | T-029, T-030 |
| T-032 Add decision-layer unit tests | Medium | Tests may validate mocks rather than the actual decision contract. | T-027 through T-031 |

**Phase assessment:** This is the most suitable phase for deterministic unit testing. No Jira mutation should occur before M-3.

### Phase 4: Side Effects and Reliability

| Task | Complexity | Primary risks | Dependencies |
|---|---|---|---|
| T-033 Implement pre-mutation re-read | High | The parent can change again between the read and mutation. | T-019, T-029, T-030 |
| T-034 Implement idempotency and concurrency guard | High | Distributed workers or separate Jira rules may bypass a local lock. | T-018 through T-020 |
| T-035 Implement execution registration | High | PostgreSQL and Jira state can diverge; native Jira may not provide equivalent durable state. | T-019, T-023, T-034 |
| T-036 Implement marker comment handling | High | Comment-before-transition ordering can leave misleading markers after failed transitions. | T-021, T-034 |
| T-037 Implement Jira transition execution | High | Workflow fields, permissions, rate limits, and transition ambiguity can fail at runtime. | T-011, T-012, T-033 through T-036 |
| T-038 Implement post-transition verification | High | Eventual consistency or a successful response with stale data can produce false failure/retry. | T-037 |
| T-039 Implement diagnostic comments and notifications | High | Repeated failures can spam assignees; notification success is not guaranteed by comment success. | T-014, T-021, T-037 |
| T-040 Implement retry and reconciliation handling | High | Retrying an unknown transition outcome can duplicate a state change. | T-019, T-022, T-037, T-038 |
| T-041 Implement redacted structured logging | Medium | Logs may be incomplete, unsearchable, or leak user and issue data. | T-023, T-025, T-035 |
| T-042 Implement daily refresh | High | Scheduling, pagination, overlap, and broad mutation scope can create load or duplicate work. | T-004, T-028 through T-041 |
| T-043 Add reliability and integration tests | High | Failure injection across Jira, database, scheduler, and notifications is difficult to reproduce. | T-033 through T-042 |

**Phase assessment:** T-034, T-036, T-038, T-039, and T-040 must be designed as one failure model. Treating them as independent implementation tasks risks contradictory recovery behavior.

### Phase 5: Integration and Acceptance Testing

| Task | Complexity | Primary risks | Dependencies |
|---|---|---|---|
| T-044 Provision controlled test parent | Medium | Fixture reset and issue ownership may be unreliable. | T-015, T-026 |
| T-045 Isolate interfering automations | High | Other Jira rules or workflow post-functions may change the result or create loops. | T-044 |
| T-046 Run close-path acceptance tests | Medium | Live status transitions may not match mocked assumptions. | T-044, T-045, M-4 |
| T-047 Run reopen-path acceptance tests | Medium | Reopen target and required workflow fields may vary by parent type. | T-044, T-045, M-4 |
| T-048 Run duplicate and failure acceptance tests | High | Duplicate notifications and ambiguous external outcomes are hard to force safely. | T-044, T-045, M-4 |
| T-049 Run daily refresh acceptance test | Medium | Scheduler timing and overlap make the test environment nondeterministic. | T-004, T-042, T-044 |
| T-050 Obtain release-candidate sign-off | Low | Sign-off may overlook untested exceptions or incomplete evidence. | T-046 through T-049 |

**Phase assessment:** T-045 and T-048 are the main acceptance-test risks. A resettable fixture and explicit test evidence are required before sign-off.

### Phase 6: Deployment and Controlled Rollout

| Task | Complexity | Primary risks | Dependencies |
|---|---|---|---|
| T-051 Validate production configuration | High | A wrong mapping or secret can affect every eligible parent. | M-5 |
| T-052 Deploy application and database changes | High | Migration failure, incompatible configuration, or unhealthy service can block processing. | T-051; application-backed or hybrid only |
| T-053 Configure native Jira rule or webhook integration | High | Rule ordering, webhook security, and duplicate trigger paths can produce side effects. | T-051; native or hybrid only |
| T-054 Execute controlled rollout | High | Even a small production scope can contain unexpected workflows or notifications. | T-050 through T-053 |
| T-055 Expand to production scope | High | Broad enablement can amplify a hidden logic or configuration error. | T-054 |
| T-056 Verify rollback and disablement | High | In-flight and unknown external calls may remain unreconciled after disablement. | T-054 |

**Phase assessment:** T-054 should be a real canary with a fixed observation window, not merely a configuration toggle. T-056 should be tested before broad enablement where possible.

### Phase 7: Operations and Maintenance

| Task | Complexity | Primary risks | Dependencies |
|---|---|---|---|
| T-057 Publish operations runbook | Medium | Runbook may describe intended rather than actual deployed behavior. | M-6 |
| T-058 Establish monitoring review cadence | Medium | Thresholds may be absent, noisy, or disconnected from escalation. | T-057 |
| T-059 Maintain workflow-change validation | Medium | Workflow changes can silently invalidate transition mappings or rule conditions. | T-057 |
| T-060 Manage retention and secret rotation | High | Deleting state too early can impair reconciliation; stale secrets can remain active. | T-023, T-025, T-057 |
| T-061 Complete operational handoff | Low | Formal handoff can occur without a proven first review or usable monitoring. | T-057 through T-060 |

**Phase assessment:** T-060 is operationally high risk despite being maintenance work because retention and secret rotation affect recovery and security.

## 4. Cross-Document Traceability Review

### Consistent areas

- The main close and reopen behaviors are represented in the specification, plan, and tasks.
- The no-sub-task, partial-completion, out-of-scope, retry, diagnostic-comment, and acceptance-test behaviors are traceable.
- The plan correctly treats architecture choice and exact workflow identifiers as technical/deployment decisions rather than feature-scope requirements.
- The task milestones map in order to the plan milestones M-0 through M-7.

### Contradictions or ambiguities

#### A-001: Native Jira Automation versus application-backed implementation remains unresolved

The plan recommends the Express/PostgreSQL application but permits native Jira Automation with an exception. The tasks retain both implementation paths. Until T-001 is complete, it is impossible to determine whether database migrations, webhook authentication, typed Jira clients, or native rule configuration are required.

**Impact:** High. Phase 2 through Phase 6 work can branch substantially.

**Resolution:** Complete T-001 and T-002 before implementation tasks begin. Mark non-selected tasks explicitly `Deferred` rather than merely conditional.

#### A-002: Daily refresh conditionality is not propagated consistently

T-042 and T-049 are conditional, but T-043 depends on `T-033 through T-042`, and M-4 requires T-033 through T-043 to be complete. If refresh is deferred, the backlog does not define whether T-042 and T-049 are skipped, marked not applicable, or replaced by another gate.

**Impact:** Medium to high. Milestone completion can be blocked by an intentionally deferred task.

**Resolution:** Add a task state of `N/A - deferred` and define milestone acceptance as “all required tasks complete and all conditional tasks either complete or explicitly deferred.”

#### A-003: Feature actor and selected architecture are inconsistent

The specification names the Jira Automation rule actor as the primary actor. The plan recommends an application-backed service, which would introduce an integration identity and possibly a webhook sender as additional actors.

**Impact:** Medium. Authorization and audit ownership are unclear.

**Resolution:** After T-001, update the specification metadata or plan with the actual actors and identity ownership.

#### A-004: Exact transition identifiers are out of feature scope but required by multiple task gates

The specification correctly excludes exact IDs and names from feature behavior, but T-011, T-012, T-024, T-037, and T-051 require them operationally. This is not a defect, but the artifact that stores the mappings is not named consistently.

**Impact:** Medium. Configuration may exist only in an operator’s notes or environment variables.

**Resolution:** Create a versioned, non-secret workflow mapping artifact with environment-specific secret/configuration handling and a validation command or checklist.

#### A-005: Marker-before-transition ordering is not reconciled with failure handling

The specification requires a marker before action, while the plan includes retries, postcondition checks, and partial-success states. The task list does not define whether a marker means “evaluation started,” “transition authorized,” or “transition completed.”

**Impact:** High. A retry may either duplicate a transition or incorrectly suppress recovery.

**Resolution:** T-019 and T-021 must define marker semantics and T-036/T-040 must implement reconciliation against both marker and current Jira status.

#### A-006: `partial_success` is designed but not represented in the feature acceptance criteria

The plan and tasks include `partial_success`, but the specification’s success criteria and acceptance matrix mainly distinguish successful, no-op, and failed outcomes.

**Impact:** Medium. Operators and tests may classify successful transition plus failed notification inconsistently.

**Resolution:** Add explicit acceptance scenarios for marker-written/transition-failed, transition-succeeded/verification-uncertain, and transition-succeeded/notification-failed outcomes, or remove `partial_success` from the result model.

#### A-007: Jira Automation and Express security controls are described together

T-025 mentions webhook authentication “if applicable,” while the specification requires webhook controls only through the constitution if an Express service is chosen. The plan does not define a branch-specific security artifact.

**Impact:** High. A native rule and an Express webhook have different trust boundaries.

**Resolution:** Create branch-specific security requirements after T-001: Jira rule security configuration for native mode, or authentication/signature/replay/schema controls for application mode.

#### A-008: Acceptance tests refer to issue history and execution logs without defining the evidence format

The specification requires visible execution records, while tasks require matching history and logs. No test evidence template, log query, screenshot policy, or export format is defined.

**Impact:** Medium. Sign-off may be subjective and not reproducible.

**Resolution:** Add an acceptance evidence template and require each test to record event input, expected state, observed state, comment IDs/markers, notification result, and log correlation ID.

## 5. Missing Artifacts and Tasks

### Blocking or high-priority missing artifacts

1. **Architecture decision record**
   - Needed by T-001/T-002.
   - Must record selected architecture, ownership, exception status, and branch-specific deliverables.

2. **Workflow mapping artifact**
   - Needed by T-011, T-012, T-024, T-037, and T-051.
   - Must map supported parent type to close/reopen transition and target status without embedding secrets.

3. **Implementation contract artifacts**
   - Needed by T-016 through T-025.
   - Include event schema, result enum, idempotency state machine, retry matrix, comment templates, log schema, configuration schema, and security model.

4. **Application entry-point and Jira client tasks**
   - The application-backed path has no explicit task to implement the Express webhook route, Jira client, authentication middleware, payload validation, or centralized error handling.

5. **Database implementation tasks**
   - The plan mentions a migration and repositories, but the backlog has no explicit task to create the PostgreSQL migration, idempotency repository, execution repository, indexes, or transaction behavior.

6. **Native-rule configuration artifact**
   - The native path needs a versioned rule design/export or configuration checklist, including conditions, branches, error paths, and known Jira Automation limitations.

7. **Deployment and configuration artifact**
   - T-051 validates configuration but no task creates environment templates, startup validation, Docker Compose database configuration, or deployment manifests.

8. **Acceptance evidence template**
   - Required to make T-046 through T-050 auditable and repeatable.

9. **Operations runbook artifact**
   - T-057 creates it, but no path or format is specified, and it is not linked from the plan’s deliverables.

10. **CI quality-gate task**
    - The constitution requires type checking, linting, tests, and builds where configured, but no task establishes or verifies a CI command sequence.

### Medium-priority missing tasks

- Define API/UI requirements if the selected application architecture exposes execution logs or manual retry operations.
- Add a task for Jira client contract tests against representative Jira responses.
- Add a task for database migration rollback or backward compatibility testing.
- Add a task for event replay protection and webhook signature verification in application mode.
- Add a task for configuration drift detection after Jira workflow changes.
- Add a task for performance/load testing of daily refresh and concurrent events.
- Add a task for conflict detection with existing Jira Automation rules and workflow post-functions.
- Add a task for incident simulation after an ambiguous transition timeout.
- Add a task for data retention verification and log redaction testing.

## 6. Dependency and Sequencing Issues

1. **T-035 is underspecified for application mode.** It should depend on explicit database schema and repository tasks, not only design tasks.
2. **T-037 depends on “T-033 through T-036,” but Jira client implementation is not an explicit predecessor.** Add a Jira integration task before transition execution.
3. **T-040 depends on T-037 and T-038, but retry policy may need a testable client abstraction before either task.** Add the client/error-classification task earlier.
4. **T-042’s conditional status is not reflected in M-4 or T-043.** Define deferred-task handling.
5. **T-052 says “database migrations, if selected,” but no task creates or tests those migrations.** Add explicit schema/repository tasks.
6. **T-053 combines native rule and webhook integration.** Split it into native-rule configuration and application webhook deployment if both paths remain possible.
7. **T-056 occurs after controlled rollout but does not precede T-055.** For a high-risk automation, rollback readiness should be verified before expanding to all production parents.
8. **T-057 begins only after M-6, although monitoring and the runbook are needed during T-054.** Move a minimum monitoring/runbook version before controlled rollout and retain the full runbook for handoff.
9. **T-060 depends on T-023 and T-025 but not on the actual persistence/log implementation.** Add dependencies on the selected storage and logging tasks.
10. **T-046 through T-049 depend on M-4, but M-4 includes all reliability tests in T-043.** This is reasonable for release testing, but the plan should distinguish automated preconditions from live Jira acceptance tests to avoid circular sign-off expectations.

## 7. Recommended Remediation Backlog

Add these tasks before or during implementation:

- **T-062:** Create and approve the architecture decision record.
- **T-063:** Create the versioned workflow mapping and configuration artifact.
- **T-064:** Implement the typed Jira client and error classification layer for application mode.
- **T-065:** Implement the Express webhook route, authentication, replay protection, payload validation, and centralized error handling for application mode.
- **T-066:** Create PostgreSQL migrations, indexes, idempotency repository, execution repository, and transaction tests for application mode.
- **T-067:** Create the native Jira Automation rule design/export and constitution-exception evidence for native mode.
- **T-068:** Create branch-specific deployment manifests, environment templates, Docker Compose database configuration, and startup validation.
- **T-069:** Create the acceptance evidence template and test reset checklist.
- **T-070:** Add CI quality gates for type checking, linting, unit tests, integration tests, and build verification.
- **T-071:** Add partial-success acceptance scenarios and notification-failure classification.
- **T-072:** Verify rollback readiness before production-scope expansion.
- **T-073:** Publish minimum monitoring and escalation coverage before the controlled rollout.

## 8. Recommended Complexity and Risk Priorities

### Start first

- T-001/T-002: Architecture and exception decision.
- T-006/T-007: Access and permissions.
- T-011/T-012: Workflow transition validation.
- T-018/T-019/T-020: Idempotency and concurrency design.

### Protect with additional review

- T-028: Complete sub-task evaluation.
- T-034/T-036: Concurrency and marker side effects.
- T-037/T-038/T-040: External transitions, postconditions, and retries.
- T-039: Diagnostic comments and notifications.
- T-048: Duplicate and failure testing.
- T-054/T-055/T-056: Controlled rollout and rollback.

### Do not defer

- Workflow mapping artifact.
- Security boundary and authentication design.
- Database and execution-state implementation for application mode.
- Acceptance evidence format.
- Monitoring and escalation before enablement.

## 9. Readiness Gate

The backlog is ready to enter implementation when:

- T-001 through T-005 are complete and the non-selected architecture branch is marked deferred.
- T-006 through T-015 have verified evidence, not only verbal confirmation.
- T-016 through T-026 are approved as concrete artifacts.
- The missing application/native artifacts in Section 5 are assigned tasks and owners.
- Conditional daily-refresh tasks have explicit `required` or `N/A - deferred` status.
- Partial-success outcomes are represented consistently in the specification, plan, tasks, tests, and logs.
- Rollback, minimum monitoring, and acceptance evidence are available before controlled rollout.

## 10. Final Assessment

The task breakdown is a strong planning baseline but should not be treated as implementation-complete. The central remaining risk is not the close/reopen decision logic; it is the boundary between Jira’s external state and the automation’s durable execution state. Resolve architecture, workflow evidence, idempotency, and artifact ownership first. Then add the missing integration, persistence, security, CI, and evidence tasks before starting production-facing work.
