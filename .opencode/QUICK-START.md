# EPCV Quick Start Guide

## 5-Minute Overview

The EPCV system ensures every coding task follows a disciplined, iterative workflow:

1. **Explore** — Understand the codebase before changing it
2. **Human Approval** — You review findings and approve the solution direction
3. **Plan** — Break work into atomic tasks with acceptance criteria
4. **Human Approval** — You review the plan and approve before coding begins
5. **Code → Verify → Commit** — Implement, validate, and commit each task
6. **Loop** — Repeat for remaining tasks and phases until complete

You stay in control at two mandatory approval gates. The assistant accelerates the process but does not replace your judgement.

## Your First Command

### Full Workflow

```text
/epcv Add input validation to the signup form
```

This will:

1. Search the codebase for the signup form and related files
2. Present findings and proposed approach — **you approve the direction**
3. Create atomic task specifications with acceptance criteria
4. Present the plan — **you approve before coding starts**
5. Implement each task, verify through 4 layers, and commit
6. Deliver a complete summary with all changes

### Just Explore

```text
/explore How does the routing system work?
```

Get a structured report of the codebase without making any changes. No approval gates needed.

### Just Plan

```text
/plan Add a caching layer to the API
```

Get an exploration report and implementation plan (phases, atomic tasks, do-not-touch list) without writing code.

### Plan Then Code (Two-Step Workflow)

```text
/plan Add a caching layer to the API
```

Review the exploration and plan. Once you approve:

```text
/code
```

Execute the Code → Verify → Commit loop for the approved plan. This two-step workflow lets you review the plan thoroughly before any code is written, then proceed to implementation without re-running exploration.

### Just Verify

```text
/verify Review the changes in src/auth/
```

Get a 4-layer verification (automated, behavioural, operational, security) and quality assessment of existing code.

## What to Expect

### For a Simple Task (single file, clear requirements)

- **Time**: 5-15 minutes
- **Structure**: 1 phase, 1-2 atomic tasks
- **Approvals**: Concise summaries at both gates
- **Output**: Changes + brief summary

### For a Moderate Task (multiple files, some complexity)

- **Time**: 15-45 minutes
- **Structure**: 1-2 phases, multiple atomic tasks per phase
- **Approvals**: Full reports at both gates
- **Output**: Changes + detailed summary with all phase reports

### For a Complex Task (cross-cutting, architectural)

- **Time**: 45-90+ minutes
- **Structure**: Multiple phases, multiple atomic tasks per phase
- **Approvals**: Full reports with architecture decisions at both gates
- **Output**: Changes + comprehensive summary with architecture decisions

## What Happens on Failure

- **Verification fails**: The Coder gets specific fix instructions and retries (max 2 per task)
- **Bug-fixing loop detected**: Workflow returns to Explore for new evidence instead of continuing to patch
- **Retries exhausted**: You're asked for guidance with full context
- **You reject at a gate**: The workflow adjusts per your direction (modify plan, re-explore, etc.)

## Tips

1. **Be specific** in your requests — the more detail, the better the exploration
2. **Use `/explore` first** if you're unsure about scope
3. **Use `/plan` first** for complex tasks to review the approach before committing to implementation
4. **Use `/code` after `/plan`** to execute the approved plan without re-running exploration
5. **Review the do-not-touch list** at the plan approval gate — it prevents unrelated changes
6. **Check acceptance criteria** at the plan approval gate — they define exactly what "done" means
7. **Trust the process** — exploration prevents most implementation errors
8. **Review warnings** — PASS_WITH_WARNINGS means minor issues were noted but nothing critical
