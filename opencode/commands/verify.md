---
description: Phase 4 of EPCV — validate an implementation with four layered checks, produce PASS / PASS_WITH_WARNINGS / FAIL
agent: verifier
---

# Verify

Verify these changes:

$ARGUMENTS

Follow the `verifying-changes` skill. Requires an implementation report from `/code`. On FAIL the report includes fix instructions — hand back to `/code`; on PASS recommend `/commit-task`.
