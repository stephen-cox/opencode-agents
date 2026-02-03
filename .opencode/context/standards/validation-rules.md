# Validation Rules

## Phase Transition Gates

### Stage 2 → Stage 3: Explore → Human Approval (Solution Direction)

**Must pass ALL**:

- [ ] Exploration report has a "Files Found" section with at least 1 file
- [ ] Existing patterns are documented
- [ ] Dependency map is present (even if simple)
- [ ] Risks section exists (even if "none identified")
- [ ] Context summary is present for the Planner

**Should pass**:

- [ ] Open questions are flagged (if any exist)
- [ ] Thoroughness matches complexity level

### Stage 3: Human Approval — Solution Direction

**Must pass ALL**:

- [ ] Exploration findings presented to user
- [ ] Proposed solution direction and trade-offs presented
- [ ] Open questions surfaced for user input
- [ ] User has explicitly approved the solution direction

### Stage 4 → Stage 5: Plan → Human Approval (Implementation Plan)

**Must pass ALL**:

- [ ] Work broken into atomic tasks
- [ ] Each task has all 7 specification fields:
  - Scope and non-goals
  - Acceptance criteria (testable conditions)
  - Definition of done (completion checklist)
  - Automated tests
  - Manual test steps
  - Rollback note
  - Risk level
- [ ] Task briefs produced for the Coder
- [ ] Do-not-touch list defined

**Should pass**:

- [ ] Phases defined for moderate/complex work
- [ ] Architecture decisions documented (complex)
- [ ] Dependency guardrails specified
- [ ] Tasks ordered by dependency

### Stage 5: Human Approval — Implementation Plan

**Must pass ALL**:

- [ ] Phase breakdown presented (if multiple phases)
- [ ] Atomic task specifications presented
- [ ] Do-not-touch list and guardrails presented
- [ ] User has explicitly approved the plan

### Stage 6 → Stage 7: Code → Verify

**Must pass ALL**:

- [ ] All planned changes for the task are implemented
- [ ] Every file was read before being modified
- [ ] Do-not-touch list was respected
- [ ] Implementation report lists all changes
- [ ] Acceptance criteria status is reported
- [ ] Deviations (if any) are documented with rationale

**Should pass**:

- [ ] No unplanned changes were made
- [ ] Existing patterns were followed
- [ ] No new dependencies added without justification

### Stage 7 → Stage 8: Verify → Commit

**Must pass ALL**:

- [ ] Verification status is PASS or PASS_WITH_WARNINGS
- [ ] All acceptance criteria pass
- [ ] Definition of done is complete
- [ ] No critical issues remain
- [ ] All four verification layers checked (depth scaled by risk level)

**Should pass**:

- [ ] No warnings remain
- [ ] All tests pass
- [ ] All security checks pass

### Stage 8 → Stage 9: Commit → Task Loop

**Must pass ALL**:

- [ ] Changes committed as a self-contained unit
- [ ] Commit message references the task scope
- [ ] Commit succeeded without errors

### Stage 9: Task Loop Decision

- More tasks in current phase → return to Stage 6 (Code) with next task
- No more tasks → proceed to Stage 10 (Phase Loop)

### Stage 10: Phase Loop Decision

- More phases → return to Stage 4 (Plan) to detail next phase's tasks
- No more phases → proceed to Stage 11 (Deliver)

## Retry Rules

| Condition                                                  | Action                                                                |
| ---------------------------------------------------------- | --------------------------------------------------------------------- |
| ---------------------------------------------------------- | --------------------------------------------------------------------- |
| ----------------------------------------------------       | -------------------------------------------------------------------   |
| Verification FAIL (retry 1)                                | Route to Coder with specific fix instructions from Verifier           |
| Verification FAIL (retry 2)                                | Route to Coder with specific fix instructions from Verifier           |
| Verification FAIL (retry 3 or same file patched 3+ times)  | Bug-fixing loop escape: return to Explore for new evidence            |
| Bug-fixing loop escape also fails                          | Escalate to user with full context                                    |
| Verification PASS_WITH_WARNINGS                            | Proceed to Commit with warnings noted                                 |
| Any phase produces open questions                          | Surface at the next human approval gate                               |

## Escalation Triggers

Immediately escalate to the user when:

- Requirements are ambiguous and cannot be inferred
- A breaking change is unavoidable
- Security vulnerability is discovered
- The requested change conflicts with existing architecture
- Bug-fixing loop escape is triggered (return to Explore first, then escalate if that also fails)
- User rejects the solution direction or implementation plan
