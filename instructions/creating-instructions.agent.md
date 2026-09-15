# Create Agent Instructions

Create or update an agent instruction file for this repository.

Requirements:
- Write the instruction file in Markdown.
- State the instruction's purpose and intended task clearly.
- Define the expected inputs and required outputs.
- Specify constraints, validation rules, and failure handling.
- Prefer concise, actionable rules over explanations.
- Match the repository's existing terminology and formatting.
- Do not invent project-specific facts that were not provided.
- Preserve existing behavior when updating an instruction file unless a change is explicitly requested.

Workflow:
1. Inspect nearby instruction files and relevant repository documentation.
2. Identify the task, audience, inputs, outputs, and acceptance criteria.
3. Draft the smallest complete instruction set that satisfies those criteria.
4. Check for ambiguous, contradictory, duplicated, or unverifiable rules.
5. Review the final file for clarity, consistent Markdown, and actionable language.

Output format:
- Return the complete instruction file in Markdown.
- Use headings and bullet lists where they improve scanning.
- Include an example output or template when the requested task has a structured result.
- Do not include commentary outside the instruction file.

Quality checks:
- Every required behavior has a corresponding rule.
- Rules are specific enough for an agent to follow without guessing.
- Requirements are ordered from purpose and inputs through workflow and validation.
- The instruction does not contain irrelevant implementation details.
