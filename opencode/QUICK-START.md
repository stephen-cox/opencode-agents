# EPCV Quick Start Guide

## 5-Minute Overview

The EPCV system ensures every coding task follows a disciplined, iterative workflow:

1. **Explore** — Understand the codebase before changing it
2. **Review** — You review findings and approve the solution direction
3. **Plan** — Break work into atomic tasks with acceptance criteria
4. **Review** — You review the plan and approve before coding begins
5. **Code → Verify → Commit** — Implement, validate, and commit each task
6. **Loop** — Repeat for remaining tasks and phases until complete

You drive the workflow by invoking commands directly. There is no orchestrator —
you stay in control at every step.

## Your First Command

### Full Workflow

```text
/explore Add input validation to the signup form
```

Review the exploration report, then:

```text
/plan Add input validation to the signup form
```

Review the plan, then for each task:

```text
/code Implement task 1 from the approved plan
/verify Check the changes to src/auth/signup.ts
/commit-task 1
```

### Just Explore

```text
/explore How does the routing system work?
```

Get a structured report of the codebase without making any changes.

### Just Plan

```text
/plan Add a caching layer to the API
```

Get an exploration and implementation plan (phases, atomic tasks, do-not-touch list) without writing code.

### Plan Then Code (Two-Step Workflow)

```text
/plan Add a caching layer to the API
```

Review the plan. Once you approve:

```text
/code Implement task 1: Add cache configuration
```

Execute each task individually, verifying and committing after each one.

### Just Verify

```text
/verify Review the changes in src/auth/
```

Get a 4-layer verification (automated, behavioural, operational, security) and quality assessment of existing code.

### Workflow Reference

```text
/epcv Add a new feature
```

Shows the full EPCV workflow sequence and available commands as a quick reference.

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

- **Verification fails**: Re-run `/code` with fix instructions from the verifier (max 2 retries per task)
- **Bug-fixing loop detected**: Re-run `/explore` for new evidence instead of continuing to patch
- **Retries exhausted**: Review the full context and decide how to proceed
- **You reject at a gate**: Adjust direction — modify the plan, re-explore, etc.

## Tips

1. **Be specific** in your requests — the more detail, the better the exploration
2. **Use `/explore` first** if you're unsure about scope
3. **Use `/plan` first** for complex tasks to review the approach before committing to implementation
4. **Run `/code` per task** — implement one atomic task at a time
5. **Review the do-not-touch list** at the plan stage — it prevents unrelated changes
6. **Check acceptance criteria** at the plan stage — they define exactly what "done" means
7. **Trust the process** — exploration prevents most implementation errors
8. **Review warnings** — PASS_WITH_WARNINGS means minor issues were noted but nothing critical
