---
id: doc-001
title: >-
  Exploration: Install and Update Process for EPCV Agent System (OpenCode
  Plugin)
type: other
created_date: "2026-03-16 22:25"
updated_date: "2026-03-16 22:29"
---

## Exploration Report — Revised after OpenCode Plugin Docs Review

### Request Understanding

- **Intent**: Create an install and update mechanism for the EPCV agent system, targeting OpenCode only
- **Type**: Feature / architecture design
- **Scope**: Distribution via OpenCode's native plugin/config system. AGENTS.md is NOT needed for install — only `.opencode/` contents. backlog.md is a required dependency.
- **Out of scope**: Multi-tool support (Claude Code, Cursor, etc.)

### Key Finding: OpenCode Has Two Distribution Paths

After reviewing the OpenCode docs, there are two distinct mechanisms:

1. **Plugin system** (npm packages, `opencode.json` `plugin` array) — for JS/TS code that hooks into events, adds custom tools, etc.
2. **Config directory** (`.opencode/` or `~/.config/opencode/`) — for agents, commands, workflows, context files (all markdown)

The EPCV system is **primarily content** (markdown agents, commands, workflows, context). It is NOT a plugin in the OpenCode sense (no JS/TS hooks, no event subscriptions). However, it does need:

- MCP config in `opencode.json` (for backlog.md)
- A `package.json` dependency (`@opencode-ai/plugin`, `backlog.md`)

### Precedent: Agentic CLI

The `agentic-cli` project (393 stars, listed in OpenCode ecosystem) solves the exact same problem with a CLI `pull` command:

- `agentic pull` — copies agents/commands into local `.opencode/`
- `agentic pull -g` — copies into global `~/.config/opencode/`
- Published to npm as `agentic-cli`
- Uses a TypeScript CLI with Bun

### Recommended Approach: npm CLI with `pull` command

Create an npm package (e.g. `opencode-epcv`) that:

1. **Bundles** all `.opencode/` content as static assets in the package
2. **Provides a CLI** with `init`/`pull` and `update` commands
3. **Copies files** into the target `.opencode/` or `~/.config/opencode/` directory
4. **Merges `opencode.json`** to add MCP config for backlog.md without destroying existing config
5. **Tracks version** via a stamp file (`.opencode/.epcv-version`)

### What Gets Distributed

```txt
.opencode/
├── agents/              ← renamed from agent/ (OpenCode prefers plural)
│   ├── explorer.md
│   ├── planner.md
│   ├── coder.md
│   └── verifier.md
├── commands/            ← renamed from command/ (OpenCode prefers plural)
│   ├── explore.md
│   ├── plan.md
│   ├── code.md
│   ├── verify.md
│   ├── epcv.md
│   └── commit-epcv.md
├── workflows/
│   ├── epcv-standard.md
│   ├── explore-only.md
│   ├── verify-existing.md
│   └── navigation.md
├── context/
│   ├── navigation.md
│   ├── domain/*.md
│   ├── standards/*.md
│   ├── processes/*.md
│   └── templates/*.md
├── ARCHITECTURE.md
├── QUICK-START.md
└── TESTING.md
```

Plus merging into `opencode.json`:

```json
{
  "mcp": {
    "backlog": {
      "type": "local",
      "command": ["npx", "backlog", "mcp", "start"]
    }
  }
}
```

### Open Questions Resolved

1. ✅ OpenCode only — use npm CLI pattern (like agentic-cli)
2. ✅ No user customisation — simple overwrite on update
3. ✅ No AGENTS.md needed — only .opencode/ contents
4. ✅ backlog.md is a dependency — must be configured in MCP
