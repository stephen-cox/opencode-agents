# Common Patterns

## Routing Pattern

All subagent routing uses the @ symbol convention:

- `@explorer` — Route to exploration phase
- `@planner` — Route to planning phase
- `@coder` — Route to coding phase (per atomic task)
- `@verifier` — Route to verification phase (per atomic task)

## Context Passing Pattern

Each phase receives filtered context relevant to its role:

```text
Orchestrator → Explorer:
  - user_request
  - complexity_classification
  - known_affected_areas

Orchestrator → Planner:
  - user_request
  - exploration_report
  - complexity_classification
  - approved_solution_direction (from human gate)

Orchestrator → Coder (per task):
  - task_specification (scope, non-goals, acceptance criteria, definition of done, tests, rollback, risk)
  - task_brief (scope, constraints, files, assumptions, patterns)
  - do_not_touch_list
  - patterns_to_follow

Orchestrator → Verifier (per task):
  - task_specification (acceptance criteria, definition of done, risk level)
  - changes_made
  - manual_test_steps
  - known_issues
```

## Human Gate Pattern

Two mandatory approval points in every EPCV workflow:

```text
Explore → [Present findings + proposed direction] → Human approves → Plan
Plan    → [Present tasks + do-not-touch list]     → Human approves → Code
```

For simple tasks, present concise summaries. For moderate/complex, present full reports.

The user may:

- **Approve** → proceed to next stage
- **Request modifications** → adjust and re-present
- **Reject** → return to Explore or modify approach per user direction

## Iterative Loop Pattern

The workflow runs as nested loops:

```text
For each phase:
  Plan → phase (detail atomic tasks)
  Human approves → plan
  For each task in → phase:
    Code → task
    Verify → task (4 layers)
    Commit → task
  End task loop
End phase loop
Deliver
```

## Retry and Bug-Fixing Loop Escape Pattern

```text
Verify FAIL
  → Coder (fix instructions from Verifier, retry 1)
  → Verify
    FAIL → Coder (retry 2)
    → Verify
      FAIL → Bug-fixing loop escape
             (stop patching, return to Explore for new evidence)
             → Re-plan → Code → Verify
               FAIL → Escalate to user
```

Same-file detection: if the same file has been patched 3+ times for the same
issue, trigger bug-fixing loop escape immediately (don't wait for retry limit).

## Quality Gate Pattern

Every stage transition checks a gate:

```text
Explore ──gate──▶ Human Approval ──gate──▶ Plan ──gate──▶ Human Approval
    ──gate──▶ Code ──gate──▶ Verify ──gate──▶ Commit ──gate──▶ Task Loop
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
Simple:   Quick explore → Concise approval → Brief plan → Concise approval → Code/Verify/Commit
Moderate: Full explore  → Full approval    → Detailed plan → Full approval → Code/Verify/Commit per task
Complex:  Deep explore  → Full approval    → Architecture plan → Full approval → Multi-phase Code/Verify/Commit
```
