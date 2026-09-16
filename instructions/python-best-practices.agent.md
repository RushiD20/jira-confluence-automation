# Python Best Practices

Write and review Python code that is clear, maintainable, testable, and consistent with the repository.

Core principles:
- Give each function, class, and module one clear responsibility.
- Prefer small, cohesive functions with descriptive names.
- Keep public interfaces simple and stable.
- Avoid duplicated logic; extract shared behavior only when the abstraction is clear.
- Prefer explicit control flow over clever or implicit behavior.
- Do not mix unrelated concerns such as data retrieval, business logic, formatting, and file I/O in one function.

Code style:
- Use 4-space indentation and follow standard Python formatting conventions.
- Use descriptive names; do not use one-letter names except for conventional small scopes.
- Add type annotations to function parameters, return values, and important data structures.
- Use docstrings for public modules, classes, and functions when their purpose is not obvious.
- Prefer `pathlib.Path` for filesystem paths.
- Use f-strings for readable string interpolation.
- Use context managers for resources that must be opened and closed.
- Keep imports organized and remove unused imports.
- Avoid mutable default arguments and broad exception handling.

Implementation workflow:
1. Inspect nearby code, tests, and project documentation before changing behavior.
2. Identify the owning module and keep the change within the smallest appropriate boundary.
3. Separate pure computation from side effects where practical.
4. Validate inputs at the boundary and raise clear, specific exceptions for invalid data.
5. Preserve existing public behavior unless a breaking change is explicitly requested.
6. Add or update focused tests for changed behavior and important edge cases.
7. Run the narrowest relevant tests, then run broader checks when the change affects shared code.

Testing expectations:
- Test observable behavior rather than implementation details.
- Keep tests deterministic and independent of execution order.
- Use representative inputs, boundary values, invalid inputs, and failure paths.
- Mock external systems only at their integration boundary.
- Do not weaken assertions merely to make a test pass.

Constraints:
- Do not introduce dependencies when the standard library or an existing project dependency is sufficient.
- Do not silently catch, ignore, or replace errors with misleading defaults.
- Do not change unrelated files or reformat unrelated code.
- Do not add comments that merely restate the code; document non-obvious decisions instead.
- Report unavailable tools, failing checks, and unresolved assumptions rather than hiding them.
