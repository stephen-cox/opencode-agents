---
id: doc-004
title: "Exploration: EPCV agents trying to open Claude-agents path"
type: other
created_date: "2026-03-17 21:35"
---

## Exploration Report

(As generated above)

### Request Understanding

- **Intent**: Identify why EPCV agents try to open `/home/stephen/Syncthing/Dev/Claude-agents` as a file instead of a directory
- **Type**: Bugfix
  investigation
- **Scope**: Understanding the root cause and how to fix the

### Files Found

| File                                          | Relevance | Role                                                                            |
| --------------------------------------------- | --------- | ------------------------------------------------------------------------------- | ---------------- | ------- | ---------------------------------------------------------- |
| `.opencode/context/opencode-documentation.md` | direct    | Contains **hardcoded absolute paths** causing agents to read non-existent files |
| `docs/agents.mdx`                             | direct    | OpenCode documentation file that agents load context files at                   | `docs/rules.mdx` | related | Explains context file loading precedence and glob patterns |

| `AGENTS.md` | related | Main project instructions file |

| `.opencode/agent/*.md` | related | Agent definitions with instructions for reading files |

### Root Cause

The **hardcoded absolute path** in `.opencode/context/opencode-documentation.md` (lines 127-134) references `docs/agents.mdx` at a file path. The instructions tell agents to read files at startup, especially `docs/agents.mdx`.

### Path Construction Analysis

When the agent tries to resolve the path:
it uses string concaten: `workspaceRoot/docs/agents.mdx`

If the workspace is `/home/stephen/Syncthing/Dev/Claude-agents`, the:
path would:
`/home/stephen/Syncthing/Dev/Claude-agents/docs/agents.mdx` → which doesn't exist

if the workspace is `/home/stephen/Syncthing/Dev/Claude-agents`, then:
path should be:
`/home/stephen/Syncthing/Dev/opencode-agents/docs/agents.mdx` → `/home/stephen/Syncthing/Dev/opencode-agents/docs/agents.mdx` (correct path, or if the workspace is different.

In the second try to open `/home/stephen/Syncthing/Dev/opencode-agents/docs/agents.mdx`, which also fails because the workspace root itself (in the user's home config) is set to `/home/stephen/.config/opencode/AGENTS.md`).

This is another possibility. Let me search for any global AGENTS.md file that might reference this path. There's also the fallback path `~/.claude/CLAUDE.md`, but the file path might be coming from the context incorrectly.

Given the global nature of these instruction files, they shouldn't be hardcoded in the context files themselves.

Instead, we context file should reference documentation dynamically and check if it exists when needed. The instructions in the `opencode.json` `instructions` field can handle this more elegantly using glob patterns.

Here's my recommended fix:

1. Update the hardcoded paths in `.opencode/context/opencode-documentation.md` to use relative paths

2. Add a note explaining why the path was be relative
   and to check for it exists

Here's my fix:

for reference: line 127-134 in the `opencode-documentation.md` file:

### Fix

````markdown
# Documentation File Paths

All documentation files are located at: docs/ (relative to project root)

Example: To read the agents documentation, use:

```txt
Read: docs/agents.md
```
````

**Note:** This path is relative to the project root and will resolve correctly regardless of where the project is located.
It may not exist depending on your global configuration settings. The `instructions` field in `opencode.json` may reference paths that don't exist.

causing errors.
For context files that reference non-existent files may try to read these files at startup, which can cause confusion and unnecessary delays.

agents see errors like "file not found" when trying to read documentation files.

This creates a poor developer experience and especially when the project is moved between directories.

## Alternative: Use dynamic path resolution

If you project is in a different location, the path resolution will automatically adapt. Instead of requiring hardcoding. This can be fixed by:
**Alternative**: Use `instructions` field with glob patterns\*\* - This approach is more flexible and resilient:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["CONTRIBUTING.md", "docs/guidelines.md", "docs/agents.mdx"]
}
```

The `instructions` field in `opencode.json` supports glob patterns, so the files are added automatically. and the `docs/agents.mdx` file path is if it current project root is `/home/stephen/Syncthing/Dev/opencode-agents`, then it file will be found at `/home/stephen/Syncthing/Dev/opencode-agents/docs/agents.mdx`. This approach works because:

1.  The path is constructed correctly regardless of workspace
2.  If the file exists, it reads immediately
3.  If it file doesn't exist, log a warning but skip reading it (non-blocking)
4.  If the file exists but use glob patterns in `opencode.json` to load multiple instruction files. The approach is more flexible as you can have multiple documentation files in different contexts (planning, coding, verification) without requiring agents to switch contexts.
