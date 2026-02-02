---
description: Review existing code for quality and correctness
agent: verifier
subtask: true
---

Verify the following code or changes:

$ARGUMENTS

Run a full verification using four layered checks:
1. **Automated**: Run tests, linting, type checks, and build validation
2. **Behavioural**: Check edge cases, failure paths, and user-facing behaviour
3. **Operational**: Review error handling, logging, configuration, and rollback
4. **Security**: Check input validation, output encoding, authorisation, secrets management, logging hygiene, and dependency security

Produce a verification report with a clear PASS / FAIL / PASS_WITH_WARNINGS status, including issues found with severity and specific fix instructions for any failures.
