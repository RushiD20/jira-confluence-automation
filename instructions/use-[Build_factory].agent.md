# Use Build Factory

Use `tools/Build_factory.py` to generate a local JSON definition of the Jira close-parent automation path for project `ARE`.

When to use:
- Use it when documenting or preparing the close-parent path for a sub-task transitioned into Jira's Done status category.
- Use it when a local automation definition is needed for review, configuration mapping, or testing.
- Do not use it to apply changes directly to Jira; the script only writes JSON files locally.
- Do not use it for the reopen-parent path, scheduled refresh logic, or live workflow validation.

How to invoke:
- Run the command from the repository root.
- Pass one or more output paths as positional command-line arguments.

```powershell
python tools/Build_factory.py <output-path>
```

Example:

```powershell
python tools/Build_factory.py work/close-parent-automation.json
```

- The output path must identify a JSON file location. Parent directories are created automatically.
- Multiple output paths may be supplied when the same definition is needed in more than one location.

Generated path contents:
- Rule name: `Close Parent When Sub-Tasks Finish`.
- Project condition: `ARE`.
- Trigger: a sub-task is transitioned into the Done status category.
- Conditions: the issue is an `ARE` sub-task with a parent; the parent has at least one sub-task; all parent sub-tasks are Done; and the parent is not already Done.
- Branch: the parent issue.
- Actions: add the searchable idempotency marker, then transition the parent to `DONE`.
- Failure requirements: add a diagnostic comment containing the condition, attempted transition, available failure reason, required manual action, and parent-assignee mention.

Validation:
1. Confirm the output path is suitable for a local JSON artifact.
2. Run the command and verify it reports `Automation path written to:` for each path.
3. Parse or inspect the generated JSON before using it as a Jira configuration reference.
4. Confirm the exact workflow transition names, smart values, permissions, and assignee mention syntax in Jira before live configuration.
5. Report command failures and do not treat a generated local definition as proof that the Jira rule is active.

Constraints:
- Do not supply credentials or API tokens to the script.
- Do not overwrite important files without confirming the output path.
- Do not assume `DONE` is a valid transition until the `ARE` workflow has been verified.
- Keep the generated definition aligned with `project_spec.md` and the current Jira Automation rule builder.
