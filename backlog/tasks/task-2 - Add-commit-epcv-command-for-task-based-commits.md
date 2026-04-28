---
id: TASK-2
title: Add /commit-epcv command for task-based commits
status: Done
assignee: []
created_date: "2026-02-05 22:15"
updated_date: "2026-02-05 22:21"
labels:
  - epcv
  - commands
  - usability
dependencies: []
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->

Create a `/commit` command that commits all files changed during implementation and verification of a task. The commit message should be short and reference the task number.

**Commit message format**: `task-{n} {short description}` where description is auto-generated from the task title.

**Command usage**:

- `/commit {n}` — Commit with explicit task number
- `/commit` — Infer task from context (e.g., "In Progress" task in Backlog.md), ask for clarification if unclear

**Files to create/modify**:

- Create: `.opencode/command/commit.md`
- Update: `.opencode/navigation.md` (Quick Start table + Commands table)
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria

<!-- AC:BEGIN -->

- [x] #1 `.opencode/command/commit.md` exists with correct YAML frontmatter (description, agent: epcv-orchestrator)
- [x] #2 Command supports both `/commit {n}` and `/commit` (auto-infer) modes
- [x] #3 Instructions document commit message format: `task-{n} {short description}`
- [x] #4 Instructions explain task inference from Backlog.md "In Progress" status
- [x] #5 Instructions explain fallback to ask user if task cannot be inferred
- [x] #6 `.opencode/navigation.md` Quick Start table includes `/commit` with purpose
- [x] #7 `.opencode/navigation.md` Commands table includes `/commit` with file path and agent
- [x] #8 Markdown linting passes (`npm run lint:md`)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->

## Implementation Summary

### Files Created

- `.opencode/command/commit.md` — New `/commit` command

### Files Modified

- `.opencode/navigation.md` — Added `/commit` to Quick Start and Commands tables

### Design Decisions

- Routes to `epcv-orchestrator` (has bash/git permissions)
- Supports both `/commit {n}` (explicit) and `/commit` (auto-infer) modes
- Auto-infers task from Backlog.md "In Progress" status
- Falls back to asking user if task cannot be determined
- Commit message format: `task-{n} {short description}`

### Verification

- All modified files pass markdown linting
- Command follows existing patterns from `/code` command

## Rename

Renamed from `/commit` to `/commit-epcv` to avoid conflict with existing global `/commit` command that uses conventional commits with emojis.

<!-- SECTION:NOTES:END -->
