# Error Handling Patterns

## Phase-Level Error Handling

### Exploration Errors

| Error | Handling |
|-------|----------|
| No relevant files found | Report finding, surface at human approval gate |
| File read permission denied | Note in report, suggest alternative approach |
| Ambiguous search results | Document all candidates, flag as open question for user |
| Codebase too large to fully explore | Focus on directly mentioned areas, note limitations |

### Planning Errors

| Error | Handling |
|-------|----------|
| Conflicting requirements | Flag to user at plan approval gate |
| No viable approach found | Present constraints to user, ask for guidance |
| Missing information from Explorer | Request re-exploration of specific area |
| Circular dependencies in change order | Break cycle, document the approach |
| Task cannot be made atomic | Split further or document why it must be larger |

### Coding Errors

| Error | Handling |
|-------|----------|
| File not found (expected by plan) | Document deviation, check if path changed |
| Edit target not found in file | Re-read file, adjust edit to match current content |
| Pattern conflict discovered | Document in implementation notes, follow plan |
| Unexpected file state | Re-read, document finding, adapt if safe |
| Do-not-touch list violation detected | Revert the change, document the near-miss |

### Verification Errors

| Error | Handling |
|-------|----------|
| Test failure | Classify severity, include in report with layer |
| Build failure | Critical issue, FAIL with fix instructions |
| Missing test coverage | Warning unless critical path, note in report |
| Performance regression | Warning or critical depending on severity |
| Acceptance criteria not met | Critical issue, FAIL with specific fix instructions |
| Definition of done incomplete | FAIL if critical items, warning if minor items |

## Recovery Strategies

### Retry with Fix (per task)
When verification fails for an atomic task:
1. Verifier produces specific fix instructions referencing the failing acceptance criteria
2. Orchestrator routes back to Coder with fix instructions
3. Coder implements fixes (reads files again first, checks do-not-touch list)
4. Orchestrator routes back to Verifier
5. Maximum 2 retries per task before bug-fixing loop escape

### Bug-Fixing Loop Escape
When retries are exhausted or the same file is patched 3+ times for the same issue:
1. **Stop patching** — do not attempt another fix
2. **Return to Explore** — gather new evidence about the root cause
3. **Refine the hypothesis** — the original approach may be wrong
4. **Adjust the plan** — produce a new task specification based on new evidence
5. **Resume Code → Verify** with the revised approach
6. If the escape also fails, **escalate to user** with full context:
   - What was attempted (original approach + retries)
   - Why it failed (specific errors and patterns)
   - What new evidence was gathered
   - Suggested paths forward

### User Escalation
When automated recovery fails:
1. Compile full context (request, exploration, plan, changes, issues)
2. Present clear summary of what was attempted
3. Explain what went wrong and why
4. Suggest possible paths forward
5. Ask user for direction

### Human Gate Rejection
When the user rejects at an approval gate:
1. **Rejects solution direction** (post-Explore): Return to Explore with user's feedback, or modify the proposed direction per user input
2. **Rejects implementation plan** (post-Plan): Modify the plan per user direction, or return to Explore if the approach needs rethinking

### Graceful Degradation
When a phase partially succeeds:
1. Document what succeeded and what failed
2. Assess if partial results are useful
3. Present options to user:
   - Continue with partial results
   - Retry the failed portion
   - Abort and start over
