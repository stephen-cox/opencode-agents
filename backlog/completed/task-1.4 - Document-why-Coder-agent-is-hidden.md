---
id: TASK-1.4
title: Document why Coder agent is hidden
status: Done
assignee: []
created_date: "2026-02-05 21:38"
updated_date: "2026-03-16 21:25"
labels:
  - epcv
  - documentation
  - coder
dependencies: []
references:
  - "`agent/subagents/coder.md`"
  - "`.opencode/ARCHITECTURE.md`"
parent_task_id: TASK-1
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->

The Coder agent is the only subagent marked `hidden: true` in its frontmatter. This presumably prevents direct user invocation, ensuring the Coder is only used within the EPCV workflow after proper exploration and planning.

ARCHITECTURE.md mentions the Coder is hidden but doesn't explain the rationale. This should be documented for clarity.

<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria

<!-- AC:BEGIN -->

- [ ] #1 ARCHITECTURE.md explains that `hidden: true` prevents direct user invocation
- [ ] #2 Rationale documented: Coder should only be invoked by orchestrator after exploration and planning
- [ ] #3 Agent format section in ARCHITECTURE.md mentions hidden as an option with explanation
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

Resolved by removing the orchestrator agent and unhiding the coder. The coder was hidden because it was meant to be invoked only by the orchestrator. With the orchestrator removed, the coder is now a primary agent invoked directly via /code command, so hidden: true has been removed.

<!-- SECTION:FINAL_SUMMARY:END -->
