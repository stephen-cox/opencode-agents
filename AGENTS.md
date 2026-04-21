# EPCV Agent Guidelines

This project uses the Explore → Plan → Code → Verify (EPCV) workflow: disciplined, iterative, human-in-the-loop at two gates (post-Explore, post-Plan).

## Core Principles

1. **Explore before acting** — never change what you don't understand
2. **Plan before coding** — design decisions belong in the plan
3. **Follow existing patterns** — consistency over theoretical perfection
4. **Verify everything** — never deliver unverified work
5. **Human in the loop** — two mandatory approval gates
6. **Fail fast** — surface blockers immediately
7. **Transparency** — document decisions, deviations, and findings

## Where the rules live

Authoritative workflow rules — process steps, output formats, hard gates, anti-patterns, report templates — live in the skills, loaded on demand:

- `exploring-ideas` (Phase 1)
- `writing-plans` (Phase 2)
- `implementing-tasks` (Phase 3)
- `verifying-changes` (Phase 4)
- `tracking-work-in-backlog` (cross-session persistence)

Agent files in `.opencode/agent/` configure tool access and hand off to the matching skill. Commands in `.opencode/command/` are thin wrappers over the agents (`/explore`, `/plan`, `/code`, `/verify`, `/epcv`, `/commit-task`). For single-conversation use, the `GeneralCoder` agent runs all four phases inline.

## Build/Lint/Test Commands

- `npm run lint:md` — check markdown style
- `npm run lint:md:fix` — auto-fix markdown style
- `npm run test:md` — test markdown formatting

<!-- BACKLOG.MD MCP GUIDELINES START -->

<CRITICAL_INSTRUCTION>

## BACKLOG WORKFLOW INSTRUCTIONS

This project uses Backlog.md MCP for all task and project management activities.

### Critical Guidance

- If your client supports MCP resources, read `backlog://workflow/overview` to understand when and how to use Backlog for this project.
- If your client only supports tools or the above request fails, call `backlog.get_workflow_overview()` tool to load the tool-oriented overview (it lists the matching guide tools).

- **First time working here?** Read the overview resource IMMEDIATELY to learn the workflow
- **Already familiar?** You should have the overview cached ("## Backlog.md Overview (MCP)")
- **When to read it**: BEFORE creating tasks, or when you're unsure whether to track work

These guides cover:

- Decision framework for when to create tasks
- Search-first workflow to avoid duplicates
- Links to detailed guides for task creation, execution, and finalization
- MCP tools reference

You MUST read the overview resource to understand the complete workflow. The information is NOT summarized here.

</CRITICAL_INSTRUCTION>

<!-- BACKLOG.MD MCP GUIDELINES END -->
