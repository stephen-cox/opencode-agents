---
name: writing-plans
description: "You MUST use this as Phase 2 of any EPCV workflow — after exploration is approved, before any code is written. Turns approved exploration findings into an ordered, atomic, testable implementation plan that a coder can follow without making design decisions."
---

# Writing Plans From Understanding

Turn approved exploration findings into a concrete implementation plan. Design the solution, break it into atomic tasks, sequence them so the tree never breaks, and hand off a brief precise enough that the Coder does not have to invent anything.

> **Hard Gate:** Do NOT write code, run builds, mutate files, or create Backlog tasks for execution until the plan has been presented and approved. Do NOT begin planning until an approved exploration document exists — if one is missing, stop and invoke the `exploring-ideas` skill first.

## Anti-Pattern: "The Plan Is Obvious From Exploration"

Exploration tells you what exists; it does not tell you what to change. Skipping to code because the path "feels clear" is where design decisions get smuggled in without review. A plan can be short when the change really is small, but you MUST present it, get approval, and record it before Coding begins.

## Anti-Pattern: "One Big Task"

A task that touches many files, blends concerns, or cannot be reverted on its own is not a task — it is a phase. Split it. The review cost of a giant task always exceeds the split cost.

## Checklist

Create a task for each item and complete in order:

1. **Confirm inputs** — approved exploration document, complexity classification, any constraints named by the user
2. **Design the solution** — pick an approach that fits existing patterns, justify it against at least one alternative
3. **Define the do-not-touch list** — files, areas, dependency rules the plan will not cross
4. **Break into phases** — only if multi-phase; each phase is a coherent, shippable slice
5. **Specify atomic tasks** — scope, acceptance criteria, definition of done, tests, rollback, risk
6. **Write task briefs** — self-contained work orders a stranger could execute
7. **Sequence within phase** — dependencies first, no broken intermediate states
8. **Present the plan** — in sections, scaled to complexity, pause for feedback after each
9. **Persist the plan** — if cross-session tracking is needed, follow the `tracking-work-in-backlog` skill (Planning section); skip for inline single-agent workflows
10. **Hand off to Coding** — only after persistence (or explicit skip)

**The terminal state is handing off to Coding** (the `coder` agent or `/code` command). Do not invoke `coder`, `verifier`, or implementation skills from here.

## The Process

### Confirming inputs

Before planning, confirm: the approved exploration document exists, the complexity is classified, and any constraints the user named during exploration are still binding. If exploration is missing or stale, stop — planning on top of unverified understanding is how teams ship the wrong thing confidently.

### Designing the solution

Pick the approach that fits the existing patterns, not the approach that would be ideal in a greenfield codebase. Name at least one alternative and say why you rejected it — this is the cheapest defence against sunk-cost bias later. Address each risk the Explorer flagged; if you cannot, surface it as an unknown and stop.

### The do-not-touch list

Before writing tasks, name what the plan _will not_ touch: files, modules, config, dependency rules. This is the guardrail against drive-by refactors and scope creep. "No new dependencies without justification" belongs here. "Do not modify migrations already on main" belongs here. Be explicit; implicit boundaries get crossed.

### Breaking into phases

Use phases only when the work genuinely is multi-stage. Each phase must be a coherent slice that could ship on its own and leave the system in a valid state. Order by dependency, then by risk (lower risk first — you want to learn cheaply). Detail the next phase fully; later phases can stay coarse and be refined when reached.

### Specifying atomic tasks

Atomic means: small enough to review confidently, independently verifiable, revertible without disturbing other tasks. Each task carries:

- **Scope and non-goals** — what is included and, critically, excluded
- **Acceptance criteria** — testable conditions for success
- **Definition of done** — the completion checklist (review, coverage, docs)
- **Automated tests** — specific tests to add or change
- **Manual test steps** — for behaviour that cannot be automated
- **Rollback note** — how to revert, including migrations and config
- **Risk level** — low / medium / high; drives verification rigour

If a task cannot carry all of these, it is not atomic yet. Split it.

### Writing task briefs

The brief is a work order for a stranger. It must stand alone without the conversation that produced it:

- **Scope and non-goals** — what to do, what NOT to do
- **Constraints** — versions, environments, dependencies, deployment
- **Relevant files and commands** — specific paths, build/test commands
- **Assumptions** — explicit notes about API behaviour, permissions, edge cases
- **Patterns to follow** — references to existing code (from exploration)

If a Coder would need to re-run exploration to act on the brief, the brief is incomplete.

### Sequencing within a phase

Order tasks so every intermediate state is valid:

1. Types, interfaces, utilities
2. Core logic
3. Integration and wiring
4. Tests
5. Documentation

Each task produces one self-contained, committable change.

## Presenting the Plan

Scale each section to complexity. Present in sections and pause for feedback:

- **Solution design** — approach, rationale, alternatives considered
- **Architecture decisions** — one row per non-trivial choice
- **Do-not-touch list** — files, areas, dependency rules
- **Phase breakdown** — scope per phase, task counts
- **Task specifications** — the seven fields for each task in the current phase
- **Task briefs** — per-task work orders for the Coder

## Planning Depth by Complexity

- **Simple** — 1 phase, 1–2 tasks. Brief design. Acceptance criteria and DoD per task. Implicit rollback (git revert). Concise briefs.
- **Moderate** — 1–2 phases, multiple tasks. Full design with rationale. All seven fields per task. Explicit do-not-touch list. Explicit rollback per task.
- **Complex** — multiple phases. Comprehensive design with alternatives analysis. ADRs for non-trivial decisions. Strict do-not-touch and dependency guardrails. Migration/data rollback spelled out. Current phase fully detailed; later phases coarse.

## After Approval

- **Persist the plan (if tracking)** — when running as a specialized `planner` agent or in a multi-session workflow, follow the `tracking-work-in-backlog` skill (Planning section) to create tasks, milestones, and plan entries. Skip persistence for inline single-agent workflows and say so explicitly in the hand-off.
- **Hand off** — tell the user planning is complete and recommend invoking the Coder next (`/code` or the `coder` agent). Do not invoke Coding yourself unless the user asks.

## Key Principles

- **Minimal changes** — the best plan makes the fewest changes that meet the requirements
- **Follow existing patterns** — consistency beats theoretical best practice
- **No broken intermediate states** — every committed step must leave the tree valid
- **Explicit over implicit** — spell out what to do; the Coder should not design
- **Testable outcomes** — if you cannot say how to verify it, the plan is not specific enough
- **Atomic or split** — if a task cannot be reviewed, reverted, and tested independently, split it
- **Read-only** — planning describes the change; it does not make the change
- **Respect the do-not-touch list** — the plan defends scope; the Coder cannot add guardrails you forgot
