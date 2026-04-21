# EPCV System — Navigation

## Overview

This is an **Explore → Plan → Code → Verify (EPCV)** workflow system that enforces
a disciplined, iterative approach to every coding task. Understanding precedes action,
validation follows implementation, and a human remains in the loop at every decision point.

Work is broken into **phases** and **atomic tasks**. Each task is coded, verified, and
committed individually. The human drives the workflow by invoking commands directly —
there is no orchestrator agent. Two mandatory human approval gates ensure the developer
controls requirements and approach.

## Quick Start

| Command               | Purpose                                                           |
| --------------------- | ----------------------------------------------------------------- |
| `/epcv <request>`     | Show the EPCV workflow sequence and available commands            |
| `/explore <question>` | Investigate codebase without changes                              |
| `/plan <task>`        | Design solution with atomic task specs                            |
| `/code <brief>`       | Implement an atomic task from an approved plan                    |
| `/verify <code>`      | Review changes with 4-layer verification                          |
| `/commit-task [n]`    | Commit task changes with auto-generated message (task # optional) |

## Workflow Sequence

Run these commands in order, reviewing output at each step:

```text
/explore → review → /plan → review → /code → /verify → /commit-task → task loop → phase loop
```

## System Components

### Agents

| Agent        | File                     | Purpose                                                   |
| ------------ | ------------------------ | --------------------------------------------------------- |
| Explorer     | `agent/explorer.md`      | Codebase investigation (Phase 1)                          |
| Planner      | `agent/planner.md`       | Solution design, atomic task specs, task briefs (Phase 2) |
| Coder        | `agent/coder.md`         | Implementation per atomic task (Phase 3)                  |
| Verifier     | `agent/verifier.md`      | 4-layer verification per atomic task (Phase 4)            |
| GeneralCoder | `agent/general_coder.md` | Runs all four phases inline in a single conversation      |

Read-only Haiku subagents in `agent/subagent/` (context-scout, dependency-mapper, test-scout) can be delegated to by the GeneralCoder for cheap parallel context gathering.

All agents use OpenCode format (YAML frontmatter with `description` and `mode` fields, plain markdown body).

### Skills

Agents are thin shims; the workflow rules, output formats, and hard gates live in skills, loaded on demand:

| Skill                      | Loaded By                      | Purpose                                                       |
| -------------------------- | ------------------------------ | ------------------------------------------------------------- |
| `exploring-ideas`          | Explorer, GeneralCoder         | Phase 1 process, exploration report format                    |
| `writing-plans`            | Planner, GeneralCoder          | Phase 2 process, atomic task spec, task brief format          |
| `implementing-tasks`       | Coder, GeneralCoder            | Phase 3 process, implementation report format                 |
| `verifying-changes`        | Verifier, GeneralCoder         | Phase 4 process, 4-layer verification report, verdict rules   |
| `tracking-work-in-backlog` | Referenced by each phase skill | Backlog persistence for cross-session/specialised-agent flows |

### Commands

| Command        | File                     | Agent    |
| -------------- | ------------------------ | -------- |
| `/epcv`        | `command/epcv.md`        | (none)   |
| `/explore`     | `command/explore.md`     | explorer |
| `/plan`        | `command/plan.md`        | planner  |
| `/code`        | `command/code.md`        | coder    |
| `/verify`      | `command/verify.md`      | verifier |
| `/commit-task` | `command/commit-task.md` | coder    |

All commands use OpenCode format (YAML frontmatter with `description`, optional `agent`/`model`, body uses `$ARGUMENTS`).

## Key Principles

1. **Explore before acting** — Never change what you don't understand
2. **Plan before coding** — Design decisions belong in the plan
3. **Human in the loop** — You drive the workflow; two mandatory approval gates (post-Explore, post-Plan)
4. **Atomic tasks** — Small, independently verifiable, revertible units of work
5. **Follow existing patterns** — Consistency over perfection
6. **Verify everything** — Four layers: automated, behavioural, operational, security
7. **Fail fast** — Surface blockers immediately

## Documentation

- [Architecture Guide](ARCHITECTURE.md) — System design, workflow, component relationships
- [Quick Start Guide](QUICK-START.md) — Get started in 5 minutes
- [Testing Guide](TESTING.md) — Validation checklist (human gates, task loops, 4-layer verification)
