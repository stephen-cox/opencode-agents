# OpenCode Documentation Reference

The `docs/` folder contains comprehensive OpenCode documentation in MDX format. This reference guide helps agents locate the right documentation for their tasks.

## Quick Reference

When working on OpenCode-related features, **always consult the relevant documentation first** before making changes or assumptions about how OpenCode works.

---

## Core Concepts

### Getting Started

- **`docs/index.mdx`** - Introduction, installation, and quick start guide
- **`docs/config.mdx`** - Configuration options and settings
- **`docs/troubleshooting.mdx`** - Common issues and solutions

### Agent System

- **`docs/agents.mdx`** - Agent configuration, primary agents vs subagents, built-in agents
- **`docs/commands.mdx`** - Custom command creation and configuration
- **`docs/rules.mdx`** - Rule system for agent behavior customization
- **`docs/skills.mdx`** - Skill system for specialized capabilities

---

## Integration & Extensibility

### MCP & Tools

- **`docs/mcp-servers.mdx`** - Model Context Protocol server integration
- **`docs/tools.mdx`** - Tool system and custom tool creation
- **`docs/custom-tools.mdx`** - Advanced custom tool development

### Plugins & SDK

- **`docs/plugins.mdx`** - Plugin system and plugin development
- **`docs/sdk.mdx`** - OpenCode SDK for programmatic integration

### Language Support

- **`docs/go.mdx`** - Go language integration
- **`docs/lsp.mdx`** - Language Server Protocol integration
- **`docs/formatters.mdx`** - Code formatter configuration

---

## User Interfaces

### Terminal & Desktop

- **`docs/tui.mdx`** - Terminal UI features and usage
- **`docs/cli.mdx`** - Command-line interface
- **`docs/web.mdx`** - Web interface
- **`docs/ide.mdx`** - IDE integration

### Customization

- **`docs/themes.mdx`** - Theme customization
- **`docs/keybinds.mdx`** - Keyboard shortcut configuration
- **`docs/modes.mdx`** - Operating modes (chat, edit, etc.)

---

## Infrastructure & Deployment

### Server & Network

- **`docs/server.mdx`** - Server deployment and configuration
- **`docs/network.mdx`** - Network configuration and proxy settings
- **`docs/permissions.mdx`** - Permission system and security

### Providers & Models

- **`docs/providers.mdx`** - LLM provider configuration
- **`docs/models.mdx`** - Model selection and configuration

### Enterprise

- **`docs/enterprise.mdx`** - Enterprise features and deployment
- **`docs/acp.mdx`** - Access Control Protocol

---

## Collaboration & Ecosystem

### Version Control Integration

- **`docs/github.mdx`** - GitHub integration
- **`docs/gitlab.mdx`** - GitLab integration

### Sharing & Collaboration

- **`docs/share.mdx`** - Session sharing features
- **`docs/ecosystem.mdx`** - OpenCode ecosystem and community tools

---

## Platform-Specific

- **`docs/windows-wsl.mdx`** - Windows and WSL setup
- **`docs/zen.mdx`** - Zen mode features

---

## Usage Guidelines for Agents

### When to Consult Documentation

1. **Before implementing OpenCode features** - Understand the existing architecture
2. **When adding integrations** - Follow established patterns for MCP, plugins, tools
3. **When modifying agent behavior** - Check agents.mdx, commands.mdx, rules.mdx
4. **When troubleshooting** - Review troubleshooting.mdx first
5. **When unsure about capabilities** - Search the relevant docs

### How to Use This Reference

1. **Identify the feature area** you're working on
2. **Locate the relevant documentation file(s)** from the categories above
3. **Read the documentation** using the Read tool
4. **Follow existing patterns** found in the documentation
5. **Document any deviations** if you must diverge from documented behavior

### Documentation File Paths

All documentation files are located at: `docs/`

Example: To read the agents documentation, use:

```txt
Read: docs/agents.mdx
```

---

## Notes for EPCV Workflow

- **Exploration Phase**: Always review relevant docs before proposing solutions
- **Planning Phase**: Reference documentation when designing implementations
- **Coding Phase**: Follow patterns and conventions documented in the MDX files
- **Verification Phase**: Validate against documented behavior and best practices
