---
description: Commit task changes with auto-generated message referencing task number
agent: coder
---

# Commit-EPCV Command

Commit all changed files with a message referencing the task number.

$ARGUMENTS

This command stages all changes and creates a commit with the format: `task-{n} {short description}` where the description is derived from the task title.

Follow these steps:

1. Determine the task number:
   - If a task number is provided in the arguments, use it
   - If no task number is provided, check Backlog.md for a task with status "In Progress"
   - If exactly one task is "In Progress", use that task number
   - If zero or multiple tasks are "In Progress", ask the user to specify the task number
2. Retrieve the task title from Backlog.md using `task_view`
3. Generate a short description from the task title (remove common prefixes like "Add", "Create", "Implement" if needed to keep it concise)
4. Stage all changes: `git add -A`
5. Create the commit with message format: `task-{n} {short description}`
6. Report the commit result to the user

## Usage

Commit with explicit task number:

```text
/commit-epcv 2
```

This will look up TASK-2 in Backlog.md and generate a commit like:
`task-2 Add commit command for task-based commits`

Commit with auto-inferred task (when one task is "In Progress"):

```text
/commit-epcv
```

The command will find the "In Progress" task and use its number and title.

## Examples

| Command            | Result                                                         |
| ------------------ | -------------------------------------------------------------- |
| `/commit-epcv 2`   | `task-2 Add commit command for task-based commits`             |
| `/commit-epcv 1.3` | `task-1.3 Add /code command for resuming after plan approval`  |
| `/commit-epcv`     | Uses the current "In Progress" task, or asks for clarification |
