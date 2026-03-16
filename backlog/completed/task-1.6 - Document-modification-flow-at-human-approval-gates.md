---
id: TASK-1.6
title: Document modification flow at human approval gates
status: Done
assignee: []
created_date: "2026-02-05 21:39"
updated_date: "2026-03-16 21:25"
labels:
  - epcv
  - documentation
  - human-gates
dependencies: []
references:
  - "`agent/epcv-orchestrator.md`"
  - "`.opencode/context/standards/error-handling.md`"
  - "`.opencode/workflows/epcv-standard.md`"
parent_task_id: TASK-1
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->

The human gates describe three outcomes: approve, request modifications, reject. But there's limited guidance on how "request modifications" works in practice.

**Questions to address:**

- Post-Explore modification: Does the orchestrator re-run Explorer with new constraints? Does it modify the findings itself?
- Post-Plan modification: Does it re-run Planner with feedback? Does it make specific adjustments to the plan?

The error-handling.md mentions "Return to Explore with user's feedback" but doesn't detail the mechanics.

<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria

<!-- AC:BEGIN -->

- [ ] #1 Orchestrator instructions describe how to handle 'request modifications' at each gate
- [ ] #2 Post-Explore modification flow documented (re-run Explorer vs adjust findings)
- [ ] #3 Post-Plan modification flow documented (re-run Planner vs adjust plan)
- [ ] #4 Error handling documentation updated with specific modification procedures
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

Resolved by removing the orchestrator agent. The modification flow at human approval gates is now straightforward: the human reviews output, decides to approve/reject/modify, and invokes the appropriate command. No orchestrator needs to handle re-routing. This is documented in the updated agent-roles.md and epcv-workflow-process.md.

<!-- SECTION:FINAL_SUMMARY:END -->
