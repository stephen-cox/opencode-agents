# EPCV Architecture Guide

## System Architecture

```text
                    User Request
                          │
                          ▼
               ┌─────────────────────┐
               │   EPCV Orchestrator  │
               │  (Request Classifier │
               │   + Phase Router)    │
               └──────────┬──────────┘
                          │
           ┌──────────────┼──────────────┐
           │              │              │
      ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
      │ Simple  │   │Moderate │   │ Complex │
      │(abbrev) │   │(standard│   │(extended│
      └────┬────┘   └────┬────┘   └────┬────┘
           │              │              │
           └──────────────┼──────────────┘
                          │
                          ▼
               ┌─────────────────────┐
               │     @explorer       │ ← Stage 2: Understand
               │  (Codebase Search,  │
               │   Pattern Analysis) │
               └──────────┬──────────┘
                          │ exploration_report
                          ▼
               ┌─────────────────────┐
               │   Human Gate #1     │ ← Stage 3: Approve solution direction
               └──────────┬──────────┘
                          │ approved_direction
                          ▼
               ┌─────────────────────┐
               │     @planner        │ ← Stage 4: Design (phases + atomic tasks)
               │  (Phase Breakdown,  │
               │   Task Specs/Briefs)│
               └──────────┬──────────┘
                          │ task_specs, task_briefs, do_not_touch
                          ▼
               ┌─────────────────────┐
               │   Human Gate #2     │ ← Stage 5: Approve implementation plan
               └──────────┬──────────┘
                          │
                          ▼
               ┌─────────────────────────────────────┐
               │  Task Loop (per task in phase)       │
               │                                     │
               │  ┌─────────────────────┐            │
               │  │      @coder         │ ← Stage 6  │
               │  │  (Atomic Task Impl) │            │
               │  └──────────┬──────────┘            │
               │             │ changes_made           │
               │             ▼                        │
               │  ┌─────────────────────┐            │
               │  │     @verifier       │ ← Stage 7  │
               │  │  (4-Layer Checks)   │            │
               │  └──────────┬──────────┘            │
               │             │ PASS / FAIL            │
               │             ▼                        │
               │  ┌─────────────────────┐            │
               │  │      Commit         │ ← Stage 8  │
               │  └──────────┬──────────┘            │
               │             │                        │
               │             ▼ next task or exit      │
               └─────────────────────────────────────┘
                          │
                          ▼ Phase Loop (Stage 10)
                     ┌────┴────┐
                     │         │
               ┌─────▼───┐ ┌──▼──────┐
               │ More     │ │ No more │
               │ phases   │ │ phases  │
               │→ Plan    │ │→ Deliver│
               └─────────┘ └─────────┘
```

### Retry Flow (within Task Loop)

```text
Verify FAIL → Coder (fix instructions, retry 1) → Verify
                                                      │
                                         FAIL → Coder (retry 2) → Verify
                                                                     │
                                                        FAIL → Bug-fixing loop escape
                                                               (return to Explore)
                                                               → Escalate if still fails
```

## Component Relationships

### Orchestrator → Subagents (Manager-Worker Pattern)

The Orchestrator never performs phase work directly. It:

1. Classifies the request
2. Routes to the appropriate subagent with filtered context
3. Receives the subagent's output
4. Checks the quality gate
5. Presents results at human approval gates (post-Explore, post-Plan)
6. Manages the task loop and phase loop
7. Commits verified changes per task
8. Routes to the next subagent or delivers results

### Context Flow (Filtered)

Each subagent receives only the context it needs:

