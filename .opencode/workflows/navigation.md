# Workflows Navigation

## Available Workflows

### EPCV Standard (`epcv-standard.md`)

**The default workflow for most coding tasks.**

The human drives the full iterative workflow: `/explore` → review → `/plan` → review → `/code` → `/verify` → `/commit-epcv` (per task, per phase).

| Complexity | Approach                                           | Duration   |
| ---------- | -------------------------------------------------- | ---------- |
| Simple     | Abbreviated: 1 phase, 1-2 tasks, concise reviews   | 5-15 min   |
| Moderate   | Standard: 1-2 phases, multiple tasks, full reviews | 15-45 min  |
| Complex    | Extended: multiple phases, ADRs, strict guardrails | 45-90+ min |

**Use when**: You want to make changes to the codebase.

**Start with**: `/explore <request>`

---

### Explore Only (`explore-only.md`)

**Investigation without changes.**

Runs only the Explore phase to understand the codebase.

**Use when**: You want to understand code without changing it.

**Command**: `/explore <question>`

---

### Verify Existing (`verify-existing.md`)

**Review code that already exists.**

Runs a quick Explore for context, then full 4-layer verification (automated, behavioural, operational, security) scaled by risk.

**Use when**: You want to review code quality, check for issues, or validate changes.

**Command**: `/verify <what to check>`

---

## Workflow Selection Guide

| I want to...                     | Use                                  |
| -------------------------------- | ------------------------------------ |
| Build a feature                  | `/explore` → `/plan` → `/code`       |
| Fix a bug                        | `/explore` → `/plan` → `/code`       |
| Refactor code                    | `/explore` → `/plan` → `/code`       |
| Understand code                  | `/explore`                           |
| Review code quality              | `/verify`                            |
| Plan before committing           | `/explore` → `/plan`                 |
| Get a second opinion on approach | `/explore` → `/plan`                 |
| Execute an approved plan         | `/code` → `/verify` → `/commit-epcv` |
