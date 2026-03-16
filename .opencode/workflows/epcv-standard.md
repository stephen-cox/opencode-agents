# EPCV Standard Workflow

## Overview

The iterative Explore → Plan → Code → Verify workflow. Work is broken into phases
and atomic tasks. Each task is coded, verified, and committed individually. The human
drives the workflow by invoking commands directly. Human approval gates ensure the
developer remains in control of requirements and approach.

## Context Dependencies

- `context/domain/epcv-methodology.md` - Core methodology
- `context/domain/agent-roles.md` - Agent responsibilities
- `context/processes/epcv-workflow-process.md` - Process details
- `context/processes/complexity-classification.md` - Complexity guide
- `context/standards/quality-criteria.md` - Quality standards
- `context/standards/validation-rules.md` - Gate criteria

## Workflow Stages

### Stage 1: Classify

**Actor**: Human
**Action**: Analyse request and determine complexity
**Inputs**: User request
**Outputs**: Complexity classification, workflow strategy
**Success Criteria**: Complexity is one of: simple, moderate, complex

### Stage 2: Explore

**Command**: `/explore`
**Agent**: Explorer
**Action**: Investigate codebase for context
**Inputs**: User request, complexity classification
**Outputs**: Exploration report
**Success Criteria**:

- Files found and listed
- Patterns documented
- Dependencies mapped
- Risks identified
  **Gate**: Exploration report is complete

### Stage 3: Human Approval — Solution Direction

**Actor**: Human
**Action**: Review exploration findings and proposed direction
**Inputs**: Exploration report
**Outputs**: Approval to proceed
**Success Criteria**: User explicitly approves the solution direction
**Gate**: Human approval received

### Stage 4: Plan

**Command**: `/plan`
**Agent**: Planner
**Action**: Break work into phases and atomic task specifications
**Inputs**: User request, exploration report, approved direction, complexity
**Outputs**: Phase breakdown, atomic task specs, task briefs, do-not-touch list
**Success Criteria**:

- Work broken into phases (moderate/complex) or single phase (simple)
- Each task has: scope, non-goals, acceptance criteria, definition of done,
  automated tests, manual test steps, rollback note, risk level
- Task briefs produced for the Coder
- Do-not-touch list and guardrails defined
  **Gate**: Atomic tasks with acceptance criteria produced

### Stage 5: Human Approval — Implementation Plan

**Actor**: Human
**Action**: Review plan
**Inputs**: Phase breakdown, task specifications, do-not-touch list
**Outputs**: Approval to proceed
**Success Criteria**: User explicitly approves the plan
**Gate**: Human approval received

### Stage 6: Code (per task)

**Command**: `/code`
**Agent**: Coder
**Action**: Implement the current atomic task
**Inputs**: Task specification, task brief, do-not-touch list, patterns
**Outputs**: Changed files, implementation report
**Success Criteria**:

- Task changes implemented
- Do-not-touch list respected
- Patterns followed
- Deviations documented
  **Gate**: Task implemented, guardrails respected

### Stage 7: Verify (per task)

**Command**: `/verify`
**Agent**: Verifier
**Action**: Validate task through four verification layers
**Inputs**: Task spec (acceptance criteria, definition of done, risk level), changes
**Outputs**: Verification report with layered results and status
**Success Criteria**:

- Layer 1 (Automated): tests, lint, type check, build pass
- Layer 2 (Behavioural): manual test steps and edge cases pass
- Layer 3 (Operational): error handling, logging, config, rollback verified
- Layer 4 (Security): input validation, encoding, auth, secrets, hygiene checked
- Verification depth matches task risk level
- Acceptance criteria met
- Definition of done complete
  **Gate**: Status is PASS or PASS_WITH_WARNINGS

### Stage 8: Commit (per task)

**Command**: `/commit-epcv`
**Agent**: Coder
**Action**: Commit verified changes as a self-contained unit
**Inputs**: Verified changes for current task
**Outputs**: Git commit
**Success Criteria**: Changes committed with clear message referencing task scope

### Stage 9: Task Loop

**Actor**: Human
**Action**: Check for remaining tasks in current phase
**Decision**:

- More tasks → return to Stage 6 (`/code`) with next task
- No more tasks → proceed to Stage 10 (Phase Loop)

### Stage 10: Phase Loop

**Actor**: Human
**Action**: Check for remaining phases in the plan
**Decision**:

- More phases → return to Stage 4 (`/plan`) to detail next phase's tasks
- No more phases → Done

## Error Handling

- **Exploration fails**: Ask user for clarification at approval gate
- **User rejects direction**: Re-run `/explore` or modify per user input
- **Planning blocked**: Surface blocker to user at plan approval gate
- **User rejects plan**: Modify plan or re-explore per user direction
- **Coding deviation**: Document and continue if safe
- **Verification FAIL**: Re-run `/code` with fix instructions (max 2 per task)
- **Bug-fixing loop**: Stop patching, re-run `/explore` for new evidence
- **Retries exhausted**: User reviews full context and decides next steps

## Estimated Duration

- Simple: 5-15 minutes (1 phase, 1-2 tasks)
- Moderate: 15-45 minutes (1-2 phases, multiple tasks)
- Complex: 45-90+ minutes (multiple phases, multiple tasks)
