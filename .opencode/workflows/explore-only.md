# Explore-Only Workflow

## Overview

A standalone exploration workflow for when you need to understand the codebase
without making changes. Useful for research, onboarding, or pre-planning.

## Context Dependencies

- `context/domain/epcv-methodology.md` — Explore phase definition
- `context/domain/agent-roles.md` — Explorer role and responsibilities
- `context/processes/complexity-classification.md` — Thoroughness guide

## Workflow Stages

### Stage 1: Scope

**Actor**: Human
**Action**: Determine what to explore and how thoroughly
**Inputs**: User's exploration request
**Outputs**: Exploration scope and thoroughness level
**Success Criteria**: Clear scope defined

### Stage 2: Explore

**Command**: `/explore`
**Agent**: Explorer
**Action**: Investigate codebase per scope
**Inputs**: Exploration scope, thoroughness level
**Outputs**: Exploration report (files, patterns, dependencies, risks, open questions)
**Success Criteria**:

- All requested areas explored
- Patterns documented
- Dependencies mapped
- Risks identified
- Open questions flagged
- Findings clearly organised

### Stage 3: Review

**Actor**: Human
**Action**: Review exploration findings
**Inputs**: Exploration report
**Outputs**: Understanding of the codebase area

No human approval gate is needed since no changes are being made.

## Use Cases

- "How does the authentication system work?"
- "What files would be affected if I change the User model?"
- "What patterns does this project use for error handling?"
- "Map the dependencies of the payment module"
