# Set Up a Project

Create or initialize a complete project structure that is runnable, maintainable, and appropriate for the stated requirements.

Inputs:
- Accept the project purpose, target users, required features, preferred language or framework, runtime version, integrations, and expected commands when provided.
- Treat existing files, configuration, documentation, and repository conventions as constraints.
- Ask for clarification or state an explicit assumption when a missing requirement materially affects the architecture.
- Do not replace or discard existing user work.

Processing steps:
1. Inspect the workspace, existing project files, version-control state, and relevant documentation.
2. Translate the requirements into a minimal list of capabilities, entry points, dependencies, configuration values, and validation checks.
3. Choose the smallest established stack that satisfies the requirements and matches the repository.
4. Design a clear directory structure with one ownership boundary per component.
5. Create the application code, configuration, dependency metadata, documentation, and focused tests required to run the project.
6. Use environment variables or documented configuration for secrets; never hard-code credentials or tokens.
7. Add sensible error handling and a clear startup or execution path.
8. Run the installation, build, lint, type-check, and test commands that apply to the selected stack.
9. Verify the primary workflow and record any unavailable tools, assumptions, or unresolved failures.

Project requirements:
- Keep modules cohesive and follow the repository's existing naming and formatting conventions.
- Pin or constrain dependencies using the ecosystem's standard project metadata when reproducibility requires it.
- Provide a README with prerequisites, setup, configuration, run commands, test commands, and troubleshooting for expected failures.
- Include a safe example configuration such as `.env.example` when environment variables are required.
- Add tests for the primary workflow, important edge cases, and failure paths.
- Keep generated files, caches, local secrets, and machine-specific settings out of version control.
- Make commands work from the documented working directory.

Output format:
1. Provide the created or updated project files.
2. Summarize the architecture, entry point, dependencies, and configuration requirements.
3. List the exact setup and validation commands that were run and their results.
4. State assumptions, deferred work, and any remaining failures explicitly.

Constraints:
- Do not introduce a framework or dependency without a requirements-based reason.
- Do not modify unrelated files or perform destructive migrations.
- Do not commit changes unless explicitly requested.
- Do not expose secrets in source files, logs, documentation, or command output.
- Do not claim the project is working when required validation could not be run.
