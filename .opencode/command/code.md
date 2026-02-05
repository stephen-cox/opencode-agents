---
description: Execute the Code → Verify → Commit loop for an approved plan
agent: epcv-orchestrator
---

# Code Command

Execute the Code → Verify → Commit phases for a previously approved plan.

$ARGUMENTS

This command is designed to resume after `/plan` has been run and the plan has been approved. It skips the Explore and Plan phases and proceeds directly to implementation.

Follow these steps:

1. Confirm that a plan exists from the current conversation (task specifications, do-not-touch list, patterns to follow)
2. If no plan exists, inform the user they should run `/plan` first or provide the plan context
3. For each task in the current phase: run @coder to implement, then @verifier to validate, then commit
4. Loop through remaining tasks and phases
5. Deliver a complete summary with all changes

## Usage

After running `/plan <request>` and reviewing the plan:

```text
/code
```

Or provide additional context if resuming from a previous session:

```text
/code Continue with the approved plan for <feature description>
```

## Prerequisites

- A plan must have been created and approved (either in this session via `/plan` or provided as context)
- The plan should include: task specifications, do-not-touch list, and patterns to follow
