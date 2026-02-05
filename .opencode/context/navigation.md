# Context Files Navigation

## Organisation

Context files are organised into four categories, each serving a distinct purpose
in the EPCV system.

## Domain (`context/domain/`)

Core knowledge about the EPCV methodology and system design.

| File                  | Purpose                                                                                                                                                    | Used By      |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| `epcv-methodology.md` | Core philosophy, iterative workflow, four phases, atomic tasks, human gates, 4-layer verification, complexity levels, scaling, principles                  | All agents   |
| `agent-roles.md`      | Agent responsibilities (including task briefs, do-not-touch lists, 4-layer verification), iterative information flow with human gates and task/phase loops | Orchestrator |

## Processes (`context/processes/`)

Step-by-step procedures for executing workflows.

| File                           | Purpose                                                                                                                                     | Used By                |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| `epcv-workflow-process.md`     | 11-stage iterative workflow sequence with human gates, task/phase loops, commit step, quality gates, error handling, bug-fixing loop escape | Orchestrator           |
| `complexity-classification.md` | Classification criteria, decision tree, override rules                                                                                      | Orchestrator, Explorer |

## Standards (`context/standards/`)

Quality rules and validation criteria.

| File                  | Purpose                                                                                                                                          | Used By                |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------- |
| `quality-criteria.md` | Code quality standards, acceptance criteria compliance, definition of done compliance, 4-layer verification quality, minimum scores              | Verifier, Coder        |
| `validation-rules.md` | Phase transition gates (including human gates, commit gate, task/phase loop gates), retry rules with bug-fixing loop escape, escalation triggers | Orchestrator, Verifier |
| `error-handling.md`   | Error patterns per phase, retry with fix, bug-fixing loop escape, human gate rejection, user escalation, graceful degradation                    | All agents             |

## Templates (`context/templates/`)

Reusable output formats and common patterns.

| File                 | Purpose                                                                                                                                                                                             | Used By    |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `output-formats.md`  | Report templates: exploration, implementation plan, atomic task spec, task brief, implementation report, 4-layer verification report, EPCV summary                                                  | All agents |
| `common-patterns.md` | Routing, context passing, human gate, iterative loop, retry/bug-fixing escape, quality gate, atomic task, 4-layer verification, read-before-write, search, ordering, complexity adaptation patterns | All agents |
