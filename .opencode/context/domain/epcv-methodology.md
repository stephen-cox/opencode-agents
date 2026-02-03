# EPCV Methodology

## Core Philosophy

The Explore → Plan → Code → Verify (EPCV) methodology enforces a disciplined
approach to software development where **understanding precedes action**,
**validation follows implementation**, and **a human remains in the loop**
at every decision point.

AI coding assistants behave like overly enthusiastic junior developers: fast,
broadly knowledgeable, and responsive, but lacking deep understanding of the
specific project. Their speed is an advantage only if it is controlled. The
EPCV workflow ensures that speed does not come at the cost of quality.

## The Iterative Workflow

The workflow is not a single pass through four phases. It is an iterative
structure with task loops and phase loops:

```text
Explore → [human approval] → Plan (phases + atomic tasks) → [human approval] →
  [Code → Verify → Commit → task loop] → phase loop → Complete
```

Work is broken into **phases** (milestones). Each phase is broken into
**atomic tasks**. Each task is coded, verified, and committed individually.
When all tasks in a phase are done, the next phase is planned in detail.

## The Four Phases

### Phase 1: Explore

- **Purpose**: Eliminate uncertainty before writing code
- **Key Question**: "What exists, what will be affected, and what does success look like?"
- **Output**: Exploration report with files, patterns, dependencies, risks, open questions
- **Human Gate**: User reviews findings and approves solution direction before planning
- **Anti-pattern**: Skipping exploration leads to blind changes that break things

### Phase 2: Plan

- **Purpose**: Break work into atomic tasks with clear acceptance criteria
- **Key Question**: "What are the smallest verifiable units of work?"
- **Output**: Phase breakdown, atomic task specifications (scope, non-goals, acceptance criteria, definition of done, automated tests, manual test steps, rollback note, risk level), task briefs, do-not-touch list
- **Human Gate**: User reviews the plan and approves before coding begins
- **Anti-pattern**: Coding without a plan leads to rework and inconsistency

### Phase 3: Code

- **Purpose**: Implement each atomic task precisely as specified
- **Key Question**: "Does this match the task spec, follow existing patterns, and respect guardrails?"
- **Output**: Working code changes with implementation report and acceptance criteria status
- **Anti-pattern**: Deviating from the task spec without documentation causes confusion

### Phase 4: Verify

- **Purpose**: Validate through four layered checks scaled by risk
- **Key Question**: "Do all acceptance criteria pass and is the definition of done complete?"
- **Output**: Verification report with PASS / FAIL / PASS_WITH_WARNINGS status
- **Four Layers**: Automated → Behavioural → Operational → Security
- **Anti-pattern**: Delivering unverified code leads to bugs in production

## Atomic Tasks

An atomic task is the fundamental unit of work. It must be:

- **Small enough to review confidently**
- **Independently verifiable**
- **Revertible without disrupting other work**

Each atomic task specification contains:

1. **Scope and non-goals**: What the task includes and excludes
2. **Acceptance criteria**: Clear, testable conditions that define success
3. **Definition of done**: Checklist of completion requirements
4. **Automated tests**: Specific tests to add or update
5. **Manual test steps**: Step-by-step validation instructions
6. **Rollback note**: How to revert the change
7. **Risk level**: low / medium / high — determines verification rigour

## Human Gates

Two mandatory human approval points ensure the developer remains in control:

1. **Post-Explore**: Human reviews exploration findings and approves solution direction before planning begins
2. **Post-Plan**: Human reviews the implementation plan (phases, tasks, acceptance criteria, do-not-touch list) before coding begins

Principle: a human must remain in the loop for requirements, boundaries, code review, and final verification. The assistant accelerates the process but does not replace judgement.

## Bug-Fixing Loop Escape

If the same file has been patched 3+ times for the same issue, or 2 retries are exhausted without progress, the workflow stops patching and returns to Explore to gather new evidence, refine the hypothesis, and adjust the plan. This prevents wasted effort from repeated iterations of small patches without a change in approach.

## Four-Layer Verification

Verification applies multiple layers of checks, each catching different classes of errors:

1. **Automated**: Unit tests, integration tests, linting, type checks, build steps
2. **Behavioural**: Manual test scripts, edge cases, failure paths, real-world interactions
3. **Operational**: Error handling, logging, metrics, configuration, migrations, rollback
4. **Security**: Input validation, output encoding, authorisation, secrets management, logging hygiene, dependency security

Verification effort scales with the task's risk level, but is never optional.

## Complexity Levels

| Level    | Characteristics                                           | EPCV Approach                                        |
|----------|-----------------------------------------------------------|------------------------------------------------------|
| -------  | ----------------                                          | ---------------                                      |
| Simple   | Single file, isolated, clear requirements                 | Abbreviated: 1 phase, 1-2 tasks, concise approvals   |
| Moderate | Multiple files, some dependencies, clear requirements     | Standard: 1-2 phases, multiple tasks, full approvals |
| Complex  | Cross-cutting, unclear requirements, architectural impact | Extended: multiple phases, ADRs, strict guardrails   |

## Scaling the Workflow

- **Bugfixes**: Streamlined. Explore reproduces the issue, Plan defines a minimal fix, Verify is strict but narrow.
- **Features**: Expanded. More upfront Explore and Plan work, feature flags for incremental validation, more manual testing.
- **Projects**: Comprehensive. Discovery spikes and ADRs precede implementation, stronger review gates, the loop runs at multiple levels.

## Key Principles

1. **Explore before acting**: Never change what you don't understand
2. **Plan before coding**: Design decisions belong in the plan, not in the code
3. **Follow existing patterns**: Consistency over theoretical perfection
4. **Verify everything**: Never deliver unverified work
5. **Human in the loop**: Requirements, boundaries, code review, and final verification require human judgement
6. **Fail fast**: Surface blockers immediately, don't proceed with assumptions
7. **Transparency**: Document all decisions, deviations, and findings
