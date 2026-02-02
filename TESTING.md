# EPCV Testing Guide

## Component Testing Checklist

### Orchestrator
- [ ] Correctly classifies a simple request (single file, clear requirements)
- [ ] Correctly classifies a moderate request (multiple files, dependencies)
- [ ] Correctly classifies a complex request (cross-cutting, architectural)
- [ ] Routes to @explorer first for every request
- [ ] Passes appropriate filtered context to each subagent
- [ ] Enforces quality gates between all 11 stages
- [ ] Presents exploration findings at Human Gate #1 (post-Explore)
- [ ] Waits for explicit user approval at Human Gate #1
- [ ] Presents plan at Human Gate #2 (post-Plan)
- [ ] Waits for explicit user approval at Human Gate #2
- [ ] Handles user rejection at Human Gate #1 (re-explore or modify direction)
- [ ] Handles user rejection at Human Gate #2 (modify plan or re-explore)
- [ ] Manages the task loop (advances to next task after commit)
- [ ] Manages the phase loop (returns to Plan for next phase)
- [ ] Commits verified changes per task with clear message
- [ ] Handles PASS verdict correctly (commits and advances)
- [ ] Handles PASS_WITH_WARNINGS correctly (commits with warnings noted)
- [ ] Handles FAIL verdict correctly (retries with Coder, max 2 per task)
- [ ] Detects bug-fixing loop (same file patched 3+ times for same issue)
- [ ] Triggers bug-fixing loop escape (returns to Explore for new evidence)
- [ ] Escalates after bug-fixing loop escape also fails

### Explorer
- [ ] Finds relevant files using glob patterns
- [ ] Finds relevant code using grep searches
- [ ] Reads and analyses file contents
- [ ] Maps dependencies between files
- [ ] Identifies existing coding patterns
- [ ] Flags risks and concerns
- [ ] Flags open questions for the human approval gate
- [ ] Produces structured exploration report
- [ ] Adjusts thoroughness by complexity level
- [ ] Uses only read-only tools (read, glob, grep — no write, edit, bash)

### Planner
- [ ] Synthesises exploration report into solution design
- [ ] Considers alternative approaches
- [ ] Breaks work into phases for moderate/complex tasks
- [ ] Produces atomic task specifications with all 7 fields:
  - [ ] Scope and non-goals
  - [ ] Acceptance criteria (testable conditions)
  - [ ] Definition of done (completion checklist)
  - [ ] Automated tests
  - [ ] Manual test steps
  - [ ] Rollback note
  - [ ] Risk level
- [ ] Produces task briefs for the Coder (scope, constraints, files, assumptions, patterns)
- [ ] Defines do-not-touch list and dependency guardrails
- [ ] Orders tasks by dependency within each phase
- [ ] Scales planning depth by complexity (simple: concise, moderate: full, complex: comprehensive)
- [ ] Each task is independently verifiable and produces a committable change
- [ ] Uses only read-only tools (read, glob, grep — no write, edit, bash)

### Coder
- [ ] Reviews task brief before writing code
- [ ] Reviews task specification (acceptance criteria, definition of done)
- [ ] Reads every file before modifying it
- [ ] Verifies files are NOT on the do-not-touch list before editing
- [ ] Follows implementation plan step order
- [ ] Uses Edit tool for modifications (not Write for existing files)
- [ ] Matches existing code patterns
- [ ] Checks guardrails (no unrelated changes, no new deps without justification)
- [ ] Documents any deviations from task spec
- [ ] Reports acceptance criteria status in implementation report
- [ ] Detects bug-fixing loop (same file edited 3+ times for same issue)
- [ ] Leaves no incomplete implementations

### Verifier
- [ ] Reviews every changed file against the task specification
- [ ] Applies Layer 1 — Automated checks (tests, lint, type check, build)
- [ ] Applies Layer 2 — Behavioural checks (manual test steps, edge cases, failure paths)
- [ ] Applies Layer 3 — Operational checks (error handling, logging, config, migrations, rollback)
- [ ] Applies Layer 4 — Security checks (input validation, encoding, auth, secrets, hygiene, deps)
- [ ] Scales verification depth by risk level:
  - [ ] Low risk: Layer 1 full, Layers 2-4 basic
  - [ ] Medium risk: all layers standard
  - [ ] High risk: all layers thorough with evidence
