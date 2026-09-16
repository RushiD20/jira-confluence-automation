# Write Python Tests

Create focused, deterministic tests that verify observable Python behavior and protect the requested contract.

Inputs:
- Accept the behavior description, implementation under test, expected inputs and outputs, side effects, and failure conditions.
- Inspect the target module, callers, nearby tests, and project documentation before writing tests.
- Follow the repository's existing test framework and naming conventions; use `unittest` when extending the current test suite.

Processing steps:
1. Identify the public behavior and acceptance criteria to test.
2. Choose the established test location and a descriptive test class and method name.
3. Cover the normal path first, then relevant boundary, invalid-input, and failure cases.
4. Assert returned values, exceptions, persisted output, and other observable effects rather than private implementation details.
5. Isolate each test from filesystem, network, time, randomness, environment variables, and test execution order.
6. Use temporary directories or equivalent fixtures for filesystem tests and clean up resources reliably.
7. Mock external systems only at their integration boundary; do not mock the behavior being verified.
8. Keep test data minimal but representative, including values that distinguish similar behaviors.
9. Run the narrowest relevant test command, inspect failures, and fix the test or implementation only when the evidence supports it.

Test requirements:
- Give each test one clear reason to fail.
- Use descriptive names that state the behavior and condition being tested.
- Keep tests independent, repeatable, and deterministic.
- Verify exception type and meaningful details when error behavior is part of the contract.
- Include regression coverage for every bug or behavior change being addressed.
- Preserve existing tests and assertions unless the intended behavior has explicitly changed.

Output format:
1. Add or update focused test files in the repository's established test location.
2. Summarize the behaviors covered and any assumptions.
3. Report the exact validation command and its result.
4. Report unresolved failures or unavailable test tooling explicitly.

Constraints:
- Do not weaken assertions, skip failing tests, or add broad exception handling to hide failures.
- Do not test implementation details that prevent safe refactoring.
- Do not introduce a new testing framework or dependency when the existing project setup is sufficient.
- Do not change production code solely to make a poorly specified test pass; clarify the contract or report the ambiguity.
- Do not modify unrelated files or reformat unrelated tests.
