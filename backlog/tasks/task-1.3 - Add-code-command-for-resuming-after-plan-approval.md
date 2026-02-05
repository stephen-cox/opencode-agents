---
id: TASK-1.3
title: Add /code command for resuming after plan approval
status: Done
assignee: []
created_date: "2026-02-05 21:38"
updated_date: "2026-02-05 21:44"
labels:
  - epcv
  - commands
  - usability
dependencies: []
references:
  - "`command/epcv.md`"
  - "`command/plan.md`"
  - "`.opencode/navigation.md`"
  - "`.opencode/workflows/navigation.md`"
parent_task_id: TASK-1
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->

Currently there are commands for `/epcv`, `/explore`, `/plan`, and `/verify`, but no standalone `/code` command. If a user runs `/plan`, approves the plan, and then wants to proceed to implementation, they'd need to run `/epcv` again from scratch or manually instruct the orchestrator to continue.

A `/code` command would enable a natural workflow:

1. `/plan Add feature X` → Review exploration and plan
2. User approves
3. `/code` → Execute the Code → Verify → Commit loop for the approved plan

This makes the `/plan` → `/code` workflow more intuitive and avoids re-running exploration.

<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria

<!-- AC:BEGIN -->

- [x] #1 `/code` command exists in `.opencode/command/code.md`
- [x] #2 Command can resume from a previously approved plan
- [x] #3 Command routes to orchestrator to execute Code → Verify → Commit loop
- [x] #4 Documentation updated to describe the `/plan` → `/code` workflow
- [x] #5 Navigation files updated to include the new command
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->

## Implementation Summary

### Files Created

- `.opencode/command/code.md` - New command file for `/code`

### Files Modified

- `.opencode/navigation.md` - Added `/code` to Quick Start table and Commands table
- `.opencode/workflows/navigation.md` - Added `/plan` then `/code` workflow to selection guide
- `.opencode/QUICK-START.md` - Added "Plan Then Code" section and updated tips

### Design Decisions

- The `/code` command routes to `epcv-orchestrator` (same as `/plan` and `/epcv`) since it needs to coordinate the Code → Verify → Commit loop
- Command checks for existing plan context and provides guidance if none exists
- Supports both same-session continuation and cross-session resumption with context provided as arguments

### Verification

- All modified files pass markdown linting (`npm run lint:md`)
<!-- SECTION:NOTES:END -->
