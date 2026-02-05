# Workflows Navigation

## Available Workflows

### EPCV Standard (`epcv-standard.md`)

**The default workflow for most coding tasks.**

Runs the full iterative workflow: Explore → [human approval] → Plan → [human approval] → Code → Verify → Commit (per task, per phase).

| Complexity     | Approach                                                    | Duration        |
| -------------- | ----------------------------------------------------------- | --------------- |
| -------------- | ----------------------------------------------------------- | --------------- |
| Simple         | Abbreviated: 1 phase, 1-2 tasks, concise approvals          | 5-15 min        |
| Simple         | Abbreviated: 1 phase, 1-2 tasks, concise approvals          | 5-15 min        |
| Moderate       | Standard: 1-2 phases, multiple tasks, full approvals        | 15-45 min       |
| Complex        | Extended: multiple phases, ADRs, strict guardrails          | 45-90+ min      |

**Use when**: You want to make changes to the codebase.

**Trigger**: `/epcv <request>`

---

### Explore Only (`explore-only.md`)

**Investigation without changes.**

Runs only the Explore phase to understand the codebase.

**Use when**: You want to understand code without changing it.

**Trigger**: `/explore <question>`

---

### Verify Existing (`verify-existing.md`)

**Review code that already exists.**

Runs a quick Explore for context, then full 4-layer verification (automated, behavioural, operational, security) scaled by risk.

**Use when**: You want to review code quality, check for issues, or validate changes.

**Trigger**: `/verify <what to check>`

---

## Workflow Selection Guide

| I want to...                     | Use                  |
| -------------------------------- | -------------------- |
| Build a feature                  | `/epcv`              |
| Fix a bug                        | `/epcv`              |
| Refactor code                    | `/epcv`              |
| Understand code                  | `/explore`           |
| Review code quality              | `/verify`            |
| Plan before committing           | `/plan`              |
| Get a second opinion on approach | `/plan`              |
| Execute an approved plan         | `/plan` then `/code` |
