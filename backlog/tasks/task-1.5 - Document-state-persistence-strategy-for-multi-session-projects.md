---
id: TASK-1.5
title: Document state persistence strategy for multi-session projects
status: To Do
assignee: []
created_date: "2026-02-05 21:38"
labels:
  - epcv
  - state-management
  - resilience
dependencies: []
references:
  - "`agent/epcv-orchestrator.md`"
  - "`.opencode/workflows/epcv-standard.md`"
  - "`.opencode/ARCHITECTURE.md`"
parent_task_id: TASK-1
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->

The EPCV system doesn't describe how state is persisted between sessions. If a complex multi-phase project is interrupted (user closes the terminal, session times out), there's no mechanism to resume from where it left off. The phase loop and task loop assume continuous execution.

**Considerations:**

- Git commit history could serve as checkpoints for completed tasks
- A state file (e.g., `.opencode/state/current-session.md`) could track which phase/task is active
- The orchestrator could be instructed to check for and resume interrupted sessions

This may be a documentation-only change (explaining the current implicit strategy) or could involve adding actual state persistence.

<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria

<!-- AC:BEGIN -->

- [ ] #1 Documentation explains how to resume interrupted EPCV workflows
- [ ] #2 Strategy documented for what serves as checkpoints (git commits, state files, or both)
- [ ] #3 Orchestrator instructions include guidance on detecting and resuming interrupted work
<!-- AC:END -->
