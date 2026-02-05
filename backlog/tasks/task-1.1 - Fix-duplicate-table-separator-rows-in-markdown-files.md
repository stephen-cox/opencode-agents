---
id: TASK-1.1
title: Fix duplicate table separator rows in markdown files
status: To Do
assignee: []
created_date: "2026-02-05 21:38"
labels:
  - epcv
  - documentation
  - markdown
dependencies: []
references:
  - "`.opencode/navigation.md`"
  - "`.opencode/workflows/navigation.md`"
  - "`.opencode/context/navigation.md`"
  - "`.opencode/ARCHITECTURE.md`"
parent_task_id: TASK-1
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->

Multiple markdown files have tables with three separator rows instead of one, causing empty rows to render in markdown viewers.

**Affected files:**

- `.opencode/navigation.md`
- `.opencode/workflows/navigation.md`
- `.opencode/context/navigation.md`
- `.opencode/ARCHITECTURE.md`
- `.opencode/context/domain/epcv-methodology.md`
- `.opencode/context/processes/epcv-workflow-process.md`
- `.opencode/context/processes/complexity-classification.md`
- `.opencode/context/standards/quality-criteria.md`
- `.opencode/context/standards/validation-rules.md`
- `.opencode/context/standards/error-handling.md`

**Example of the issue:**

```markdown
| Header 1 | Header 2 |
| -------- | -------- | ----------- |
| -------- | -------- | ← duplicate |
| -------  | -------  | ← duplicate |
| data     | data     |
```

Each table should have exactly one separator row after the header row.

<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria

<!-- AC:BEGIN -->

- [ ] #1 All markdown tables have exactly one separator row after the header
- [ ] #2 No empty rows render when viewing tables in markdown viewers
- [ ] #3 Markdown linting passes (`npm run lint:md`)
<!-- AC:END -->
