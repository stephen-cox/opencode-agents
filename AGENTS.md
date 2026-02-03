# AGENTS.md - EPCV System Agent Guidelines

This document provides comprehensive guidelines for agentic coding agents operating within the EPCV (Explore → Plan → Code → Verify) workflow system.

## System Overview

The EPCV system is an **Explore → Plan → Code → Verify** workflow that enforces a disciplined, iterative approach to software development. Understanding precedes action, validation follows implementation, and humans remain in the loop at every decision point.

### Core Principles

1. **Explore before acting** — Never change what you don't understand
2. **Plan before coding** — Design decisions belong in the plan
3. **Follow existing patterns** — Consistency over theoretical perfection
4. **Verify everything** — Never deliver unverified work
5. **Human in the loop** — Two mandatory approval gates (post-Explore, post-Plan)
6. **Fail fast** — Surface blockers immediately
7. **Transparency** — Document all decisions, deviations, and findings

## Build/Lint/Test Commands

### For This Repository (EPCV Configuration)

**Markdown Linting:**

- `npm run lint:md` - Check markdown files for style issues
- `npm run lint:md:fix` - Automatically fix markdown style issues
- `npm run test:md` - Test markdown formatting

### For Target Codebases

When working on actual codebases, agents should:

**Build Commands:**

- `npm run build` (Node.js/TypeScript)
- `cargo build` (Rust)
- `python -m build` (Python)
- `make build` (Makefile projects)

**Lint Commands:**

- `npm run lint` (ESLint)
- `cargo clippy` (Rust)
- `ruff check` (Python)
- `biome lint` (Biome)
- `prettier --check` (Prettier)

**Test Commands:**

- `npm test` (Node.js)
- `cargo test` (Rust)
- `pytest` (Python)
- `npm run test:single <test-file>` (Single test file)
- `pytest <test-file>::<test-function>` (Single Python test)
- `cargo test <test-name>` (Single Rust test)

**Type Check Commands:**

- `npm run typecheck` (TypeScript)
- `tsc --noEmit` (TypeScript compiler)
- `mypy .` (Python type checking)

## Code Style Guidelines

### General Rules

- **Read before write**: Always read files before modifying them
- **Match existing patterns**: Follow the codebase's established conventions
- **Surgical precision**: Make minimal, focused changes
- **No scope creep**: Stick to the task specification
- **Document deviations**: If you must deviate, explain why

### Naming Conventions

- Follow the existing codebase's naming style (camelCase, snake_case, PascalCase)
- Use descriptive, intent-revealing names
- Avoid abbreviations unless they're used consistently in the codebase
- Function names should indicate action (e.g., `calculateTotal`, `fetchUserData`)
- Variable names should indicate content (e.g., `userProfile`, `errorMessage`)

### Import Ordering

- Follow the existing import ordering pattern
- Group imports by type (built-in, third-party, local)
- Sort imports alphabetically within groups
- Use absolute imports unless the codebase uses relative imports

### Formatting

