---
description: Design a solution with atomic task specifications
agent: planner
---

# Plan Command

Design a solution and produce atomic task specifications for the following request:

$ARGUMENTS

Follow these steps:

1. Review any exploration report from a prior `/explore` run (if available in conversation context)
2. If no exploration has been done, perform a quick codebase investigation to gather context
3. Design the optimal solution approach with rationale
4. Break work into phases (milestones) for moderate/complex tasks
5. Produce atomic task specifications for the current phase, each with: scope, non-goals, acceptance criteria, definition of done, automated tests, manual test steps, rollback note, risk level
6. Produce task briefs for the Coder (scope, constraints, files, assumptions, patterns)
7. Define the do-not-touch list and dependency guardrails
8. Present the full plan for human review

Do NOT proceed to implementation. Stop after presenting the plan.
