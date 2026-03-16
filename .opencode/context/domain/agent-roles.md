# Agent Roles and Responsibilities

## Human (Workflow Driver)

**Role**: Workflow coordinator, request classifier, and approval gate enforcer

The human drives the EPCV workflow by invoking commands directly. There is no
orchestrator agent — the human performs all coordination tasks:

- Classify request complexity (simple / moderate / complex)
- Invoke agents in sequence via commands (`/explore`, `/plan`, `/code`, `/verify`, `/commit-epcv`)
- Review output at each step and approve at human gates
- Manage the task loop (advance to next task after commit)
- Manage the phase loop (return to `/plan` for next phase)
- Handle retries on verification failure (re-run `/code` with fix instructions, max 2 per task)
- Detect bug-fixing loops and re-run `/explore` for new evidence
- Commit verified changes per task
- Escalate when retries are exhausted

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

**Triggers**: `/explore` command

**Receives**: User request, complexity context

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

**Triggers**: `/plan` command (after human approval of solution direction)

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

**Triggers**: `/code` command (per atomic task within a phase)

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

**Triggers**: `/verify` command (per atomic task after Coder completes)

**Receives**: Task spec (acceptance criteria, definition of done, risk level), changes made, manual test steps

**Produces**: Verification report with layered results, acceptance criteria results, definition of done results, status

---

## Information Flow

```text
User Request
    │
    ▼
┌─────────────┐
│ Human (You) │ ← Classifies complexity, drives workflow
└──────┬──────┘
       │
       ▼
┌──────────┐
│ /explore │ ← Produces exploration report
│ Explorer │
└────┬─────┘
     │ exploration_report
     ▼
┌─────────────┐
│ Human Gate  │ ← You approve solution direction
└──────┬──────┘
      │ approved_direction
      ▼
┌──────────┐
│ /plan    │ ← Produces phases + atomic task specs + task briefs
│ Planner  │
└────┬─────┘
     │ phase_breakdown, task_specs, task_briefs, do_not_touch
     ▼
┌─────────────┐
│ Human Gate  │ ← You approve implementation plan
└──────┬──────┘
      │
      ▼
┌──────────────────────────────────────────────┐
│ Task Loop (per task in current phase)        │
│                                              │
│  ┌──────────┐                                │
│  │ /code    │ ← Implements atomic task       │
│  │ Coder    │                                │
│  └────┬─────┘                                │
│       │ changes_made                         │
│       ▼                                      │
│  ┌──────────┐                                │
│  │ /verify  │ ← 4-layer verification         │
│  │ Verifier │                                │
│  └────┬─────┘                                │
│       │ PASS / FAIL                          │
│       ▼                                      │
│  ┌─────────────┐                             │
│  │ /commit-epcv│ ← Self-contained commit     │
│  └─────────────┘                             │
│       │                                      │
│       ▼ next task (or exit loop)             │
└──────────────────────────────────────────────┘
       │
       ▼ Phase Loop: more phases → back to /plan
       │              no more → Done
```

### Retry Flow (within Task Loop)

```text
/verify FAIL → /code (fix instructions, retry 1) → /verify
                                                      │
                                         FAIL → /code (retry 2) → /verify
                                                                     │
                                                        FAIL → Bug-fixing loop escape
                                                               (/explore for new evidence)
                                                               → Escalate if still fails
```
