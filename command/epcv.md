---
description: Run the full Explore → Plan → Code → Verify workflow
agent: epcv-orchestrator
---

Run the full EPCV workflow for the following request:

$ARGUMENTS

Follow the complete iterative workflow:
1. Classify the request complexity (simple / moderate / complex)
2. Run @explorer to investigate the codebase
3. Present exploration findings and get human approval on solution direction
4. Run @planner to produce phases and atomic task specifications
5. Present the plan and get human approval before coding
6. For each task: run @coder to implement, then @verifier to validate, then commit
7. Loop through remaining tasks and phases
8. Deliver a complete summary with all changes
