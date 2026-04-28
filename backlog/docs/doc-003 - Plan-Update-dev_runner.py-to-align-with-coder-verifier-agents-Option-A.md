---
id: doc-003
title: "Plan: Update dev_runner.py to align with coder/verifier agents (Option A)"
type: other
created_date: "2026-03-17 21:21"
---

## Implementation Plan — Option A

### Solution Design

**Approach**: Update `dev_runner.py` prompts and logic to align with the agents' existing MCP-based workflow. Remove CLI command instructions, delegate Backlog updates to agents, and provide the context agents expect.

**Rationale**: The agents already have comprehensive system prompts and MCP tool access. The runner should provide task-specific context and let agents handle their own Backlog updates using their preferred tools. This eliminates conflicting instructions and leverages the agents' existing capabilities.

**Alternatives Considered**:

- Option B (update agents): Would require rewriting agent system prompts and removing MCP integration, breaking the existing human-driven workflow
- Hybrid (runner uses MCP too): Would require adding MCP client to Python, adding complexity

---

### Changes Required

#### 1. Update `build_coder_prompt()` (lines 493-553)

**Current issues**:

- No Backlog task ID provided
- No do-not-touch list
- No task brief with patterns/constraints
- Generic "senior developer" framing duplicates agent system prompt

**Changes needed**:

```python
def build_coder_prompt(
    task: Task,
    extra_criteria: list[str],
    feedback: str = "",
    do_not_touch: list[str] = None,  # NEW
    patterns: str = "",  # NEW
) -> str:
```

Add to prompt:

- `## Backlog Task ID\n{task.id}` (so agent can claim it)
- `## Do-Not-Touch List\n{do_not_touch}` (for guardrail checks)
- `## Patterns to Follow\n{patterns}` (from exploration/plan)
- Remove generic "senior developer" intro (agent has this)
- Add explicit instruction: "Use Backlog MCP tools to claim this task (set status to In Progress) and record implementation notes when done"

#### 2. Update `build_verifier_prompt()` (lines 556-644)

**Current issues**:

- Lines 618-626: Instructs verifier to use CLI commands (`backlog task edit {task.id} --check-ac 1`)
- Conflicts with verifier agent's MCP tool usage
- JSON output request is buried mid-prompt

**Changes needed**:

**Remove** (lines 618-628):

```python
## Updating the Backlog Task
If verification PASSES, you MUST update the backlog task before returning:
1. Check off every passing acceptance criterion (1-based index):
   `backlog task edit {task.id} --check-ac 1 --check-ac 2 ...`
2. Check off every passing definition of done item (1-based index):
   `backlog task edit {task.id} --check-dod 1 --check-dod 2 ...`
3. Set the task status to Done:
   `backlog task edit {task.id} -s Done`
4. Add a final summary describing what was implemented and verified:
   `backlog task edit {task.id} --final-summary "Brief summary of implementation and verification"`

If verification FAILS, do NOT update the task — the runner will handle retries.
```

**Replace with**:

```python
## Updating the Backlog Task
Use Backlog MCP tools to update the task based on verification results:
- On PASS: Check acceptance criteria, check definition of done items, write final summary, set status to Done
- On FAIL: Append failure details to notes, leave status as In Progress

Follow your standard verification workflow (Step 9 in your system prompt).
```

**Move JSON requirement to end** and make it more prominent:

````python
## Output Format
You MUST end your response with a JSON code block in EXACTLY this format:

```json
{
  "passed": true,  // or false
  "new_criteria": ["criterion 1", "criterion 2"],  // empty array if none
  "feedback_for_developer": "Detailed feedback here"
}
````

This JSON block is required for the automation runner to parse your verdict.

````

#### 3. Remove Runner's Backlog Status Updates

**Current behavior**: Runner sets status via CLI at lines 761, 847, 874

**Changes needed**:
- **Line 761**: Remove `set_task_status(config, task.id, "In Progress")` — coder agent does this
- **Line 847**: Remove `set_task_status(config, task.id, "Done")` — verifier agent does this
- **Line 874**: Keep `set_task_status(config, task.id, "Blocked")` — agents don't handle max retries case

Add comment explaining delegation:
```python
# Task status updates delegated to agents via MCP tools:
# - Coder sets "In Progress" when claiming task
# - Verifier sets "Done" on PASS
# - Runner only sets "Blocked" on max retries (agents don't handle this case)
````

#### 4. Remove `add_acceptance_criteria()` Call

