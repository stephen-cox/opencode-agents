---
id: TASK-004
title: >-
  Update dev_runner.py to use coder agent for coding/commits and verifier agent
  for verification
status: Done
assignee: []
created_date: "2026-03-17 22:53"
updated_date: "2026-03-17 22:55"
labels: []
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->

Update the dev_runner.py automation script so that:

1. The coder agent is used by default (not optional) for coding sessions
2. The verifier agent is used by default (not optional) for verification sessions
3. Git commits are delegated to the coder agent instead of being done by the runner
4. The coder prompt instructs the agent to commit its work after implementation

## Context

Currently the runner:

- Has `coder_agent` and `verifier_agent` as optional CLI flags defaulting to None
- Does git commits itself via `git_commit()` after verification passes
- The coder agent never commits — the runner does it externally

The desired behavior:

- Default agent names to "coder" and "verifier" respectively
- Have the coder agent commit its own work as part of implementation
- Remove the runner's post-verification git commit step
- The runner should still handle git revert on failures and blocked tasks

## Scope

- Update Config defaults for coder_agent and verifier_agent
- Update CLI argument defaults
- Update build_coder_prompt() to instruct coder to commit
- Update run_task() to remove runner git commit after verification passes
- Keep git_revert() for failure/blocked cases
- Keep git_commit() function for potential fallback use

## Non-Goals

- Changing agent system prompts
- Changing core orchestration logic
- Modifying polling/session management
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria

<!-- AC:BEGIN -->

- [x] #1 Config.coder_agent defaults to "coder" instead of None
- [x] #2 Config.verifier_agent defaults to "verifier" instead of None
- [x] #3 CLI --coder-agent default is "coder"
- [x] #4 CLI --verifier-agent default is "verifier"
- [x] #5 Git commit process unchanged — runner still commits after verification passes
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->

### Files Modified

- `.opencode/scripts/dev_runner.py` — 2 edits

### Changes Made

1. **Config dataclass** (line 49-50): Changed `coder_agent: Optional[str] = None` → `coder_agent: str = "coder"` and `verifier_agent: Optional[str] = None` → `verifier_agent: str = "verifier"`
2. **CLI arguments** (lines 1054-1063): Added `default="coder"` to `--coder-agent` and `default="verifier"` to `--verifier-agent`, updated help text to show defaults

### Deviations from Original Task Spec

- Git commit process left unchanged per user instruction — runner still commits after verification passes
- build_coder_prompt() and run_task() not modified (git delegation cancelled)
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

Updated dev_runner.py to default to using the \"coder\" agent for coding sessions and the \"verifier\" agent for verification sessions. Previously these were None (no agent), requiring explicit CLI flags. Git commit process unchanged — runner still commits after verification passes.

<!-- SECTION:FINAL_SUMMARY:END -->
