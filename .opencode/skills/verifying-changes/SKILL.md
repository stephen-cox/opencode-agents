---
name: verifying-changes
description: "You MUST use this as Phase 4 of any EPCV workflow — after an implementation report is produced, before any change is delivered or committed. Validates an atomic task's implementation through four layered checks (automated, behavioural, operational, security) scaled by risk level, and produces a definitive PASS / PASS_WITH_WARNINGS / FAIL verdict with specific fix instructions."
---

# Verifying Changes Against The Plan

Validate that an implementation is correct, complete, and delivery-ready. Check the diff against the task specification, run the four verification layers, scale rigour to risk level, and produce a verdict precise enough that a Coder on FAIL knows exactly what to fix.

> **Hard Gate:** Do NOT edit code, refactor, or "fix" issues you find — verification is read-only aside from running checks. Do NOT commit, push, or deliver the change; delivery is a separate phase. Do NOT issue PASS if any critical check fails, regardless of how minor the remaining work "feels".

## Anti-Pattern: "Tests Pass, Ship It"

Green tests are one layer of four. Plenty of broken changes pass their tests — missing error handling, leaked secrets, silent scope creep, do-not-touch violations, acceptance criteria the tests do not cover. Work through every layer the risk level demands. Do not short-circuit because Layer 1 was clean.

## Anti-Pattern: "Close Enough"

A failing acceptance criterion is a FAIL, not a PASS_WITH_WARNINGS. Warnings are for issues that do not block delivery (style nits, non-critical edge cases, info-level suggestions). If the implementation does not meet the spec, the verdict is FAIL and the Coder gets fix instructions.

## Anti-Pattern: "I'll Just Fix This One Thing"

You are read-only. Even a one-line fix makes you the author of the change you are supposed to be judging, and erases the reviewer/implementer boundary the workflow depends on. Report the issue, hand it back, let the Coder fix it.

## Checklist

Create a task for each item and complete in order:

1. **Locate the work (if tracking)** — for cross-session workflows, follow the `tracking-work-in-backlog` skill to find the In Progress task the Coder left; for inline workflows, the implementation report is in the conversation
2. **Review the diff** — read every created/modified file; compare against the task spec
3. **Check guardrails** — do-not-touch list respected, no unplanned changes, no unauthorised dependencies
4. **Layer 1 — Automated** — tests, lint, types, build
5. **Layer 2 — Behavioural** — manual test steps, edge cases, failure paths
6. **Layer 3 — Operational** — error handling, logging, config, migrations, rollback
7. **Layer 4 — Security** — input validation, output encoding, authorisation, secrets, log hygiene, deps
8. **Check acceptance criteria** — item by item, with evidence
9. **Check definition of done** — item by item, with evidence
10. **Produce the verdict** — PASS / PASS_WITH_WARNINGS / FAIL with severity-classified issues
11. **Record the verdict (if tracking)** — follow the `tracking-work-in-backlog` skill (Verification section): on PASS mark criteria/DoD, write `finalSummary`, set Done; on FAIL uncheck failing criteria, append fix instructions, leave In Progress

**The terminal state is handing off to Delivery** (commit / PR / release — a separate phase). Verification never delivers, never commits, never marks acceptance criteria satisfied without evidence.

## The Process

### Reviewing the diff

Read every file the Coder created or modified. Compare each change line-by-line against the task specification and brief. You are looking for three things: that every planned change landed, that no unplanned change crept in, and that the do-not-touch list was respected. A diff that "looks right" is not verified — read it.

### Layer 1 — Automated checks

Run the project's automated gates: unit tests, integration tests, type check, lint, build. If a gate cannot be run (tooling missing, no test harness for this code), say so explicitly — do not silently skip. When tests cannot be executed directly, inspect the test files for correctness: do assertions match expected behaviour, is setup/teardown sound, are new paths actually covered.

### Layer 2 — Behavioural checks

Walk the manual test steps from the task spec. Then push past the happy path: boundary conditions, empty inputs, invalid inputs, failure modes. Verify user-facing messages and error surfaces. For UI work, exercise the feature in a browser — type checks and tests verify code correctness, not feature correctness.

### Layer 3 — Operational checks

Production-readiness concerns the tests usually miss:

- **Error handling** — errors caught, logged, surfaced appropriately
- **Logging** — key operations logged at appropriate levels
- **Metrics** — relevant signals emitted where the system depends on them
- **Configuration** — changes documented and correct across environments
- **Migrations** — schema changes correct, reversible, ordered safely
- **Rollback** — the procedure in the task spec actually works

### Layer 4 — Security checks

Non-negotiable regardless of task size:

- **Input validation** — every boundary input validated and sanitised
- **Output encoding** — outputs encoded to prevent injection
- **Authorisation** — access controls applied at every gate, not just the obvious ones
- **Secrets** — no hardcoded secrets, no secrets in logs, no secrets in errors
- **Log hygiene** — sensitive data excluded from logs, traces, telemetry
- **Dependency security** — new deps free of known vulnerabilities; no unauthorised deps