**Current behavior**: Line 868 adds new criteria via CLI when verifier identifies gaps

**Changes needed**:

- Remove `add_acceptance_criteria(config, task.id, verify.new_criteria)` — verifier agent already added them via MCP
- Keep `new_criteria.extend(verify.new_criteria)` for tracking in the retry loop

#### 5. Update `get_task_details()` to Include Plan/Notes

**Current behavior**: Extracts description, acceptance criteria, definition of done, manual checks

**Changes needed**:
Add extraction for:

- `task.plan` — implementation plan/task brief (for coder)
- `task.do_not_touch` — extracted from plan or description
- `task.patterns` — patterns to follow (from plan)

These fields need to be added to the `Task` dataclass and extracted from the Backlog task's plan section.

#### 6. Pass Context to Coder Prompt

**Current behavior**: `build_coder_prompt(task, new_criteria, feedback)` — line 777

**Changes needed**:

```python
prompt = build_coder_prompt(
    task,
    new_criteria,
    feedback,
    do_not_touch=task.do_not_touch,  # NEW
    patterns=task.patterns,  # NEW
)
```

#### 7. Update Task Dataclass

**Current definition** (lines 90-97):

```python
@dataclass
class Task:
    id: str
    slug: str
    title: str
    description: str = ""
    acceptance_criteria: list[str] = field(default_factory=list)
    definition_of_done: list[str] = field(default_factory=list)
    manual_checks: list[str] = field(default_factory=list)
```

**Add fields**:

```python
@dataclass
class Task:
    id: str
    slug: str
    title: str
    description: str = ""
    acceptance_criteria: list[str] = field(default_factory=list)
    definition_of_done: list[str] = field(default_factory=list)
    manual_checks: list[str] = field(default_factory=list)
    plan: str = ""  # NEW - task brief for coder
    do_not_touch: list[str] = field(default_factory=list)  # NEW
    patterns: str = ""  # NEW - patterns to follow
```

#### 8. Improve JSON Parsing Robustness

**Current behavior**: `parse_verify_result()` has fallback parsing but could be more robust

**Changes needed**:

- Add logging when JSON parsing fails
- Consider accepting the verifier's native report format as an alternative (parse "Status: PASS/FAIL" from the structured report)
- Add a fallback that looks for "PASS" or "FAIL" in the response text if JSON parsing completely fails

---

### Testing Strategy

After changes:

1. **Unit test**: Mock OpenCode API responses, verify prompts contain expected sections
2. **Integration test**: Run against a test milestone with 1-2 simple tasks
3. **Verify**: Check that agents successfully claim tasks, update Backlog via MCP, and produce parseable output

---

### Rollback Plan

If changes break the runner:

- Git revert the commit
- The runner's CLI-based Backlog updates still work independently
- Agents continue to work in human-driven workflow (unaffected)

---

### Summary of Changes

| File            | Lines   | Change                                                     | Reason                                                   |
| --------------- | ------- | ---------------------------------------------------------- | -------------------------------------------------------- |
| `dev_runner.py` | 90-97   | Add `plan`, `do_not_touch`, `patterns` to Task dataclass   | Provide context agents expect                            |
| `dev_runner.py` | 189-216 | Extract plan/do-not-touch/patterns in `get_task_details()` | Populate new Task fields                                 |
| `dev_runner.py` | 493-553 | Update `build_coder_prompt()` signature and body           | Add task ID, do-not-touch, patterns; remove duplication  |
| `dev_runner.py` | 556-644 | Update `build_verifier_prompt()`                           | Remove CLI instructions, delegate to MCP, emphasize JSON |
| `dev_runner.py` | 761     | Remove `set_task_status(..., "In Progress")`               | Coder agent handles this                                 |
| `dev_runner.py` | 847     | Remove `set_task_status(..., "Done")`                      | Verifier agent handles this                              |
| `dev_runner.py` | 868     | Remove `add_acceptance_criteria()` call                    | Verifier agent already added via MCP                     |
| `dev_runner.py` | 777     | Pass `do_not_touch` and `patterns` to coder prompt         | Provide expected context                                 |
| `dev_runner.py` | 652-686 | Improve `parse_verify_result()` logging/fallbacks          | Better error handling                                    |

---

### Risk Level: Low

- Changes are isolated to prompt generation and task status management
- No changes to core orchestration logic (session creation, polling, diff retrieval, git operations)
- Agents already work correctly with MCP tools in human-driven workflow
- Worst case: agents ignore runner's prompts and follow their system prompts (current behavior)
