---
id: TASK-1.2
title: Clarify orchestrator write/edit permissions are for commits only
status: To Do
assignee: []
created_date: "2026-02-05 21:38"
labels:
  - epcv
  - orchestrator
  - security
dependencies: []
references:
  - "`agent/epcv-orchestrator.md`"
  - "`AGENTS.md`"
  - "`.opencode/context/domain/agent-roles.md`"
parent_task_id: TASK-1
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->

The EPCV orchestrator has `write: true` and `edit: true` in its frontmatter, but AGENTS.md and agent-roles.md state the orchestrator "Does NOT: Write code." This creates a design inconsistency.

The write/edit permissions are likely needed for the commit stage (Stage 8), but without explicit guardrails, the orchestrator could bypass the Coder and write implementation code directly.

**Options to consider:**

1. Add explicit instructions in the orchestrator that write/edit tools are only for commit operations (staging files), not for writing implementation code
2. If OpenCode supports it, handle commits through bash (`git add`, `git commit`) without needing write/edit permissions
3. Document the rationale for why the orchestrator needs these permissions
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria

<!-- AC:BEGIN -->

- [ ] #1 Orchestrator instructions explicitly state write/edit tools are only for commit operations
- [ ] #2 Documentation explains why orchestrator has write/edit permissions
- [ ] #3 No ambiguity about when orchestrator can use write/edit vs when Coder should be invoked
<!-- AC:END -->
