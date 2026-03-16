---
description: Implement an atomic task from an approved plan
agent: coder
---

# Code Command

Implement the following atomic task:

$ARGUMENTS

This command is designed for executing individual atomic tasks from an approved plan.

Follow these steps:

1. Review the task specification and task brief (from conversation context or provided arguments)
2. If no task spec exists, ask the user to run `/plan` first or provide the task details
3. Read every file before modifying it
4. Verify files are NOT on the do-not-touch list before editing
5. Implement the task following existing patterns precisely
6. Document any deviations from the task spec
7. Produce an implementation report with acceptance criteria status

After implementation, the user should run `/verify` to validate the changes, then `/commit-epcv` to commit.

## Usage

With task context from a prior `/plan` run:

```text
/code Implement task 1 from the approved plan
```

With explicit task details:

```text
/code Add input validation to the signup form — scope: src/auth/signup.ts, patterns: use zod schema validation matching existing forms
```
