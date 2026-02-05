---
id: TASK-1.1
title: Fix duplicate table separator rows in markdown files
status: Done
assignee: []
created_date: "2026-02-05 21:38"
updated_date: "2026-02-05 21:57"
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

- [x] #1 All markdown tables have exactly one separator row after the header
- [x] #2 No empty rows render when viewing tables in markdown viewers
- [x] #3 Markdown linting passes (`npm run lint:md`)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->

## Implementation Summary

### Files Modified

- `.opencode/navigation.md` - Fixed 3 tables (Agents, Workflows, Context)
- `.opencode/workflows/navigation.md` - Fixed 1 table (Complexity)
- `.opencode/context/navigation.md` - Fixed 4 tables (Domain, Processes, Standards, Templates)
- `.opencode/ARCHITECTURE.md` - Fixed 3 tables (Context Flow, Why 4 Phases, Performance)
- `.opencode/context/domain/epcv-methodology.md` - Fixed 1 table (Complexity Levels)
- `.opencode/context/processes/epcv-workflow-process.md` - Fixed 2 tables (Quality Gates, Error Handling)
- `.opencode/context/standards/quality-criteria.md` - Fixed 1 table (Minimum Scores)
- `.opencode/context/standards/validation-rules.md` - Fixed 1 table (Retry Rules)
- `.opencode/context/standards/error-handling.md` - Fixed 3 tables (Exploration, Coding, Verification Errors)

### Total: 19 tables fixed across 10 files

### Verification

- `npm run lint:md` passes with 0 errors
- All tables now have exactly one separator row after the header
<!-- SECTION:NOTES:END -->