### Checking acceptance criteria and DoD

Go through the task's acceptance criteria item by item. Each one gets a pass/fail with evidence — the specific test, log line, manual step, or file fragment that proves it. Then do the same for the definition of done. A criterion with no evidence is not passed, it is unverified.

### Classifying findings by severity

- **Critical** (must fix) — behaviour that does not meet acceptance criteria, build/compile failures, test failures in critical paths, security vulnerabilities, data-loss risks, do-not-touch violations
- **Warning** (note, do not block) — style inconsistencies, missing edge-case handling on non-critical paths, functional-but-suboptimal implementations, missing documentation
- **Info** (future improvement) — refactor opportunities, performance ideas, extra coverage suggestions

### Producing the verdict

- **PASS** — all layers pass at the required rigour, all acceptance criteria met with evidence, DoD complete
- **PASS_WITH_WARNINGS** — all critical checks pass and all acceptance criteria met, but non-blocking warnings exist
- **FAIL** — any critical issue, any unmet acceptance criterion, any unverifiable DoD item; every FAIL carries specific fix instructions

## Verification Report

```text
## Verification Report — Task: {task title}

### Status: {PASS / PASS_WITH_WARNINGS / FAIL}
### Risk Level: {low / medium / high}

### Layer 1: Automated Checks
| Check | Result | Notes |
|-------|--------|-------|
| Unit tests | PASS/FAIL | {details} |
| Integration tests | PASS/FAIL/N/A | {details} |
| Type check | PASS/FAIL/N/A | {details} |
| Lint | PASS/FAIL/N/A | {details} |
| Build | PASS/FAIL/N/A | {details} |

### Layer 2: Behavioural Checks
| Manual Test Step | Result | Notes |
|------------------|--------|-------|
| {step from task spec} | PASS/FAIL | {details} |
- **Edge cases**: {pass/fail — details}
- **Failure paths**: {pass/fail — details}

### Layer 3: Operational Checks
- **Error handling**: {pass/fail — details}
- **Logging**: {pass/fail/n/a — details}
- **Metrics**: {pass/fail/n/a — details}
- **Configuration**: {pass/fail/n/a — details}
- **Migrations**: {pass/fail/n/a — details}
- **Rollback procedure**: {pass/fail — details}

### Layer 4: Security Checks
- **Input validation**: {pass/fail — details}
- **Output encoding**: {pass/fail — details}
- **Authorisation**: {pass/fail/n/a — details}
- **Secrets management**: {pass/fail — details}
- **Logging hygiene**: {pass/fail/n/a — details}
- **Dependency security**: {pass/fail/n/a — details}

### Acceptance Criteria
- [x] {criterion_1} — PASS: {evidence}
- [ ] {criterion_2} — FAIL: {reason}

### Definition of Done
- [x] {item_1} — Complete
- [ ] {item_2} — Incomplete: {reason}

### Issues Found
| # | Severity | Layer | Description | Fix Required |
|---|----------|-------|-------------|--------------|
| 1 | {critical/warning/info} | {1-4} | {description} | {yes/no} |

### Recommendations
- {suggestion_1}

### Fix Instructions (if FAIL)
{Specific, actionable instructions for the Coder to fix each critical issue}
```

## Risk-Scaled Rigour

Rigour scales with the task's risk level. Layers are never skipped — only the depth changes.

- **Low** — Layer 1 full; Layer 2 happy-path manual checks; Layer 3 minimal sanity check; Layer 4 basic scan (input validation, secrets)
- **Medium** — Layer 1 full; Layer 2 manual steps + edge cases; Layer 3 error handling, logging, config; Layer 4 all six checks
- **High** — Layer 1 full; Layer 2 all manual steps + edge cases + failure paths; Layer 3 all checks with explicit sign-off; Layer 4 all six checks with detailed evidence

## After the Verdict

- **Record the verdict (if tracking)** — follow the `tracking-work-in-backlog` skill (Verification section). On PASS/PASS_WITH_WARNINGS it walks you through checking criteria, writing the final summary, and setting Done. On FAIL it walks you through unchecking failing criteria, appending fix instructions, and leaving the task In Progress. Skip for inline single-agent workflows.
- **Hand off** — on PASS, recommend delivery (commit / PR). On FAIL, recommend invoking the Coder next with the fix instructions attached.

## Key Principles

- **Assume nothing** — verify everything; read every changed file; check every criterion
- **Be objective** — judge against the plan and requirements, not personal preference
- **Be specific** — name what is wrong, where, and exactly how to fix it
- **Severity matters** — do not fail on style nits; do not pass on critical misses
- **Actionable FAIL** — every FAIL carries fix instructions precise enough that the Coder does not have to guess
- **Layers are mandatory** — rigour scales with risk, but no layer is ever skipped
- **Read-only** — you verify, you do not fix; fixing is the Coder's job
- **Evidence or unverified** — a checkbox without evidence is not passed
