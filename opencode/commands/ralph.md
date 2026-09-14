---
description: Run a pre-approved batch of tasks through code → verify → fix → commit with the Ralph agent
agent: ralph
---

# Ralph batch run

Execute a pre-approved batch of tasks without further human interaction: each task is built by the coder-worker, verified by the verifier-worker, fixed up to 3 times on FAIL, and committed on PASS. Failed tasks are stashed and skipped; a batch report lands at the end.

$ARGUMENTS

Provide the batch one of two ways:

1. **Task list** — paste the approved task briefs (or reference them, e.g. "tasks 3–5 from the approved plan above")
2. **Milestone** — name a Backlog milestone and Ralph will pull its tasks

Preconditions (Ralph checks these before starting):

- The batch has already been approved at Gate #2 — Ralph never plans or approves
- The git working tree is clean
- Each task is atomic and independently committable

Follow these steps:

1. Load and follow the `ralph-batch-runner` skill
2. Confirm preconditions; if the tree is dirty, stop and ask the user
3. Run the task loop for each task in order (build → verify → fix ≤ 3 → commit, stash and skip on the fourth FAIL)
4. Produce the batch report: verdicts, attempts, commit hashes, stash refs, and failure details

## Usage

Run tasks from the approved plan in this conversation:

```text
/ralph Implement tasks 3-5 from the approved plan
```

Run a milestone's tasks:

```text
/ralph milestone: v1.2 release
```

## Examples

| Command                            | Result                                                      |
| ---------------------------------- | ----------------------------------------------------------- |
| `/ralph Implement tasks 3-5 above` | Runs tasks 3–5 through code → verify → fix → commit         |
| `/ralph milestone: v1.2 release`   | Pulls the milestone's tasks from Backlog and runs the batch |
| `/ralph TASK-4 TASK-7`             | Runs the named Backlog tasks as a batch                     |
