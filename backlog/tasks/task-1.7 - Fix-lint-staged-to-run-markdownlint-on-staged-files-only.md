---
id: TASK-1.7
title: Fix lint-staged to run markdownlint on staged files only
status: Done
assignee: []
created_date: "2026-02-05 21:39"
updated_date: "2026-02-05 22:28"
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

- [x] #1 lint-staged config includes markdownlint-cli2 for \*.md files
- [x] #2 Pre-commit hook only runs lint-staged (not global markdownlint)
- [x] #3 Committing a single file only lints that file, not all markdown files
- [x] #4 Both markdownlint and prettier run on staged markdown files
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->

## Implementation Summary

### Files Modified

- `package.json` — Updated lint-staged config to run `markdownlint-cli2` then `prettier --write` on `*.md` files
- `.husky/pre-commit` — Removed `npm run test:md`, now only runs `npx lint-staged`

### Changes

- Before: Pre-commit ran markdownlint on ALL files, then lint-staged ran prettier on staged files
- After: Pre-commit only runs lint-staged, which runs both markdownlint and prettier on staged files only

### Verification

- Committing will test the new setup automatically

<!-- SECTION:NOTES:END -->
