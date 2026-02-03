# Quality Criteria

## Code Quality Standards

### Correctness

- Code does exactly what the acceptance criteria specify
- No unintended side effects
- Edge cases are handled
- Error conditions produce meaningful responses

### Pattern Adherence

- Matches existing codebase conventions
- Uses the same naming conventions (camelCase, snake_case, etc.)
- Follows the same file organisation patterns
- Uses the same import/export style
- Matches indentation and formatting

### Readability

- Code is self-documenting where possible
- Complex logic has explanatory comments
- Function/variable names clearly express intent
- No unnecessary complexity or cleverness

### Maintainability

- Changes are isolated and modular
- No tight coupling introduced
- Dependencies are explicit, not implicit
- Future developers can understand the change

### Acceptance Criteria Compliance

- Every acceptance criterion from the task spec is met
- Evidence exists for each criterion (test result, manual check, code review)
- No criterion is skipped or marked as "not applicable" without justification

### Definition of Done Compliance

- Every item in the definition of done checklist is complete
- Code reviewed, tests pass, documentation updated (as specified)
- No items left incomplete without documented reason

## Exploration Quality

- All relevant files identified
- Dependencies mapped at appropriate depth
- Existing patterns clearly documented
- Risks identified with severity levels
- Open questions flagged for the human approval gate
- No major blind spots

## Plan Quality

- Work broken into atomic tasks (small, independently verifiable, revertible)
- Each task has all 7 specification fields (scope, non-goals, acceptance criteria, definition of done, automated tests, manual test steps, rollback note, risk level)
- Task briefs produced for the Coder (scope, constraints, files, assumptions, patterns)
- Do-not-touch list and dependency guardrails defined
- Tasks ordered by dependency (foundations → core → integration → tests → docs)
- Each task produces a self-contained, committable change
- Planning depth matches complexity (simple: concise, moderate: full, complex: comprehensive)

## Verification Quality

### Layer 1: Automated

- All automated checks run (tests, lint, type check, build)
- No regressions introduced
- Test coverage of new/changed code

### Layer 2: Behavioural

- Manual test steps from task spec executed
- Edge cases and failure paths validated
- User-facing behaviour confirmed correct

### Layer 3: Operational

- Error handling reviewed
- Logging at appropriate levels
- Configuration changes documented
- Rollback procedure verified

### Layer 4: Security

- Input validation and output encoding checked
- Authorisation controls verified
- Secrets not hardcoded or logged
- Dependency security assessed

### Verification Depth

- Verification rigour matches the task's risk level
- Low risk: automated full + behavioural basic + operational minimal + security basic
- Medium risk: all layers at standard depth
- High risk: all layers thorough with detailed evidence

## Minimum Scores for Delivery

| Dimension              | Minimum                    | Target                   |
|------------------------|----------------------------|--------------------------|
| ---------------------- | -------------------------- | ------------------------ |
| ---------------------  | ------------------------   | ----------------------   |
| Correctness            | Must pass                  | Must pass                |
| Pattern Adherence      | 8/10                       | 9/10                     |
| Acceptance Criteria    | 100% pass                  | 100% pass                |
| Definition of Done     | 100% complete              | 100% complete            |
| Test Coverage          | Critical paths covered     | All paths covered        |
| Build Status           | Must pass                  | Must pass                |
| Security Checks        | No critical issues         | No issues                |
