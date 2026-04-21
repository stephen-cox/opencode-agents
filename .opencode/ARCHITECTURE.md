# EPCV Architecture Guide

## System Architecture

```text
                    User Request
                          │
                          ▼
               ┌─────────────────────┐
               │   Human (You)       │
               │  (Classify request, │
               │   drive workflow)   │
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
               │  /explore           │ ← Phase 1: Understand
               │  (Explorer agent)   │
               └──────────┬──────────┘
                          │ exploration_report
                          ▼
               ┌─────────────────────┐
               │   Human Gate #1     │ ← Review findings, approve direction
               └──────────┬──────────┘
                          │ approved_direction
                          ▼
               ┌─────────────────────┐
               │  /plan              │ ← Phase 2: Design (phases + atomic tasks)
               │  (Planner agent)    │
               └──────────┬──────────┘
                          │ task_specs, task_briefs, do_not_touch
                          ▼
               ┌─────────────────────┐
               │   Human Gate #2     │ ← Review plan, approve before coding
               └──────────┬──────────┘
                          │
                          ▼
               ┌─────────────────────────────────────┐
               │  Task Loop (per task in phase)       │
               │                                     │
               │  ┌─────────────────────┐            │
               │  │  /code              │ ← Phase 3  │
               │  │  (Coder agent)      │            │
               │  └──────────┬──────────┘            │
               │             │ changes_made           │
               │             ▼                        │
               │  ┌─────────────────────┐            │
               │  │  /verify            │ ← Phase 4  │
               │  │  (Verifier agent)   │            │
               │  └──────────┬──────────┘            │
               │             │ PASS / FAIL            │
               │             ▼                        │
               │  ┌─────────────────────┐            │
               │  │  /commit-task       │ ← Commit   │
               │  └──────────┬──────────┘            │
               │             │                        │
               │             ▼ next task or exit      │
               └─────────────────────────────────────┘
                          │
                          ▼ Phase Loop
                     ┌────┴────┐
                     │         │
               ┌─────▼───┐ ┌──▼──────┐
               │ More     │ │ No more │
               │ phases   │ │ phases  │
               │→ /plan   │ │→ Done   │
               └─────────┘ └─────────┘
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

## Component Relationships

### Human-Driven Routing (No Orchestrator)

The human drives the workflow by invoking commands directly. There is no orchestrator
agent. Each command routes to a specialised agent:

1. `/explore` → Explorer agent (read-only investigation)
2. Review exploration report, approve direction
3. `/plan` → Planner agent (solution design, atomic task specs)
4. Review plan, approve before coding
5. `/code` → Coder agent (implement atomic task)
6. `/verify` → Verifier agent (4-layer validation)
7. `/commit-task` → Coder agent (commit verified changes)
8. Loop through remaining tasks and phases

### Context Flow

Each agent receives context through the conversation. The human provides
relevant context from prior phases when invoking each command:

| Agent    | Needs From Prior Phases                                  |
| -------- | -------------------------------------------------------- |
| Explorer | User request, complexity assessment                      |
| Planner  | User request, exploration report, approved direction     |
| Coder    | Task spec, task brief, do-not-touch list, patterns       |
| Verifier | Task spec (acceptance criteria, DoD, risk), changes made |

### Quality Gates

```text
/explore ──gate──▶ Human Approval ──gate──▶ /plan ──gate──▶ Human Approval
    ──gate──▶ /code ──gate──▶ /verify ──gate──▶ /commit-task ──gate──▶ Task Loop
```

Each gate checks specific criteria before allowing progression.
Failed gates block the workflow until resolved.
Human gates require explicit user approval.

### Agent Format

All agents use OpenCode format:

- YAML frontmatter with `description` (required) and `mode: primary`
- Optional: `temperature`, `tools` (map of tool→boolean), `permission` (map with bash glob support)
- Body is plain markdown (no XML tags)

## Design Decisions

### Why No Orchestrator?

The EPCV workflow has two mandatory human approval gates. Since the human is
already present at every decision point, an orchestrator agent adds indirection
without proportional value. The human naturally:

- Classifies request complexity
- Routes to the appropriate agent via commands
- Reviews output and approves at gates
- Decides whether to retry, loop, or escalate
- Manages the task and phase loops

Removing the orchestrator simplifies the architecture, eliminates permission
ambiguity (the orchestrator needed write/edit for commits but shouldn't write code),
and gives the human more direct control.

### Why an Iterative Workflow?

The workflow is iterative: tasks loop within phases, phases loop within plans.
A single-pass workflow cannot handle multi-task features or multi-phase projects.
The iterative structure ensures:

- Each task is independently verified and committed
- Later phases are planned in detail only when reached
- The workflow scales from bugfixes (1 task) to projects (many phases)

### Why Human Gates?

Without approval gates:

- The assistant might pursue the wrong solution direction
- The plan might not match the developer's intent
- Requirements and boundaries are not validated

### Why Atomic Tasks?

Without them:

- Changes are too large to review confidently
- Failures are hard to isolate and revert
- The assistant's scope creep goes unchecked

### Why 4 Phases?

| Phase   | Prevents                                   |
| ------- | ------------------------------------------ |
| Explore | Blind changes that break existing patterns |
| Plan    | Rework from poor design decisions          |
| Code    | Inconsistency from ad-hoc implementation   |
| Verify  | Bugs and regressions reaching the user     |

### Why Separate Agents?

Each agent has a focused responsibility and optimised configuration:

- **Explorer**: Read-only tools (read, glob, grep), temperature 0.1
- **Planner**: Read-only tools, temperature 0.2 (slightly more creative for design)
- **Coder**: Full tools (write, edit, bash, read, glob, grep), temperature 0.1
- **Verifier**: Bash + read (no write/edit), temperature 0.1, all bash commands allowed

Separation prevents the "do everything at once" anti-pattern that leads to skipped
steps and lower quality.

### Why Bug-Fixing Loop Escape?

Repeated iterations of small patches without new information result in wasted effort
and increasingly convoluted code. The escape pattern forces a return to Explore to
gather new evidence and refine the hypothesis before continuing.

### Why Complexity Classification?

Not every task needs the same rigour:

- A typo fix doesn't need architecture analysis
- A new auth system shouldn't get a quick plan

Classification ensures appropriate effort for each task.

## Performance Characteristics

| Metric              | Expected                                       |
| ------------------- | ---------------------------------------------- |
| Context efficiency  | High — each agent gets only relevant context   |
| First-pass success  | ~80% — exploration prevents blind errors       |
| Retry success rate  | ~95% — specific fix instructions from Verifier |
| Human gate overhead | Minimal — concise summaries for simple tasks   |
| Iterative scaling   | Linear — task/phase loops handle any size      |