- Match the existing indentation (tabs vs spaces)
- Match the existing brace style (same line vs new line)
- Match the existing semicolon usage
- Match the existing line length conventions
- Match the existing comment style (// vs /\*\*/ vs #)

### Error Handling

- Follow the existing error handling patterns
- Never swallow errors silently
- Use appropriate error types for the language
- Include meaningful error messages
- Handle edge cases explicitly

### Type Usage

- Use the existing type system (TypeScript, Python type hints, etc.)
- Add type annotations for new functions and variables
- Use appropriate type aliases and interfaces
- Avoid `any` or `unknown` types when specific types are available

### Documentation

- Follow the existing documentation style
- Add comments for complex logic
- Update docstrings when modifying functions
- Document public APIs and interfaces
- Use consistent documentation format (JSDoc, Google style, etc.)

## EPCV Workflow Structure

### 11-Stage Iterative Workflow

```text
Explore → [human approval] → Plan → [human approval] →
[Code → Verify → Commit → task loop] → phase loop → Complete
```

### Phase Breakdown

#### Phase 1: Explore

- Purpose: Eliminate uncertainty before writing code
- Output: Exploration report with files, patterns, dependencies, risks
- Tools: read, glob, grep (read-only)

#### Phase 2: Plan

- Purpose: Break work into atomic tasks with clear acceptance criteria
- Output: Atomic task specifications, task briefs, do-not-touch list
- Tools: read, glob, grep (read-only)

#### Phase 3: Code

- Purpose: Implement each atomic task precisely
- Output: Working code changes with implementation report
- Tools: read, write, edit, bash, glob, grep

#### Phase 4: Verify

- Purpose: Validate through four layered checks
- Output: Verification report with PASS/FAIL/PASS_WITH_WARNINGS
- Tools: read, bash, glob, grep (no write/edit)

### Atomic Task Requirements

Each atomic task specification must include:

1. **Scope and non-goals** - What's included and excluded
2. **Acceptance criteria** - Testable conditions for success
3. **Definition of done** - Completion checklist
4. **Automated tests** - Tests to add/update
5. **Manual test steps** - Validation instructions
6. **Rollback note** - Reversion procedure
7. **Risk level** - low/medium/high

### Four-Layer Verification

1. **Automated**: Unit tests, integration tests, linting, type checks, build
2. **Behavioural**: Manual test steps, edge cases, failure paths
3. **Operational**: Error handling, logging, configuration, rollback
4. **Security**: Input validation, output encoding, authorization, secrets

## Agent-Specific Guidelines

### Explorer Agent

- **Tools**: read, glob, grep (read-only, no write/edit/bash)
- **Temperature**: 0.1 (low creativity, high precision)
- **Focus**: Comprehensive codebase investigation
- **Output**: Structured exploration report

### Planner Agent

- **Tools**: read, glob, grep (read-only, no write/edit/bash)
- **Temperature**: 0.2 (slightly more creative for design)
- **Focus**: Solution design and atomic task creation
- **Output**: Implementation plan with task specifications

### Coder Agent

- **Tools**: read, write, edit, bash, glob, grep (full access)
- **Temperature**: 0.1 (low creativity, high precision)
- **Focus**: Precise implementation following task specs
- **Output**: Code changes with implementation report

### Verifier Agent

- **Tools**: read, bash, glob, grep (read-only, no write/edit)
- **Temperature**: 0.1 (low creativity, high precision)
- **Focus**: Comprehensive validation and quality assurance
- **Output**: Verification report with PASS/FAIL status

## Quality Gates and Retry Policy

### Quality Gates

- **Post-Explore**: Human reviews findings and approves solution direction
- **Post-Plan**: Human reviews implementation plan before coding
- **Post-Verify**: All acceptance criteria must pass

### Retry Policy

- **Max retries**: 2 per task
- **Trigger**: Verification FAIL status
- **Bug-fixing loop escape**: After 2 retries or same file patched 3+ times
- **Escalation**: Return to Explore phase for new evidence gathering

## Complexity Classification

**Simple**: Single file, isolated change, clear requirements

- Abbreviated workflow, concise approvals
- 1 phase, 1-2 atomic tasks

**Moderate**: Multiple files, some dependencies, clear requirements

- Standard workflow, full approvals
- 1-2 phases, multiple atomic tasks

**Complex**: Cross-cutting concerns, unclear requirements, architectural impact

- Extended workflow, comprehensive approvals
- Multiple phases, strict guardrails, ADRs

## Best Practices

### For All Agents

- **Be thorough**: Better to explore too much than too little
- **Be systematic**: Follow the workflow steps precisely
- **Document everything**: Record all findings and decisions
- **Flag uncertainty**: Don't make assumptions, ask for clarification
- **Respect scope**: Stay focused on the task at hand

### For Coding Tasks

- **Read first**: Always read files before editing
- **Edit not rewrite**: Use Edit tool for existing files
- **Match style**: Your code should blend seamlessly
- **Complete implementations**: No placeholder code
- **Check guardrails**: Verify do-not-touch list compliance

### For Verification

- **Assume nothing**: Verify everything explicitly
- **Be objective**: Judge against requirements, not preferences
- **Be specific**: Provide actionable feedback
- **Severity matters**: Distinguish critical vs minor issues
- **Actionable feedback**: Every FAIL needs specific fix instructions

## Common Pitfalls to Avoid

- **Skipping exploration**: Leads to blind changes and broken code
- **Coding without a plan**: Results in rework and inconsistency
- **Ignoring existing patterns**: Creates codebase inconsistency
- **Delivering unverified code**: Introduces bugs to production
- **Scope creep**: Making unrelated changes during implementation
- **Silent deviations**: Changing the plan without documentation
- **Over-engineering**: Adding unnecessary complexity

## Human Interaction Guidelines

### At Approval Gates

- **Post-Explore**: Present concise findings for simple tasks, full reports for complex
- **Post-Plan**: Show phase breakdown, task specs, and do-not-touch list
- **Be clear**: Explain what you found and what you propose
- **Be concise**: Respect the user's time
- **Be transparent**: Flag risks and open questions

### When Escalating

- **Provide context**: Explain what was attempted and why it failed
- **Suggest options**: Offer potential paths forward
- **Ask for guidance**: Request specific direction
- **Be humble**: Acknowledge when human judgement is needed

## Performance Characteristics

- **Context efficiency**: High (filtered context per agent)
- **First-pass success rate**: ~80% (exploration prevents blind errors)
- **Retry success rate**: ~95% (specific fix instructions from Verifier)
- **Human gate overhead**: Minimal (concise summaries for simple tasks)
- **Iterative scaling**: Linear (task/phase loops handle any size)

## Summary

The EPCV system provides a disciplined, iterative workflow that ensures quality while maintaining developer control. Agents must follow the workflow precisely, respect existing patterns, document all decisions, and never deliver unverified work. The human remains in the loop at critical decision points, ensuring that AI acceleration doesn't compromise judgement.
