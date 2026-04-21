---
id: TASK-003
title: Update dev_runner.py to align with coder/verifier agent MCP workflow
status: Done
assignee: []
created_date: "2026-03-17 21:24"
updated_date: "2026-03-17 21:36"
labels: []
dependencies: []
references:
  - doc-002
  - doc-003
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->

Update the dev_runner.py automation script to work seamlessly with the current coder and verifier agents by aligning prompts with agent system prompts, delegating Backlog updates to agents via MCP tools, and providing the context agents expect.

## Context

The runner currently uses Backlog CLI commands and provides prompts that conflict with the agents' MCP-based workflow. This causes:

- Conflicting instructions (runner says "use CLI", agents use MCP)
- Missing context (no task IDs, do-not-touch lists, or patterns)
- Redundant status updates (both runner and agents update the same fields)
- Potential JSON parsing failures (verifier may not produce expected format)

## Scope

Update `dev_runner.py` to:

1. Add new fields to Task dataclass (plan, do_not_touch, patterns)
2. Extract these fields from Backlog tasks
3. Update coder prompt to include task ID, do-not-touch list, and patterns
4. Update verifier prompt to delegate Backlog updates to MCP tools and emphasize JSON output
5. Remove redundant status updates from runner (delegate to agents)
6. Remove redundant acceptance criteria additions (verifier handles via MCP)
7. Pass new context to coder prompt
8. Improve JSON parsing robustness

## Non-Goals

- Changing agent system prompts (they already work correctly)
- Adding MCP client to Python (keep using CLI for runner's own task queries)
- Changing core orchestration logic (session creation, polling, diff retrieval)
- Modifying git operations or retry logic
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria

<!-- AC:BEGIN -->

- [x] #1 Task dataclass has plan, do_not_touch, and patterns fields
- [x] #2 get_task_details() extracts plan, do_not_touch, and patterns from Backlog tasks
- [x] #3 build_coder_prompt() includes Backlog task ID section
- [x] #4 build_coder_prompt() includes Do-Not-Touch List section
- [x] #5 build_coder_prompt() includes Patterns to Follow section
- [x] #6 build_coder_prompt() instructs coder to use MCP tools to claim task
- [x] #7 build_verifier_prompt() removes CLI command instructions (lines 618-628)
- [x] #8 build_verifier_prompt() delegates Backlog updates to MCP tools
- [x] #9 build_verifier_prompt() emphasizes JSON output requirement at end of prompt
- [x] #10 Runner does not call set_task_status for In Progress (line 761 removed)
- [x] #11 Runner does not call set_task_status for Done (line 847 removed)
- [x] #12 Runner still calls set_task_status for Blocked (line 874 kept)
- [x] #13 Runner does not call add_acceptance_criteria (line 868 removed)
- [x] #14 build_coder_prompt call passes do_not_touch and patterns parameters
- [x] #15 parse_verify_result() logs when JSON parsing fails
- [x] #16 parse_verify_result() has fallback to parse Status: PASS/FAIL from structured report
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->

## Implementation Complete

### Files Modified

- `.opencode/scripts/dev_runner.py` (1099 → 1127 lines)

### Changes Made

1. **Task dataclass** (lines 89-100): Added `plan`, `do_not_touch`, `patterns` fields
2. **get_task_details()** (lines 219-221): Extract plan, do-not-touch, patterns from Backlog tasks
3. **build_coder_prompt()** (lines 503-577):
   - Added function parameters for do_not_touch and patterns
   - Added Backlog Task ID section
   - Added Do-Not-Touch List section
   - Added Patterns to Follow section
   - Added instruction to use MCP tools to claim task
   - Removed generic 'senior developer' intro
4. **build_verifier_prompt()** (lines 641-664):
   - Removed CLI command instructions (old lines 618-628)
   - Replaced with MCP delegation instructions
   - Moved JSON requirement to end with emphasis
5. **run_task()** (lines 799-803):
   - Removed set_task_status for 'In Progress' (line 781)
   - Removed set_task_status for 'Done' (line 870)
   - Kept set_task_status for 'Blocked' (line 920)
   - Added comment explaining delegation to agents
6. **run_task()** (line 890): Removed add_acceptance_criteria() call
7. **build_coder_prompt call** (lines 820-826): Pass do_not_touch and patterns parameters
8. **parse_verify_result()** (lines 672-719):
   - Added logging for JSON parsing failures
   - Added fallback to parse 'Status: PASS/FAIL' from structured report
   - Added final keyword fallback

### Key Decisions

- Kept function definitions for set_task_status and add_acceptance_criteria (used elsewhere)
- Used Optional[list[str]] type hint for do_not_touch parameter
- Extraction uses section headers: 'Implementation Plan', 'Do-Not-Touch', 'Patterns'
- Fallback parsing tries 3 methods: JSON block → raw JSON → structured report → keywords
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

## Verification Summary

Successfully updated dev_runner.py to align with coder/verifier agent MCP workflow. All 16 acceptance criteria verified and passing.

### Changes Implemented

- Task dataclass extended with plan, do_not_touch, patterns fields
- Extraction logic updated to populate new fields from Backlog tasks
- Coder prompt enhanced with task ID, do-not-touch list, patterns, and MCP instructions
- Verifier prompt updated to delegate Backlog updates to MCP tools with emphasized JSON output
- Redundant status updates removed (In Progress, Done) - delegated to agents
- Redundant add_acceptance_criteria call removed - delegated to verifier agent
- JSON parsing improved with logging and 3-tier fallback (JSON block → structured report → keywords)

### Verification Results

- **Layer 1 (Automated)**: PASS - Python syntax valid, imports successful, all functions intact
- **Layer 2 (Behavioural)**: PASS - Prompt generation tested with edge cases, fallback parsing verified
- **Layer 3 (Operational)**: PASS - Error handling preserved, logging enhanced, core orchestration unchanged
- **Layer 4 (Security)**: PASS - Input validation safe, no hardcoded secrets, no new dependencies

### Notes

- Comments mentioning --check-ac/--check-dod remain for context but actual CLI command instructions removed
- Manual testing (DoD #5) deferred - requires OpenCode server and test milestone setup
- Code follows existing style conventions and maintains backward compatibility
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done

<!-- DOD:BEGIN -->

- [x] #1 All acceptance criteria pass
- [x] #2 Code follows existing dev_runner.py style and conventions
- [x] #3 No changes to core orchestration logic (session, polling, diff, git)
- [x] #4 Comments added explaining delegation to agents
- [ ] #5 Manual test: runner works with test milestone containing 1-2 tasks
<!-- DOD:END -->
