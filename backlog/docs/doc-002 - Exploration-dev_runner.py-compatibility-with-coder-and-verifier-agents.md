---
id: doc-002
title: "Exploration: dev_runner.py compatibility with coder and verifier agents"
type: other
created_date: "2026-03-17 21:14"
---

## Exploration Report

### Request Understanding

- **Intent**: Assess whether `dev_runner.py` will work correctly with the current coder and verifier agents
- **Type**: Exploration / compatibility analysis
- **Scope**: The runner script, the coder agent, the verifier agent, and the Backlog integration layer

### Files Found

| File                                      | Relevance | Role                                                                         |
| ----------------------------------------- | --------- | ---------------------------------------------------------------------------- |
| `.opencode/scripts/dev_runner.py`         | direct    | Automation runner — orchestrates implement/verify loop via OpenCode HTTP API |
| `.opencode/agent/coder.md`                | direct    | Coder agent definition — implements atomic tasks                             |
| `.opencode/agent/verifier.md`             | direct    | Verifier agent definition — validates implementations                        |
| `.opencode/opencode.json`                 | related   | MCP config — Backlog.md configured as MCP server                             |
| `.opencode/context/domain/agent-roles.md` | related   | Documents agent responsibilities and Backlog integration                     |
| `.opencode/ARCHITECTURE.md`               | related   | EPCV workflow architecture                                                   |

### Key Findings

#### 1. Backlog Integration Mismatch (CRITICAL)

The runner uses the **Backlog CLI** (`backlog task list`, `backlog task edit`, etc.) for all task management. The agents use **Backlog MCP tools** (`task_search`, `task_edit`, `task_list`, etc.) via the MCP server configured in `opencode.json`.

- **Runner** (lines 137-245): Calls `subprocess.run(["backlog", ...])` for listing tasks, getting details, setting status, adding acceptance criteria, and adding notes.
- **Agents**: Reference MCP tool names like `task_edit`, `task_search`, `task_view`, `acceptanceCriteriaCheck`, `definitionOfDoneCheck`, etc.

These are **two different interfaces to the same Backlog.md system**, so they should be compatible at the data level — both read/write the same markdown task files. However, the CLI must be installed separately (`npx backlog` or a global install).

#### 2. Verifier Prompt Conflict (MAJOR)

The runner's `build_verifier_prompt()` (lines 556-644) instructs the verifier to use **Backlog CLI commands** to update tasks:

```
backlog task edit {task.id} --check-ac 1 --check-ac 2 ...
backlog task edit {task.id} --check-dod 1 --check-dod 2 ...
backlog task edit {task.id} -s Done
backlog task edit {task.id} --final-summary "..."
```

But the **verifier agent** (verifier.md, lines 117-143) is trained to use **MCP tools**:

```
task_edit with acceptanceCriteriaCheck
task_edit with definitionOfDoneCheck
task_edit with finalSummary
task_edit with status "Done"
```

When the runner sends its prompt to the verifier via OpenCode API, the verifier will receive **two conflicting sets of instructions**: the runner's prompt says "use CLI commands" while the agent's system prompt says "use MCP tools". The agent will likely follow its system prompt (MCP tools), which is actually correct since it has MCP access. But the runner's prompt instructions about CLI commands will be confusing/ignored.

#### 3. Runner Also Updates Task Status (DUPLICATION)

The runner independently manages task status:

- `set_task_status(config, task.id, "In Progress")` — line 761
- `set_task_status(config, task.id, "Done")` — line 847
- `set_task_status(config, task.id, "Blocked")` — line 874

The **coder agent** also sets status to "In Progress" (Step 0 in coder.md), and the **verifier agent** sets status to "Done" on PASS (Step 9 in verifier.md). This creates a race condition / double-update scenario, though since both set the same values, it's benign.

#### 4. Coder Prompt vs Agent System Prompt (MODERATE)

The runner's `build_coder_prompt()` (lines 493-553) provides a generic "senior developer" system prompt. The coder agent already has a comprehensive system prompt in `coder.md`. When sent via the OpenCode API with `agent: "coder"`, the agent's system prompt is used, and the runner's prompt becomes the user message. This should work — the runner's prompt provides task-specific context while the agent's system prompt provides methodology. However:

- The runner's prompt doesn't include Backlog task IDs, so the coder agent's Step 0 ("Claim Task in Backlog") may fail to find the right task
- The runner's prompt doesn't include a do-not-touch list, task brief, or patterns — things the coder agent expects

#### 5. Verifier JSON Output Expectation (MODERATE)

The runner expects the verifier to output a specific JSON block (lines 631-643):

```json
{
  "passed": false,
  "new_criteria": [...],
  "feedback_for_developer": "..."
}
```

The verifier agent's own output format (verifier.md, lines 146-203) produces a structured text report with tables, not JSON. The runner's prompt explicitly requests JSON, which should override the agent's default format for the final output. But the verifier may produce its standard report format AND the JSON, or just the report. The `parse_verify_result()` function (lines 652-686) has fallback parsing, so it should handle most cases.

#### 6. Agent Parameter in API (WORKS)

The OpenCode API accepts an `agent` parameter in the message POST body (line 176 of server.mdx docs). The runner supports `--coder-agent` and `--verifier-agent` CLI flags. If these are set to "coder" and "verifier" respectively, the correct agent definitions will be loaded.

#### 7. No Git Revert Between Verify Failure and Retry (DESIGN ISSUE)

When verification fails, the runner does NOT revert changes before retrying (line 859-868). It only reverts on max retries exceeded (line 873). This means the coder's retry attempt starts with the previous (failed) changes still in place. This could be intentional (iterative fixing) but could also lead to accumulated cruft.

### Dependency Map

```
dev_runner.py
  → OpenCode HTTP API (session, message, diff, shell endpoints)
  → Backlog CLI (subprocess calls for task management)
  → git CLI (subprocess calls for commit/revert)

coder.md agent
  → Backlog MCP tools (task_search, task_edit, task_view)
  → OpenCode built-in tools (write, edit, bash, read, glob, grep)

verifier.md agent
  → Backlog MCP tools (task_edit, task_search)
  → OpenCode built-in tools (bash, read, glob, grep)
```

### Risks and Concerns

1. **Backlog CLI not installed** (HIGH): Runner requires `backlog` CLI binary; project only configures MCP via `npx backlog mcp start`
2. **Conflicting Backlog instructions** (MAJOR): Runner prompt tells verifier to use CLI; agent uses MCP tools
3. **Missing task context in coder prompt** (MODERATE): No Backlog task ID, no do-not-touch list, no task brief
4. **Verifier output format mismatch** (MODERATE): Runner expects JSON; agent produces structured text report
5. **Double status updates** (LOW): Both runner and agents update task status

### Context Summary

The `dev_runner.py` script is architecturally sound and will **mostly work** with the current agents, but has several integration friction points. The most critical issue is the Backlog integration mismatch: the runner uses CLI commands while agents use MCP tools. The runner's prompts also conflict with agent system prompts in places (especially the verifier's expected output format and Backlog update instructions). The coder prompt is missing context the agent expects (task IDs, do-not-touch list, task briefs). These issues won't cause hard failures but will reduce effectiveness — the verifier may not produce parseable JSON, the coder may not find its Backlog task, and Backlog updates may be duplicated or inconsistent.

### Open Questions

- Is the `backlog` CLI installed globally or only available via `npx`?
- Should the runner's prompts be updated to align with agent system prompts, or should the agents be updated?
- Should the runner delegate all Backlog updates to the agents (via MCP) and stop using CLI?
