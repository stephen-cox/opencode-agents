# Output Format Templates

## Exploration Report Template

```markdown
## Exploration Report

### Request Understanding

- **Intent**: {what the user wants}
- **Type**: feature / bugfix / refactor / exploration
- **Scope**: {in scope} | Out of scope: {out of scope}

### Files Found

| File           | Relevance                        | Role        |
| -------------- | -------------------------------- | ----------- |
| `path/to/file` | direct / related / test / config | description |

### Existing Patterns

- **Architecture**: {patterns}
- **Naming**: {conventions}
- **Error Handling**: {approach}
- **Testing**: {framework, conventions}
- **Style**: {formatting}

### Dependency Map

affected_file → imports: [deps] ← imported by: [dependents]

### Risks and Concerns

- {risk}: {description} (severity: low/medium/high)

### Context Summary

{paragraph for Planner}

### Open Questions

- {questions needing user input}
```

## Implementation Plan Template

```markdown
## Implementation Plan

### Solution Design

- **Approach**: {description}
- **Rationale**: {why}
- **Alternatives Considered**: {others and why rejected}

### Architecture Decisions (moderate/complex)

| Decision   | Choice   | Rationale |
| ---------- | -------- | --------- |
| {decision} | {choice} | {why}     |

### Do-Not-Touch List

- {file/area}: {reason}
- Dependency guardrails: {rules}

### Phase Breakdown

| Phase | Summary       | Scope      | Tasks   |
| ----- | ------------- | ---------- | ------- |
| 1     | {description} | {included} | {count} |
| 2     | {description} | {included} | {count} |
```

## Atomic Task Specification Template

```markdown
### Task {N}: {title}

- **Scope**: {what this task includes}
- **Non-goals**: {what this task explicitly excludes}
- **Acceptance criteria**:
  - [ ] {testable condition 1}
  - [ ] {testable condition 2}
- **Definition of done**:
  - [ ] Code reviewed
  - [ ] Tests pass
  - [ ] {additional completion requirements}
- **Automated tests**: {specific tests to add or update}
- **Manual test steps**:
  1. {step 1}
  2. {step 2}
- **Rollback note**: {how to revert this change}
- **Risk level**: {low / medium / high}
```

## Task Brief Template (for Coder)

```markdown
### Brief for Task {N}:

- **Scope and non-goals**: {what to do / what NOT to do}
- **Constraints**: {versions, environments, dependencies}
- **Relevant files**: {specific paths to read and modify}
- **Commands**: {build, test, lint commands to use}
- **Assumptions**: {explicit notes about system behaviour}
- **Patterns to follow**: {references to existing code}
```

## Implementation Report Template

```markdown
## Implementation Report — Task: {task title}

### Changes Made

| #   | File   | Action                   | Description   |
| --- | ------ | ------------------------ | ------------- |
| 1   | `path` | created/modified/deleted | what was done |

### Acceptance Criteria Status

- [ ] {criterion 1}: {implemented / not yet verifiable / blocked}
- [ ] {criterion 2}: {implemented / not yet verifiable / blocked}

### Guardrail Compliance

- **Do-not-touch list respected**: yes/no
- **No unrelated changes**: yes/no
- **No new dependencies**: yes/no

### Task Spec Adherence

- **Deviations**: none / list with rationale

### Known Issues

- {issues if any}

### Test Readiness

- Ready for verification: yes/no
```

## Verification Report Template

```markdown
## Verification Report — Task: {task title}

### Status: PASS / PASS_WITH_WARNINGS / FAIL

### Risk Level: low / medium / high

### Layer 1: Automated Checks

| Check             | Result        | Notes     |
| ----------------- | ------------- | --------- |
| Unit tests        | PASS/FAIL     | {details} |
| Integration tests | PASS/FAIL/N/A | {details} |
| Type check        | PASS/FAIL/N/A | {details} |
| Lint              | PASS/FAIL/N/A | {details} |
| Build             | PASS/FAIL/N/A | {details} |

### Layer 2: Behavioural Checks

| Manual Test Step      | Result    | Notes     |
| --------------------- | --------- | --------- |
| {step from task spec} | PASS/FAIL | {details} |

- **Edge cases**: pass/fail
- **Failure paths**: pass/fail

### Layer 3: Operational Checks

- **Error handling**: pass/fail
- **Logging**: pass/fail/n/a
- **Metrics**: pass/fail/n/a
- **Configuration**: pass/fail/n/a
- **Migrations**: pass/fail/n/a
- **Rollback procedure**: pass/fail

### Layer 4: Security Checks

- **Input validation**: pass/fail
- **Output encoding**: pass/fail
- **Authorisation**: pass/fail/n/a
- **Secrets management**: pass/fail
- **Logging hygiene**: pass/fail
- **Dependency security**: pass/fail/n/a

### Acceptance Criteria

- [x] {criterion_1} - PASS: {evidence}
- [ ] {criterion_2} - FAIL: {reason}

### Definition of Done

- [x] {item_1} - Complete
- [ ] {item_2} - Incomplete: {reason}

### Issues Found

| #   | Severity              | Layer | Description | Fix Required |
| --- | --------------------- | ----- | ----------- | ------------ |
| 1   | critical/warning/info | 1-4   | desc        | yes/no       |

### Fix Instructions (if FAIL)

{specific instructions for Coder}
```

## EPCV Summary Template (Final Delivery)

```markdown
## EPCV Complete

**Request**: {summary}
**Complexity**: simple / moderate / complex
**Status**: PASS / PASS_WITH_WARNINGS

### Exploration: {n} files examined, {n} patterns identified

### Plan: {n} phases, {n} tasks specified

### Implementation: {n} tasks completed, {n} files changed, {n} commits

### Verification: {n}/{n} acceptance criteria passed, {n}/{n} definition of done complete

### Changes by Task

- **Task 1**: {title} — {files changed}
- **Task 2**: {title} — {files changed}

### Recommendations

- {follow-up suggestions}
```
