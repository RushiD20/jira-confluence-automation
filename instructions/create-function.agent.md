# Create a Python Function

Design and implement one focused Python function that is clear, testable, and consistent with the repository.

Inputs:
- Accept a plain-language description of the function's purpose and expected behavior.
- Identify required parameters, optional parameters, accepted types, return value, side effects, and error conditions from the request and nearby code.
- Inspect the owning module, callers, related helpers, and tests before choosing a signature.
- Preserve existing naming, typing, and exception conventions when extending an existing module.

Processing steps:
1. State the function's single responsibility and its contract.
2. Choose a descriptive verb-based name and a minimal parameter list.
3. Add type annotations for parameters and the return value.
4. Separate validation, core computation, and side effects where practical.
5. Handle boundary cases and invalid inputs explicitly.
6. Raise a specific, documented exception when the function cannot complete its contract; do not silently return a misleading default.
7. Keep the implementation small and avoid unrelated refactoring or new dependencies.
8. Add focused tests for normal behavior, boundary values, invalid inputs, and relevant failure paths.
9. Run the narrowest relevant tests and static checks, then report any unresolved failures.

Implementation requirements:
- Follow 4-space indentation and the repository's formatting conventions.
- Use descriptive names and avoid one-letter variables except in conventional small scopes.
- Use a docstring when the function's behavior, parameters, return value, or exceptions are not self-explanatory.
- Avoid mutable default arguments, hidden global state, unnecessary mutation, and broad exception handling.
- Do not mix unrelated responsibilities such as persistence, network calls, formatting, and business logic without a clear contract.
- Preserve backward compatibility for existing callers unless a breaking change is explicitly requested.

Output format:
1. Provide the implemented function in its owning module.
2. Provide or update focused tests in the repository's established test location.
3. Summarize the function contract, changed files, and validation commands.
4. Report assumptions, unavailable tools, and failing checks explicitly.

Quality constraints:
- The function must have one clear reason to change.
- The signature must be no broader than the requested behavior requires.
- Tests must assert observable behavior rather than implementation details.
- Do not weaken existing tests or change unrelated behavior to make validation pass.
