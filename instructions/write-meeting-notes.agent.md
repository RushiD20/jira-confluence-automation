# Extract Meeting Action Items

Extract action items and deadlines from meeting notes.

Input format:
- Accept meeting notes as plain text or Markdown.
- Treat headings, paragraphs, bullets, speaker labels, timestamps, and tables as source content.
- Use any meeting date or timezone stated in the notes when interpreting relative deadlines.
- Do not require a specific meeting-notes template.

Processing steps:
1. Read the complete meeting notes before extracting items.
2. Identify explicit commitments, assigned tasks, follow-ups, decisions that require action, and stated deadlines.
3. Separate actionable work from discussion points, background information, and completed work.
4. Associate each action with the responsible person or team when explicitly stated or clearly indicated by the notes.
5. Convert deadlines to an unambiguous date when the meeting date and context make that possible; otherwise preserve the original wording.
6. Mark missing owners or deadlines as `Unassigned` or `Not specified`.
7. Remove duplicate actions while preserving meaningful differences in owners or deadlines.
8. Keep the wording concise and faithful to the source; do not invent tasks, owners, dates, or priorities.
9. Check the extracted list against the notes for omissions, unsupported details, and duplicate entries.

Output format:
```markdown
## Action Items

| Action | Owner | Deadline |
|---|---|---|
| ... | ... | ... |

## Unresolved Details
- ...
```

Output rules:
- Include one table row per distinct action item.
- Use `Unassigned` when no owner is identified.
- Use `Not specified` when no deadline is identified.
- Put ambiguous dates, owners, or action wording in `Unresolved Details`.
- Include `## Unresolved Details` only when unresolved details exist.
- Preserve the source's timezone or date wording when normalization would be uncertain.
- Do not include a summary, recommendations, or actions that are not supported by the notes.

Constraints:
- Use Markdown only.
- Keep the output concise and focused on action items and deadlines.
- Do not exceed 30 table rows unless the input contains more than 30 distinct action items.
- Do not infer ownership from attendance alone.
- Do not treat every statement containing a future date as an action unless work or follow-up is required.
- Do not silently discard an action because its owner or deadline is missing.
