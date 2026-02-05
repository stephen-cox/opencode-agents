---
id: TASK-1.8
title: Document retry count and file-patch tracking in orchestrator
status: To Do
assignee: []
created_date: "2026-02-05 21:39"
labels:
  - epcv
  - orchestrator
  - retry-policy
dependencies: []
references:
  - "`agent/epcv-orchestrator.md`"
  - "`.opencode/context/standards/validation-rules.md`"
  - "`.opencode/context/templates/common-patterns.md`"
parent_task_id: TASK-1
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->

The retry policy and bug-fixing loop escape are well-documented conceptually, but the orchestrator doesn't describe HOW it tracks:

1. Retry count per task (max 2 retries)
2. Same-file patch count (trigger escape if same file patched 3+ times for same issue)

In practice, an LLM-based orchestrator needs to maintain this state in its conversation context. The orchestrator should be instructed to explicitly track and check these counts before routing back to the Coder.

<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria

<!-- AC:BEGIN -->

- [ ] #1 Orchestrator instructions include guidance on tracking retry counts per task
- [ ] #2 Orchestrator instructions include guidance on tracking file-patch counts
- [ ] #3 Instructions specify to check counts before routing back to Coder
- [ ] #4 Example or template provided for how to maintain this state in conversation context
<!-- AC:END -->
