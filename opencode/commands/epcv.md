---
description: Show the EPCV workflow sequence and available commands
---

# EPCV Workflow Reference

The EPCV workflow for your request:

$ARGUMENTS

## Workflow Sequence

Run these commands in order, reviewing output at each step:

1. **Explore**: `/explore <request>` — Investigate the codebase (read-only)
2. **Review** — Read the exploration report, approve the solution direction
3. **Plan**: `/plan <request>` — Design the solution and produce atomic task specs
4. **Review** — Read the plan, approve before coding begins
5. **Code**: `/code <task brief>` — Implement each atomic task
6. **Verify**: `/verify <what changed>` — Validate with 4-layer checks
7. **Commit**: `/commit-task [n]` — Commit verified changes per task (task number optional if exactly one is In Progress)
8. **Loop** — Repeat steps 5-7 for remaining tasks, then repeat steps 3-7 for remaining phases

## Quick Reference

| Command              | Agent    | Skill                | Purpose                                            |
| -------------------- | -------- | -------------------- | -------------------------------------------------- |
| `/explore <request>` | Explorer | `exploring-ideas`    | Build shared understanding of intent and landscape |
| `/plan <request>`    | Planner  | `writing-plans`      | Produce atomic, testable implementation plan       |
| `/code <brief>`      | Coder    | `implementing-tasks` | Implement one atomic task                          |
| `/verify <changes>`  | Verifier | `verifying-changes`  | 4-layer verification, PASS / FAIL verdict          |
| `/commit-task {n}`   | Coder    | —                    | Commit verified changes with task-based message    |

Progress persistence (Backlog docs and tasks) is handled by the `tracking-work-in-backlog` skill, which each phase skill references when cross-session tracking is needed.

## Human Gates

You are the orchestrator. Two approval points:

1. **Post-Explore**: Review findings, approve solution direction before planning
2. **Post-Plan**: Review task specs, approve before coding begins
