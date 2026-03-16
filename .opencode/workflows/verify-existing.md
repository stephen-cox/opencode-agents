# Verify-Existing Workflow

## Overview

A standalone verification workflow for reviewing code that was already written
(by a human or another process). Skips Plan/Code and goes straight to
exploration for context, then full 4-layer verification.

## Context Dependencies

- `context/domain/epcv-methodology.md` — Verify phase and 4-layer verification
- `context/domain/agent-roles.md` — Verifier role and responsibilities
- `context/standards/quality-criteria.md` — Quality standards and verification depth
- `context/standards/validation-rules.md` — Validation rules

## Workflow Stages

### Stage 1: Scope

**Actor**: Human
**Action**: Determine what to verify and against what criteria
**Inputs**: User's verification request, files/changes to review
**Outputs**: Verification scope, risk level, criteria

### Stage 2: Explore (abbreviated)

**Command**: `/explore`
**Agent**: Explorer
**Action**: Quick context gathering for the files under review
**Inputs**: Files to verify
**Outputs**: Brief context report (patterns, dependencies)

### Stage 3: Verify

**Command**: `/verify`
**Agent**: Verifier
**Action**: Full 4-layer verification of specified code
**Inputs**: Files to verify, context report, user's criteria, risk level
**Outputs**: Verification report with layered results
**Success Criteria**:

- Layer 1 (Automated): tests, lint, type check, build checked
- Layer 2 (Behavioural): edge cases and failure paths validated
- Layer 3 (Operational): error handling, logging, config reviewed
- Layer 4 (Security): input validation, encoding, auth, secrets checked
- Verification depth matches risk level
- Clear PASS / FAIL / PASS_WITH_WARNINGS verdict produced

### Stage 4: Review

**Actor**: Human
**Action**: Review verification results
**Inputs**: Verification report
**Outputs**: Decision on next steps (fix issues, accept, etc.)

No human approval gates are needed since this is a review-only workflow.

## Use Cases

- "Review the changes I made to auth.ts"
- "Check if my PR is ready to merge"
- "Verify the code quality of the utils/ directory"
- "Run the test suite and report results"
