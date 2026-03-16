# EPCV Workflow Process

## Standard Workflow Sequence

### 1. Request Intake

- User has a request (feature, bugfix, refactor, exploration)
- User classifies complexity: simple / moderate / complex
- User decides which command to start with

### 2. Exploration Phase

- User runs `/explore` to investigate the codebase
- Explorer searches for relevant files
- Dependencies are mapped
- Existing patterns are documented
- Risks are identified
- **Gate**: Exploration report is complete and comprehensive

### 3. Human Approval: Solution Direction

- User reviews exploration findings and proposed solution direction
- User surfaces open questions and trade-offs
- **Gate**: User approves the solution direction before planning begins

### 4. Planning Phase

- User runs `/plan` with the approved direction
- Planner reviews exploration report and approved direction
- Solution is designed with rationale
- Work is broken into phases (milestones) for moderate/complex tasks
- Each phase is broken into atomic task specifications
- Do-not-touch list and guardrails are defined
- Each task has: scope, non-goals, acceptance criteria, definition of done,
  automated tests, manual test steps, rollback note, risk level
- Task briefs are produced for the Coder
- **Gate**: Plan produces atomic tasks with acceptance criteria

### 5. Human Approval: Implementation Plan

- User reviews the phase breakdown and task specifications
- User reviews do-not-touch list and guardrails
- **Gate**: User approves the plan before coding begins

### 6. Code Phase (per task)

- User runs `/code` with the task brief
- Coder receives a single atomic task specification and task brief
- Coder reads each file before modifying
- Changes are implemented following the task brief
- Do-not-touch list is respected
- Existing patterns are followed precisely
- Deviations are documented with rationale
- **Gate**: Task changes implemented, guardrails respected

### 7. Verify Phase (per task)

- User runs `/verify` to validate the changes
- Verifier checks the task through four layers:
  1. **Automated**: unit tests, integration tests, lint, type check, build
  2. **Behavioural**: manual test steps, edge cases, failure paths
  3. **Operational**: error handling, logging, metrics, config, migrations, rollback
  4. **Security**: input validation, output encoding, authorisation, secrets, logging hygiene, dependency security
- Verification rigour scales with the task's risk level
- Acceptance criteria and definition of done are checked
- **Gate**: PASS / FAIL / PASS_WITH_WARNINGS verdict

### 8. Commit (per task)

- User runs `/commit-epcv` to commit verified changes
- Changes are committed as a logical, self-contained unit
- Commit message references the task scope

### 9. Task Loop

- If there are more tasks in the current phase → return to step 6 (`/code`)
- If no more tasks → proceed to Phase Loop

### 10. Phase Loop

- If there are more phases → return to step 4 (`/plan`) to detail the next phase's tasks
- If no more phases → Done

## Abbreviated Workflow (Simple Tasks)

For simple, single-file changes with clear requirements:

1. Quick `/explore` (targeted file search, 1-level dependency check)
2. Review findings, confirm direction
3. Brief `/plan` (1 phase, 1-2 atomic tasks with acceptance criteria)
4. Review plan, confirm approach
5. `/code` → `/verify` → `/commit-epcv` (per task)

## Extended Workflow (Complex Tasks)

For cross-cutting changes with architectural impact:

1. Deep `/explore` (comprehensive subsystem search, full dependency graph)
2. Full review (consider options and trade-offs)
3. Architecture `/plan` (multiple phases, ADRs, strict do-not-touch list)
4. Full review (phase breakdown and task specs)
5. For each phase:
   - `/plan` to detail task specifications for the phase
   - For each task: `/code` → `/verify` → `/commit-epcv`

## Quality Gates

Each transition requires passing a quality gate:

| Transition                  | Gate Criteria                                                    |
| --------------------------- | ---------------------------------------------------------------- |
| Explore → Approval          | Report complete, files identified, patterns documented           |
| Approval → Plan             | User has approved solution direction                             |
| Plan → Approval             | Atomic tasks with acceptance criteria, do-not-touch list defined |
| Approval → Code             | User has approved implementation plan                            |
| Code → Verify               | Task changes implemented, guardrails respected                   |
| Verify → Commit             | PASS or PASS_WITH_WARNINGS status                                |
| Commit → Next Task          | Changes committed successfully                                   |
| Phase Complete → Next Phase | All tasks in phase verified and committed                        |

## Error Handling

| Scenario                        | Action                                                    |
| ------------------------------- | --------------------------------------------------------- |
| Explorer finds ambiguity        | Flag as open question, user reviews at approval gate      |
| Planner identifies blocker      | Surface to user at plan approval gate                     |
| Coder discovers task spec issue | Document deviation, continue if safe                      |
| Verifier finds critical bug     | FAIL with fix instructions → user re-runs `/code` (max 2) |
| Bug-fixing loop detected        | Stop patching, user re-runs `/explore` for new evidence   |
| 2 retries exhausted             | User reviews full context and decides next steps          |
| User rejects plan               | User re-runs `/explore` or modifies plan                  |
