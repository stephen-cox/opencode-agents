---
name: tracking-work-in-backlog
description: "Use this whenever an EPCV phase needs to persist its output to Backlog — exploration findings, implementation plans, task progress, or verification verdicts. Defines the exact Backlog operations each phase performs so progress survives outside the current conversation. Skip this skill when running a single-agent inline workflow that does not need cross-session tracking."
---

# Tracking EPCV Work In Backlog

Persist each EPCV phase's output to Backlog so work survives the conversation that produced it. Each phase has a specific pattern: Exploration writes a document, Planning creates tasks and milestones, Coding updates progress, Verification records the verdict. Follow the section for the phase you are in.

> **Hard Gate:** Do NOT mutate Backlog beyond the operations described for your current phase. The Coder never marks tasks Done. The Verifier never creates new tasks. Cross-phase mutations break the workflow's audit trail.

## When To Use — And When To Skip

- **Use** when a specialized EPCV agent (`explorer`, `planner`, `coder`, `verifier`) completes its phase. Backlog is the hand-off surface between agents.
- **Use** when work spans multiple sessions and needs to be picked back up later.
- **Skip** when a single-agent inline workflow (e.g. `general_coder`) runs all phases in one conversation without pausing. In that case the conversation itself is the audit trail — avoid the overhead.
- **Skip** when the user explicitly opts out ("just do it, don't bother tracking").

## Phase: Exploration

Run after presenting findings and getting user approval.

1. **Search first** — `document_search` for an existing exploration document on this topic. If one exists, update it rather than creating a duplicate.
2. **Create the document** — `document_create` with:
   - **Title**: `Exploration: <concise topic>`
   - **Content**: the full approved exploration report (intent, constraints, landscape, risks, unknowns, summary)
3. **Report the document ID** — include it in the hand-off so the Planner can cite it as a reference.

## Phase: Planning

Run after presenting the plan and getting user approval.

1. **Search first** — `task_search` to avoid duplicating existing tasks for this work.
2. **Create a parent task** (if multi-task) — `task_create` for the overall feature/change. Put the solution-design summary in the description.
3. **Create subtasks** — one per atomic task, via `task_create`, with:
   - **Title**: the atomic task title
   - **Description**: scope, non-goals, and brief context — written as a work order for a stranger
   - **Acceptance criteria**: the testable conditions from the task spec
   - **Priority**: mapped from risk level (high risk → high priority)
   - **Parent task ID**: link to the parent if one exists
   - **Dependencies**: reference any tasks that must complete first
   - **References**: the exploration document ID
4. **Create milestones for phases** (if multi-phase) — `milestone_add` per phase, then attach to each task via `task_edit`.
5. **Attach the plan** — `task_edit` with `planSet` on each task to record the full task brief (scope, constraints, files, assumptions, patterns).
6. **Report task IDs** — include them in the hand-off so Coder and Verifier can cite them.

## Phase: Coding

Run at the start and end of implementing one atomic task.

**At the start:**

1. **Find the task** — `task_search` or `task_list` to locate the Backlog task (Planner should have provided the ID).
2. **Mark In Progress** — `task_edit` with status "In Progress".
3. **Review the record** — `task_view` to read description, acceptance criteria, plan, references. This is your source of truth, not the conversation.

**At the end, after the implementation report:**

1. **Append implementation notes** — `task_edit` with `notesAppend` to record:
   - Files created, modified, deleted
   - Key implementation decisions and rationale
   - Deviations from the task spec (with explanation)
   - Known issues discovered
   - Blockers encountered and how resolved
2. **Update the plan if you deviated** — `task_edit` with `planAppend` to record what changed and why.

**Do NOT:**

- Check acceptance criteria — that is the Verifier's job
- Mark the task Done — that is the Verifier's job on PASS
- Commit any changes — commit is a separate phase

## Phase: Verification

Run after producing the verification report.

1. **Locate the task** — `task_search` or `task_list`. It should be In Progress, left by the Coder.

**On PASS or PASS_WITH_WARNINGS:**

1. **Check acceptance criteria** — `task_edit` with `acceptanceCriteriaCheck`, marking each passing criterion by its 1-based index.
2. **Check definition-of-done items** — `task_edit` with `definitionOfDoneCheck` for each completed item.
3. **Write the final summary** — `task_edit` with `finalSummary`: a PR-style summary capturing what changed, verification results, warnings (if any), and follow-up recommendations.
4. **Set status to Done** — `task_edit` with status "Done".

**On FAIL:**

1. **Uncheck failing criteria** — `task_edit` with `acceptanceCriteriaUncheck` for any criteria previously checked but now failing.
2. **Append failure details** — `task_edit` with `notesAppend` recording:
   - Which verification layers failed and why
   - Specific fix instructions for the Coder
   - Which acceptance criteria are not met (with evidence)
3. **Leave status as In Progress** — the Coder retries from there with the fix instructions in context.

## Key Principles

- **Phase-scoped writes** — only the Coder touches progress, only the Verifier touches status and criteria, only the Planner creates tasks, only the Explorer creates exploration documents
- **Search before create** — `document_search` and `task_search` first, every time, to avoid duplicating work
- **Stranger-readable** — anything you write (descriptions, notes, summaries) should stand alone without the conversation that produced it
- **Reference across phases** — Planning cites the exploration doc, Coding cites the task, Verification cites both; the chain is the audit trail
- **No silent skips** — if you choose to skip Backlog (per the "When To Skip" rules), say so explicitly in the hand-off so the next phase knows why
