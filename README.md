# Open Code agent for Explore → Plan → Code → Verify workflow

A disciplined, iterative workflow system for AI-assisted software development that ensures quality while maintaining developer control.

## Overview

The EPCV (Explore → Plan → Code → Verify) system enforces a structured approach to coding tasks:

1. **Explore** - Understand the codebase before making changes
2. **Plan** - Design solutions and break work into atomic tasks
3. **Code** - Implement each task precisely
4. **Verify** - Validate through four-layered checks

```mermaid
flowchart TB
    A(["Bug, feature or project"]) --> B["**Explore**"]
    B --> C["Accepted solution"]
    C --> D["**Plan**"]
    D --> E1["Phase breakdown
    (for larger pieces of work)"]
    E1 --> E2["Task specification
    (for current phase)"]
    E2 --> F["**Code**"]
    F --> G["Code changes"]
    G --> H["**Verify**"]
    H --> I{"Acceptance
    criteria met?"}
    I -- No --> F
    I -- Yes --> J["Commit changes"]
    J --> K{"Are there
    more tasks?"}
    K -- No --> L{"Are there
    more phases?"}
    K -- Yes --> F
    L -- No --> M(["Complete"])
    L -- Yes --> D

    C@{ shape: lean-r}
    E1@{ shape: lean-r}
    E2@{ shape: lean-r}
    G@{ shape: lean-r}
    J@{ shape: trap-t}
```

## Key Features

- **Human-in-the-loop**: Two mandatory approval gates ensure developer control
- **Iterative workflow**: Task loops and phase loops handle projects of any size
- **Atomic tasks**: Small, independently verifiable units of work
- **Four-layer verification**: Automated, behavioural, operational, and security checks
- **Bug-fixing loop escape**: Prevents wasted effort on repeated patch attempts

## Inspiration

This system was inspired by [OpenAgentsControl](https://github.com/darrenhinde/OpenAgentsControl) and builds upon its principles of structured AI-assisted development.

## Documentation

- [AGENTS.md](AGENTS.md) - Comprehensive guidelines for agentic coding agents
- [ARCHITECTURE.md](.opencode/ARCHITECTURE.md) - System design and component relationships
- [QUICK-START.md](.opencode/QUICK-START.md) - Get started in 5 minutes
- [TESTING.md](.opencode/TESTING.md) - Validation checklist and testing approach

## Development

### Markdown Linting

This project uses [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) for markdown linting:

```bash
# Install
npm install -g markdownlint-cli2

# Run linting
markdownlint-cli2 "**/*.md"

# Fix issues
markdownlint-cli2 "**/*.md" --fix
```

## License

[MIT License](LICENSE)
