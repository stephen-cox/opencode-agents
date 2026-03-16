# Common Patterns

## Command Routing Pattern

Each command routes directly to a specialised agent:

- `/explore` → Explorer agent (read-only investigation)
- `/plan` → Planner agent (solution design, atomic task specs)
- `/code` → Coder agent (implementation per atomic task)
- `/verify` → Verifier agent (4-layer verification per atomic task)
- `/commit-epcv` → Coder agent (commit verified changes)

## Context Passing Pattern

The human provides context from prior phases when invoking each command.
Context flows through the conversation:

```text
/explore:
  - user_request
  - complexity_classification

/plan:
  - user_request
  - exploration_report (from prior /explore)
  - complexity_classification
  - approved_solution_direction (human decision)

/code (per task):
  - task_specification (scope, non-goals, acceptance criteria, definition of done, tests, rollback, risk)
  - task_brief (scope, constraints, files, assumptions, patterns)
  - do_not_touch_list
  - patterns_to_follow

/verify (per task):
  - task_specification (acceptance criteria, definition of done, risk level)
  - changes_made
  - manual_test_steps
  - known_issues
```

## Human Gate Pattern

Two mandatory approval points in every EPCV workflow:

```text
/explore → [Review findings + proposed direction] → Human approves → /plan
/plan    → [Review tasks + do-not-touch list]     → Human approves → /code
```

For simple tasks, present concise summaries. For moderate/complex, present full reports.

The user may:

- **Approve** → proceed to next command
- **Request modifications** → adjust and re-present
- **Reject** → re-run `/explore` or modify approach

## Iterative Loop Pattern

The workflow runs as nested loops driven by the human:

```text
For each phase:
  /plan → phase (detail atomic tasks)
  Human approves → plan
  For each task in → phase:
    /code → task
    /verify → task (4 layers)
    /commit-epcv → task
  End task loop
End phase loop
Done
```

## Retry and Bug-Fixing Loop Escape Pattern

```text
/verify FAIL
  → /code (fix instructions from Verifier, retry 1)
  → /verify
    FAIL → /code (retry 2)
    → /verify
      FAIL → Bug-fixing loop escape
             (stop patching, /explore for new evidence)
             → Re-plan → /code → /verify
               FAIL → Escalate (human decides next steps)
```

Same-file detection: if the same file has been patched 3+ times for the same
issue, trigger bug-fixing loop escape immediately (don't wait for retry limit).

## Quality Gate Pattern

Every stage transition checks a gate:

```text
/explore ──gate──▶ Human Approval ──gate──▶ /plan ──gate──▶ Human Approval
    ──gate──▶ /code ──gate──▶ /verify ──gate──▶ /commit-epcv ──gate──▶ Task Loop
```

Gates check specific criteria (see `standards/validation-rules.md`).
Failed gates block the workflow until resolved.

## Atomic Task Pattern

Every unit of work follows the atomic task structure:

```text
Task Specification:
  1. Scope and non-goals
  2. Acceptance criteria (testable conditions)
  3. Definition of done (completion checklist)
  4. Automated tests
  5. Manual test steps
  6. Rollback note
  7. Risk level (low / medium / high)

Task Brief (for Coder):
  - Scope and non-goals
  - Constraints
  - Relevant files and commands
  - Assumptions
  - Patterns to follow
```

## Four-Layer Verification Pattern

Verification applies four layers, scaled by risk:

```text
Layer 1 — Automated:  tests, lint, type check, build
Layer 2 — Behavioural: manual test steps, edge cases, failure paths
Layer 3 — Operational: error handling, logging, config, migrations, rollback
Layer 4 — Security:    input validation, encoding, auth, secrets, hygiene, deps

Risk scaling:
  Low:    Layer 1 full, Layers 2-4 basic
  Medium: All layers standard
  High:   All layers thorough with evidence
```

## Read-Before-Write Pattern

The Coder ALWAYS reads a file before modifying it:

```text
1. Read file (understand current state)
2. Verify file is NOT on the do-not-touch list
3. Identify exact edit location
4. Edit with surgical precision
5. Verify edit was applied correctly
```

## Exploration Search Pattern

Systematic search strategy:

```text
1. Glob for files matching request terms
2. Grep for key functions/classes/variables
3. Read matched files for context
4. Trace imports/exports for dependencies
5. Check for related test files
```

## Plan Ordering Pattern

Tasks within a phase are ordered by dependency:

```text
1. Types / Interfaces / Schemas (foundations)
2. Utilities / Helpers (shared code)
3. Core Logic (main implementation)
4. Integration (wiring, configuration)
5. Tests (verification code)
6. Documentation (if needed)
```

## Complexity Adaptation Pattern

Each phase scales its thoroughness:

```text
Simple:   Quick /explore → Concise review → Brief /plan → Concise review → /code → /verify → /commit-epcv
Moderate: Full /explore  → Full review    → Detailed /plan → Full review → /code → /verify → /commit-epcv per task
Complex:  Deep /explore  → Full review    → Architecture /plan → Full review → Multi-phase /code → /verify → /commit-epcv
```

## Backlog.md Integration Pattern

Each agent documents its work in Backlog.md via MCP tools, creating a persistent
record of decisions, tasks, progress, and outcomes:

```text
Explorer  → document_create    (exploration findings as a Backlog document)
Planner   → task_create        (atomic tasks with acceptance criteria)
          → milestone_add      (phases as milestones, if multi-phase)
          → task_edit planSet   (record task briefs on each task)
Coder     → task_edit status   (mark "In Progress")
          → task_edit notesAppend (implementation decisions, deviations, issues)
Verifier  → task_edit acceptanceCriteriaCheck (mark passing criteria)
          → task_edit finalSummary + status "Done" (on PASS)
          → task_edit notesAppend (failure details on FAIL, leave In Progress)
```

### Key Rules

- **Explorer uses documents, not tasks** — Exploration findings are reference
  material, not commitments. Use `document_create` for the exploration report.
- **Planner creates tasks** — Each atomic task spec becomes a Backlog task.
  Write descriptions as work orders for strangers (include all context).
- **Coder claims and annotates** — Set status to "In Progress" before coding,
  append notes after implementation.
- **Verifier finalises or records failure** — Check acceptance criteria on PASS,
  append fix instructions on FAIL. Never set status to "Done" on FAIL.
- **Search before creating** — Always use `task_search` or `document_search`
  before creating to avoid duplicates.
- **Never edit Backlog markdown files directly** — Always use MCP tools so
  relationships, metadata, and history stay consistent.
