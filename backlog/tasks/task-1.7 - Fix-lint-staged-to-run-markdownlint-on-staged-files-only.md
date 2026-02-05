---
id: TASK-1.7
title: Fix lint-staged to run markdownlint on staged files only
status: To Do
assignee: []
created_date: "2026-02-05 21:39"
labels:
  - tooling
  - lint
  - pre-commit
dependencies: []
references:
  - "`package.json`"
  - "`.husky/pre-commit`"
parent_task_id: TASK-1
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->

The pre-commit hook runs `npm run test:md` (markdownlint on ALL files) AND `npx lint-staged` (Prettier on staged files only). This means markdownlint runs on all markdown files on every commit, which:

1. Could be slow in a large project
2. Could fail on files the committer didn't touch

**Current setup:**

- `.husky/pre-commit`: runs `npm run test:md` then `npx lint-staged`
- `package.json` lint-staged: only runs Prettier on `*.md`

**Suggested fix:**
Add markdownlint to lint-staged so it only checks staged files:

```json
"lint-staged": {
  "*.md": ["markdownlint-cli2", "prettier --write"]
}
```

Then remove `npm run test:md` from the pre-commit hook.

<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria

<!-- AC:BEGIN -->

- [ ] #1 lint-staged config includes markdownlint-cli2 for \*.md files
- [ ] #2 Pre-commit hook only runs lint-staged (not global markdownlint)
- [ ] #3 Committing a single file only lints that file, not all markdown files
- [ ] #4 Both markdownlint and prettier run on staged markdown files
<!-- AC:END -->