| Agent       | Receives                                                                        | Does NOT Receive                             |
|-------------|---------------------------------------------------------------------------------|----------------------------------------------|
| ----------- | ------------------------------------------------------------------------------- | -------------------------------------------- |
| ----------  | -----------------------------------------------------------------------------   | --------------------------------------       |
| Explorer    | Request, complexity, known affected areas                                       | Plans, code changes, verification            |
| Planner     | Request, exploration report, approved direction, complexity                     | Code changes, verification                   |
| Coder       | Task spec, task brief, do-not-touch list, patterns                              | Raw exploration, other tasks, verification   |
| Verifier    | Task spec (acceptance criteria, DoD, risk), changes, manual test steps          | Exploration details, task briefs             |

### Quality Gates (11-Stage Enforcement)

```text
Classify → Explore ──gate──▶ Human Approval ──gate──▶ Plan ──gate──▶ Human Approval
    ──gate──▶ Code ──gate──▶ Verify ──gate──▶ Commit ──gate──▶ Task Loop ──gate──▶ Phase Loop → Deliver
```

Each gate checks specific criteria before allowing progression.
Failed gates block the workflow until resolved.
Human gates require explicit user approval.

### Agent Format

All agents use OpenCode format:

- YAML frontmatter with `description` (required) and `mode` (`primary` or `subagent`)
- Optional: `temperature`, `tools` (map of tool→boolean), `permission` (map with bash glob support), `hidden`, `color`
- Body is plain markdown (no XML tags)

## Design Decisions

### Why an Iterative Workflow?

The guide's flowchart is iterative: tasks loop within phases, phases loop within plans. A single-pass workflow cannot handle multi-task features or multi-phase projects. The iterative structure ensures:

- Each task is independently verified and committed
- Later phases are planned in detail only when reached
- The workflow scales from bugfixes (1 task) to projects (many phases)

### Why Human Gates?

The guide requires human-in-the-loop at two points. Without approval gates:

- The assistant might pursue the wrong solution direction
- The plan might not match the developer's intent
- Requirements and boundaries are not validated

### Why Atomic Tasks?

The guide defines atomic tasks as the fundamental unit of work. Without them:

- Changes are too large to review confidently
- Failures are hard to isolate and revert
- The assistant's scope creep goes unchecked

### Why 4 Phases?

| Phase      | Prevents                                            |
|------------|-----------------------------------------------------|
| ---------- | --------------------------------------------------- |
| ---------  | -------------------------------------------------   |
| Explore    | Blind changes that break existing patterns          |
| Plan       | Rework from poor design decisions                   |
| Code       | Inconsistency from ad-hoc implementation            |
| Verify     | Bugs and regressions reaching the user              |

### Why Separate Agents?

Each agent has a focused responsibility and optimised configuration:

- **Explorer**: Read-only tools (read, glob, grep), temperature 0.1
- **Planner**: Read-only tools, temperature 0.2 (slightly more creative for design)
- **Coder**: Full tools (write, edit, bash, read, glob, grep), temperature 0.1, hidden
- **Verifier**: Bash + read (no write/edit), temperature 0.1, all bash commands allowed

Separation prevents the "do everything at once" anti-pattern that leads to skipped steps and lower quality.

### Why Bug-Fixing Loop Escape?

Repeated iterations of small patches without new information result in wasted effort and increasingly convoluted code. The escape pattern forces a return to Explore to gather new evidence and refine the hypothesis before continuing.

### Why Complexity Classification?

Not every task needs the same rigour:

- A typo fix doesn't need architecture analysis
- A new auth system shouldn't get a quick plan

Classification ensures appropriate effort for each task.

## Performance Characteristics

| Metric                   | Expected                                                        |
|--------------------------|-----------------------------------------------------------------|
| ------------------------ | --------------------------------------------------------------- |
| -----------------------  | -------------------------------------------------------------   |
| Context efficiency       | High — filtered passing per subagent                            |
| First-pass success       | ~80% — exploration prevents blind errors                        |
| Retry success rate       | ~95% — specific fix instructions from Verifier                  |
| Human gate overhead      | Minimal — concise summaries for simple tasks                    |
| Iterative scaling        | Linear — task/phase loops handle any size                       |
