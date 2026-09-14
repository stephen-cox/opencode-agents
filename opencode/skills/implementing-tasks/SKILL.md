---
name: implementing-tasks
description: "You MUST use this as Phase 3 of any EPCV workflow — when executing an approved atomic task against the codebase. Implements exactly one atomic task at a time, following existing patterns, respecting guardrails, documenting deviations, and producing an implementation report ready for verification."
---

# Implementing Atomic Tasks

Execute one approved atomic task precisely. Match existing patterns, respect the do-not-touch list, document every deviation, and produce a report the Verifier can check against acceptance criteria. You do not design, you do not re-plan, you do not commit.

> **Hard Gate:** Do NOT begin implementation without an approved task specification and task brief from Planning. Do NOT commit, push, or mark tasks done — those are separate phases. Do NOT modify files on the do-not-touch list. Do NOT introduce refactors, renames, or dependencies the plan did not authorise.

## Anti-Pattern: "While I'm In Here..."

Adjacent code that looks wrong, unused imports, inconsistent spacing, a better name — leave them alone. Every drive-by change inflates the review surface, obscures the actual diff, and risks breaking something the plan did not account for. If the improvement matters, surface it as a follow-up, not a silent edit.

## Anti-Pattern: "I'll Just Patch It One More Time"

If you have edited the same file 3+ times chasing the same failure, stop. The evidence is telling you the plan is wrong or exploration missed something. Flag a bug-fixing-loop escape and return to Explore — more patches will not produce new information.

## Anti-Pattern: "Edit Without Read"

Editing a file you have not read in this session is how invariants get broken. The Edit tool will error, but even when Write would succeed, you will miss the context that makes the change safe. Always read first.

## Checklist

Create a task for each item and complete in order:

1. **Claim the task (if tracking)** — follow the `tracking-work-in-backlog` skill (Coding section, "At the start") to mark the task In Progress and load its record; skip for inline single-agent workflows
2. **Review the brief** — scope, non-goals, constraints, files, commands, assumptions, patterns
3. **Review the spec** — acceptance criteria, definition of done, tests, risk level
4. **Read before write** — read every file you will modify; verify none are on the do-not-touch list
5. **Implement in dependency order** — types/interfaces → core logic → integration → tests → docs
6. **Match patterns** — naming, error handling, imports, formatting, comment style
7. **Check guardrails** — do-not-touch respected, no unrelated changes, no unauthorised dependencies
8. **Document deviations** — what changed, why, downstream impact; never silently
9. **Produce the implementation report** — file-by-file changes, criterion status, guardrail compliance
10. **Record progress (if tracking)** — follow the `tracking-work-in-backlog` skill (Coding section, "At the end") to append notes and update the plan on deviation; do NOT mark done, do NOT commit

**The terminal state is handing off to Verification** (the `verifier` agent or `/verify` command). You do not mark tasks done, update acceptance criteria, or commit — those belong downstream.

## The Process

### Claiming the task

If cross-session tracking is in play, follow the `tracking-work-in-backlog` skill (Coding section, "At the start") to locate the task, mark it In Progress, and load the full record. The task's description, plan, acceptance criteria, and references become your source of truth — not the conversation that led up to this point. If they are missing or contradict the conversation, stop and ask.

For inline single-agent workflows, skip this step — the conversation itself carries the spec.

### Reading before writing

For every file you will modify: read it. Confirm it is not on the do-not-touch list. Study the surrounding code, the naming conventions, the error-handling idiom, the import style. Editing blind is the single most common source of broken changes.

### Implementing

Work in dependency order so every intermediate state is valid:

1. Types, interfaces, utilities
2. Core logic
3. Integration and wiring
4. Tests
5. Documentation

Prefer Edit over Write for existing files — surgical edits preserve context and shrink the review surface. Use Write only for new files. Complete each change fully before moving to the next; no placeholders, no TODO comments unless the plan specifies them.

### Matching patterns

Your code should be indistinguishable from what is already in the file. Tabs if the file uses tabs. Semicolons if the file uses semicolons. The project's error-handling idiom, not yours. The project's naming conventions, not the ones you would choose. Consistency beats personal preference every time.

### Checking guardrails

Before producing the report, sweep for:

- Any file modified that was on the do-not-touch list
- Any refactor, rename, or style change outside the task's stated scope
- Any new dependency added without plan authorisation
- Any acceptance criterion the plan covers that the diff does not address

If you find a violation, revert it before producing the report.

### Documenting deviations

If the task spec cannot be followed exactly — a missing interface, a wrong assumption, a dependency that does not behave as documented — deviate only as much as needed, and record:

- What changed relative to the spec
- Why (the evidence that forced the change)
- Downstream impact (other tasks, tests, docs that may now need adjustment)

Silent deviations are how plans become fiction. Never deviate without a note.

## Implementation Report

Produce the report after all changes are complete. Reference acceptance criteria directly.

```text
## Implementation Report — Task: {task title}

### Changes Made
| # | File | Action | Description |
|---|------|--------|-------------|
| 1 | `{path}` | {created/modified/deleted} | {what was done} |

### Acceptance Criteria Status
- [ ] {criterion 1}: {implemented / not yet verifiable / blocked}

### Guardrail Compliance
- **Do-not-touch list respected**: {yes/no — details if no}
- **No unrelated changes**: {yes/no}
- **No new dependencies**: {yes/no — justification if added}

### Task Spec Adherence
- **Deviations**: {none / list of deviations with rationale}

### Implementation Notes
- {important observations during implementation}

### Known Issues
- {issues discovered but not fixed}

### Test Readiness
- Code is ready for verification: {yes/no}
- {prerequisites for testing}
```

## After the Report

- **Record progress (if tracking)** — follow the `tracking-work-in-backlog` skill (Coding section, "At the end") to append implementation notes and update the plan on deviation. Skip for inline single-agent workflows and say so explicitly.
- **Do NOT** update acceptance criteria (Verifier territory), mark the task done, or commit anything
- **Hand off** — tell the user the implementation is ready and recommend invoking the Verifier next (`/verify` or the `verifier` agent)

## Bug-Fixing Loop Escape

If the same file is edited 3+ times against the same failure, or a task has been retried 2+ times, stop patching. More patches without new information produce more wrong code, not less. Escalate: return to Explore with the failure evidence, let new context reshape the plan, then resume.

## Key Principles

- **Plan is law** — the task spec is authoritative; disagree in writing, implement as specified unless it would cause a clear defect
- **Read before write** — never modify a file you have not read in this session
- **Surgical precision** — minimum changes that meet the criteria; no adjacent improvements
- **Pattern consistency** — match existing style exactly, even when you would choose differently
- **Complete implementations** — no placeholders, no TODOs unless the plan authorised them
- **Transparency** — document every deviation, every known issue, every guardrail decision
- **One task at a time** — this skill executes a single atomic task; do not bleed into the next
- **Not your job** — committing, marking done, updating acceptance criteria are downstream phases
