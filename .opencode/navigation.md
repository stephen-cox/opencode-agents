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
| `/commit-epcv {n}`    | Commit task changes with auto-generated message (task # optional) |

## Workflow Sequence

Run these commands in order, reviewing output at each step:

```text
/explore → review → /plan → review → /code → /verify → /commit-epcv → task loop → phase loop
```

## System Components

### Agents

| Agent    | File                | Purpose                                                   |
| -------- | ------------------- | --------------------------------------------------------- |
| Explorer | `agent/explorer.md` | Codebase investigation (Phase 1)                          |
| Planner  | `agent/planner.md`  | Solution design, atomic task specs, task briefs (Phase 2) |
| Coder    | `agent/coder.md`    | Implementation per atomic task (Phase 3)                  |
| Verifier | `agent/verifier.md` | 4-layer verification per atomic task (Phase 4)            |

All agents use OpenCode format (YAML frontmatter with `description` and `mode` fields, plain markdown body).

### Workflows

| Workflow        | File                           | Purpose                                        |
| --------------- | ------------------------------ | ---------------------------------------------- |
| EPCV Standard   | `workflows/epcv-standard.md`   | Full iterative workflow with human gates       |
| Explore Only    | `workflows/explore-only.md`    | Investigation without changes                  |
| Verify Existing | `workflows/verify-existing.md` | Review existing code with 4-layer verification |

### Context

| Category  | Directory            | Contents                                                                                            |
| --------- | -------------------- | --------------------------------------------------------------------------------------------------- |
| Domain    | `context/domain/`    | EPCV methodology (iterative workflow, atomic tasks, human gates), agent roles                       |
| Processes | `context/processes/` | Workflow process (stages), complexity classification                                                |
| Standards | `context/standards/` | Quality criteria, validation rules (with human gates), error handling (with bug-fixing loop escape) |
| Templates | `context/templates/` | Output formats (atomic task spec, 4-layer verification report), common patterns                     |

### Commands

| Command        | File                     | Agent    |
| -------------- | ------------------------ | -------- |
| `/epcv`        | `command/epcv.md`        | (none)   |
| `/explore`     | `command/explore.md`     | explorer |
| `/plan`        | `command/plan.md`        | planner  |
| `/code`        | `command/code.md`        | coder    |
| `/commit-epcv` | `command/commit-epcv.md` | coder    |
| `/verify`      | `command/verify.md`      | verifier |

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
- [Context Guide](context/navigation.md) — Context file organisation
- [Workflow Guide](workflows/navigation.md) — Workflow selection
