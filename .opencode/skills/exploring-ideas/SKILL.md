---
name: exploring-ideas
description: "You MUST use this as Phase 1 of any EPCV workflow — before planning, before code, before any change. Turns a raw user request into a shared understanding of intent, constraints, landscape, and unknowns. Works for features, bugfixes, refactors, questions, and half-formed ideas alike."
---

# Exploring Ideas Into Understanding

Help turn a raw request into a shared understanding that Planning can act on. Uncover what the user actually wants, what constrains it, what already exists in the landscape, and what is still unknown — before anyone commits to an approach.

> **Hard Gate:** Do NOT propose an implementation plan, write code, create Backlog tasks for execution, or invoke any downstream skill until you have presented an exploration report and the user has approved it. Exploration is read-only: no edits, no mutations, no task creation beyond a single Backlog document capturing the findings.

## Anti-Pattern: "The Request Is Obvious"

Most wasted work comes from skipping this phase on requests that _seemed_ obvious. "Add a button", "fix this bug", "refactor that module" — each hides assumptions about intent, scope, and constraints that the user has not actually stated. The exploration can be short when the request really is simple, but you MUST produce findings and get approval before Planning begins.

## Checklist

Create a task for each item and complete in order:

1. **Restate the request** — in your own words, including what you believe is out of scope
2. **Surface the intent** — why does the user want this? what outcome are they measuring?
3. **Probe constraints** — deadlines, stakeholders, systems that must not change, prior decisions
4. **Investigate the landscape** — only the parts relevant to the request (see "Landscape investigation" below)
5. **Name the unknowns** — open questions, ambiguities, things you cannot determine without the user
6. **Assess risks** — what could go wrong, what has high blast radius, where is coupling dangerous
7. **Present findings** — structured report, scaled to complexity
8. **Persist findings** — if cross-session tracking is needed, follow the `tracking-work-in-backlog` skill (Exploration section); skip for inline single-agent workflows
9. **Hand off to Planning** — only after the user approves the findings

**The terminal state is handing off to Planning** (the EPCV `planner` agent or the `/plan` command). Do not invoke `coder`, `verifier`, or any implementation skill from here.

## The Process

### Restating the request

Put the request in your own words and say what you think is _out_ of scope. This is the cheapest way to surface misalignment. If the user corrects your restatement, that correction is already the most valuable output of the phase.

### Surfacing intent

Ask about the _why_ before the _what_. "What does success look like?" "Who benefits, and how will they notice?" "What are you trying to avoid?" A single good intent question often collapses three hours of design debate. Prefer multiple-choice or A/B phrasing when you can; one question per message.

### Probing constraints

Constraints are the shape of the solution space. Ask about:

- **Time** — is there a deadline, release window, or freeze?
- **People** — who else has a stake, who has to approve, who will maintain this?
- **Systems** — what must not change, what has recently changed, what is load-bearing?
- **Prior decisions** — ADRs, past attempts, explicit non-goals
- **Cost** — token budget, infra cost, review bandwidth

Do not assume the absence of a constraint means it does not exist. Ask.

### Landscape investigation

Investigate only as much as the request demands. This is where codebase search lives, but it is one tool among several:

- **Code** — glob/grep/read to find relevant files, patterns, dependents, tests
- **Docs** — READMEs, ADRs, Backlog documents, comments that encode past reasoning
- **History** — `git log` / `git blame` for why something is the way it is
- **External** — APIs, libraries, standards, prior art the request depends on

Scale by complexity:

- **Simple** — touch only what the request directly names; 1 level of dependents
- **Moderate** — related files and tests; 2 levels of dependents; note adjacent patterns
- **Complex** — the whole affected subsystem; full dependency graph; deep pattern analysis; prior-art review

Stop when further investigation would not change the plan. Over-investigation is a real failure mode; note what you chose not to explore and why.

### Naming unknowns

An unknown is anything a reasonable Planner would have to guess. Unknowns are _more_ valuable than answers at this stage — they are the agenda for the next round of questions. Do not paper over them with plausible-sounding defaults. If the user must decide, say so explicitly.

### Assessing risks

For each risk, name: what could break, how likely, how bad, who would notice. Favour concrete ("changing this signature breaks three call sites in `billing/`") over generic ("refactors are risky"). Flag anything security-sensitive, performance-sensitive, or observable to end users.

## Presenting Findings

Scale each section to its complexity — a sentence or two when the request is simple, up to a few paragraphs when it is not. Present in sections and pause for feedback after each:

- **Request understanding** — restatement, scope, non-goals
- **Intent** — what the user is actually trying to achieve
- **Constraints** — deadlines, stakeholders, immovable systems, prior decisions
- **Landscape** — relevant files / docs / systems, existing patterns, dependency map
- **Risks** — what could go wrong, severity, who would notice
- **Unknowns** — open questions requiring user input
- **Summary** — one tight paragraph the Planner can read cold

## After Approval

- **Persist findings (if tracking)** — when running as a specialized `explorer` agent or in a multi-session workflow, follow the `tracking-work-in-backlog` skill (Exploration section) to save the approved report. Skip persistence for inline single-agent workflows and say so explicitly in the hand-off.
- **Hand off** — tell the user exploration is complete and recommend invoking the Planner next (`/plan` or the `planner` agent). Do not invoke Planning yourself unless the user asks.

## Key Principles

- **One question at a time** — don't drown the user
- **Prefer multiple choice** — easier to answer, sharper signal
- **Intent before implementation** — never let the _how_ sneak in before the _why_ is settled
- **Unknowns are findings** — naming a gap is as valuable as filling one
- **Scale with complexity** — simple requests get a short report; don't pad, don't skip
- **Read-only** — no edits, no code, no planning decisions; this phase describes, it does not decide
- **Respect scope** — investigate what serves the request; resist adjacent rabbit holes and note what you chose not to chase
- **Transparency** — flag every assumption you had to make when the user did not answer