- [ ] Checks each acceptance criterion (pass/fail with evidence)
- [ ] Checks each definition of done item (complete/incomplete)
- [ ] Produces clear PASS / FAIL / PASS_WITH_WARNINGS verdict
- [ ] Provides specific, actionable fix instructions on FAIL
- [ ] Uses only bash + read tools (no write/edit)

## Integration Testing

### Full EPCV Workflow
- [ ] Simple task completes all 11 stages successfully
- [ ] Moderate task completes all 11 stages with multiple tasks
- [ ] Complex task completes all 11 stages with multiple phases
- [ ] Context flows correctly between phases (filtered per agent)
- [ ] Quality gates catch issues between stages
- [ ] Human Gate #1 pauses workflow and waits for approval
- [ ] Human Gate #2 pauses workflow and waits for approval
- [ ] Each task produces a self-contained commit
- [ ] Task loop correctly advances through tasks in a phase
- [ ] Phase loop correctly returns to Plan for next phase

### Retry and Bug-Fixing Loop Flow
- [ ] Verification FAIL triggers retry to Coder with fix instructions
- [ ] Coder receives specific fix instructions from Verifier
- [ ] Re-verification runs after fix
- [ ] Second retry works if first fix is insufficient
- [ ] Bug-fixing loop escape triggers after 2 retries exhausted
- [ ] Bug-fixing loop escape triggers if same file patched 3+ times
- [ ] Escape returns to Explore for new evidence
- [ ] Escalation occurs if escape also fails

### Human Gate Flows
- [ ] User approves at Gate #1 → workflow proceeds to Plan
- [ ] User rejects at Gate #1 → workflow re-explores or modifies direction
- [ ] User approves at Gate #2 → workflow proceeds to Code
- [ ] User rejects at Gate #2 → workflow modifies plan or re-explores
- [ ] Simple tasks get concise approval summaries
- [ ] Complex tasks get full reports at approval gates

### Partial Workflows
- [ ] `/explore` runs exploration only and delivers report (no approval gates)
- [ ] `/plan` runs exploration + planning and delivers both (with approval gates)
- [ ] `/verify` runs 4-layer verification on existing code (no approval gates)

## Atomic Task Scenarios
- [ ] Task spec with all 7 fields is produced and consumed correctly
- [ ] Task brief is produced and consumed correctly
- [ ] Acceptance criteria are checked by Verifier (pass/fail per criterion)
- [ ] Definition of done is checked by Verifier (complete/incomplete per item)
- [ ] Do-not-touch list is respected by Coder
- [ ] Rollback note is verified by Verifier
- [ ] Risk level determines verification depth

## Edge Case Scenarios
- [ ] Request with no matching files in codebase
- [ ] Request that requires creating entirely new files
- [ ] Request that conflicts with existing architecture
- [ ] Request with ambiguous requirements (open questions flagged)
- [ ] Request that touches security-sensitive code (high risk verification)
- [ ] Request that requires changes to test files
- [ ] Very large codebase with many matching files
- [ ] Request that the Planner determines is infeasible
- [ ] Multi-phase project with phase loop
- [ ] Task that fails verification and triggers bug-fixing loop escape
- [ ] User rejects at both approval gates in sequence

## Validation Procedure

1. Start with a simple, well-defined task
2. Verify each stage produces expected output format
3. Verify Human Gate #1 pauses and presents findings correctly
4. Verify Human Gate #2 pauses and presents plan correctly
5. Check that context passes correctly between phases (filtered)
6. Verify atomic task specs have all 7 fields
7. Verify 4-layer verification report is produced
8. Verify commit is created per task
9. Try a moderate task and verify task loop with multiple tasks
10. Try a complex task and verify phase loop
11. Intentionally create a verification failure to test retry flow
12. Exhaust retries to test bug-fixing loop escape
13. Test each slash command independently
14. Review all output formats match templates in `context/templates/output-formats.md`
