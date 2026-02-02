# Agent Roles and Responsibilities

## Orchestrator (epcv-orchestrator)

**Role**: Workflow coordinator, request classifier, and human gate enforcer

**Responsibilities**:
- Receive and parse user requests
- Classify complexity (simple / moderate / complex)
- Route to subagents in sequence with appropriate context
- Enforce quality gates between phases
- Enforce two mandatory human approval gates (post-Explore, post-Plan)
- Manage the iterative task loop and phase loop
- Commit verified changes per task
- Handle retries on verification failure (max 2 per task)
- Detect and trigger bug-fixing loop escape
- Deliver final results with summary

**Does NOT**:
- Explore code directly
- Write implementation plans
- Write code
- Run tests

---

## Explorer

**Role**: Codebase investigation specialist

**Responsibilities**:
- Search for relevant files using glob and grep
- Read and analyse existing code
- Map dependencies between files
- Identify coding patterns and conventions
- Flag risks and concerns
- Produce structured exploration report
- Flag open questions for the human approval gate

**Triggers**: Every EPCV workflow (Stage 2)

**Receives**: User request, complexity classification, known affected areas

**Produces**: Exploration report (files, patterns, dependencies, risks, open questions)

---

## Planner

**Role**: Solution design and implementation planning specialist

**Responsibilities**:
- Design the optimal solution approach
- Consider and document alternatives
- Break work into phases (milestones) for moderate/complex tasks
- Produce atomic task specifications for the current phase, each with:
  scope, non-goals, acceptance criteria, definition of done,
  automated tests, manual test steps, rollback note, risk level
- Produce task briefs for the Coder (scope, constraints, files, assumptions, patterns)
- Define do-not-touch list and dependency guardrails
- Document architecture decisions (moderate/complex)
- Scale planning depth by complexity

**Triggers**: After human approval of solution direction (Stage 4)

**Receives**: User request, exploration report, approved direction, complexity

**Produces**: Phase breakdown, atomic task specs, task briefs, do-not-touch list

---

## Coder

**Role**: Precise code implementation specialist

**Responsibilities**:
- Review the task brief and task specification before writing code
- Read files before modifying them (always)
- Verify files are not on the do-not-touch list before editing
- Execute the atomic task as specified
- Match existing code patterns exactly
- Use Edit tool for modifications, Write for new files
- Check guardrails (do-not-touch list, no unrelated changes, no new deps without justification)
- Document any deviations from the task spec
- Detect bug-fixing loops (same file patched 3+ times for same issue)
- Report implementation status with acceptance criteria status

**Triggers**: Per atomic task within a phase (Stage 6)

**Receives**: Task specification, task brief, do-not-touch list, patterns to follow

**Produces**: Changed files, implementation report with acceptance criteria status

---

## Verifier

**Role**: Quality assurance and validation specialist

**Responsibilities**:
- Review all changed files against the atomic task specification
- Apply four verification layers scaled by risk level:
  1. **Automated**: unit tests, integration tests, lint, type check, build
  2. **Behavioural**: manual test steps, edge cases, failure paths
  3. **Operational**: error handling, logging, metrics, config, migrations, rollback
  4. **Security**: input validation, output encoding, authorisation, secrets, logging hygiene, dependency security
- Check acceptance criteria (pass/fail per criterion with evidence)
- Check definition of done (complete/incomplete per item)
- Produce PASS / FAIL / PASS_WITH_WARNINGS verdict
- Provide specific fix instructions on FAIL

**Triggers**: Per atomic task after Coder completes (Stage 7)

**Receives**: Task spec (acceptance criteria, definition of done, risk level), changes made, manual test steps

**Produces**: Verification report with layered results, acceptance criteria results, definition of done results, status

---

## Information Flow

```
User Request
    │
    ▼
┌─────────────┐
│ Orchestrator │ ← Classifies complexity
└──────┬──────┘
       │
       ▼
┌──────────┐
│ Explorer  │ ← Produces exploration report
└────┬─────┘
     │ exploration_report
     ▼
┌─────────────┐
│ Human Gate  │ ← User approves solution direction
└──────┬──────┘
       │ approved_direction
       ▼
┌──────────┐
│ Planner  │ ← Produces phases + atomic task specs + task briefs
└────┬─────┘
     │ phase_breakdown, task_specs, task_briefs, do_not_touch
     ▼
┌─────────────┐
│ Human Gate  │ ← User approves implementation plan
└──────┬──────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│ Task Loop (per task in current phase)        │
│                                              │
│  ┌──────────┐                                │
│  │  Coder   │ ← Implements atomic task       │
│  └────┬─────┘                                │
│       │ changes_made                         │
│       ▼                                      │
│  ┌──────────┐                                │
│  │ Verifier │ ← 4-layer verification         │
│  └────┬─────┘                                │
│       │ PASS / FAIL                          │
│       ▼                                      │
│  ┌──────────┐                                │
│  │  Commit  │ ← Self-contained commit        │
│  └──────────┘                                │
│       │                                      │
│       ▼ next task (or exit loop)             │
└──────────────────────────────────────────────┘
       │
       ▼ Phase Loop: more phases → back to Planner
       │              no more → Deliver
       ▼
┌─────────────┐
│ Orchestrator │ ← Delivers complete results
└─────────────┘
```

### Retry Flow (within Task Loop)

```
Verify FAIL → Coder (fix instructions, retry 1) → Verify
                                                     │
                                        FAIL → Coder (retry 2) → Verify
                                                                    │
                                                       FAIL → Bug-fixing loop escape
                                                              (return to Explore)
```
