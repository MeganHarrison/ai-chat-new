# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a multi-agent AI workflow system that automates the development of a sophisticated chat widget. The system uses OpenAI's Agents SDK with MCP (Model Context Protocol) to orchestrate specialized agents that build a complete Intercom-style customer support chat interface.

## Key Commands

### Running the Multi-Agent Workflow
```bash
# Set up environment
echo "OPENAI_API_KEY=your_key_here" > .env

# Run the main workflow
python multi_agent_workflow.py
```

### Dependencies
- Python 3.x with `python-dotenv`
- Node.js and npm (for Codex CLI)
- OpenAI Agents SDK

## Architecture

### Core System Components

1. **multi_agent_workflow.py** - Main orchestrator that:
   - Reads task specifications from TASK_LIST.md
   - Launches Project Manager agent with MCP tools
   - Uses codex_mcp_shim.py to proxy Codex CLI events
   - Manages agent handoffs through PM gating

2. **codex_mcp_shim.py** - MCP proxy that:
   - Intercepts Codex-specific notifications
   - Transforms them to standard MCP events
   - Enables Codex CLI integration

3. **Agent Hierarchy** (defined in AGENTS.md):
   ```
   Project Manager (PM)
   ├── Designer
   ├── Frontend Developer
   ├── Backend Developer
   └── Tester
   ```

### Agent Responsibilities

- **Project Manager**: Creates REQUIREMENTS.md, AGENT_TASKS.md, TEST.md and orchestrates handoffs
- **Designer**: Creates design_spec.md and wireframe.md in /design/
- **Frontend Developer**: Builds chat UI in /frontend/, widget in /widget/, flows in /conversation/
- **Backend Developer**: Creates Express API in /backend/ with all route handlers
- **Tester**: Produces TEST_PLAN.md validating the complete system

### Generated Structure
```
/design/          # UX specifications
/frontend/        # Chat interface (ChatKit-based)
/widget/          # Embeddable widget components
/conversation/    # State machine JSON configs
/backend/         # Express API server
/tests/           # Test plans and scripts
```

## Critical Rules

1. **Strict File Paths**: All agents must use exact paths specified in AGENT_TASKS.md
2. **No Frameworks**: Frontend must use vanilla JavaScript only
3. **Deterministic Workflow**: PM enforces gating - no agent proceeds without required files
4. **No Feature Creep**: Implement only what's in REQUIREMENTS.md
5. **MCP Integration**: All agents use Codex CLI for file operations

## Workflow Execution

The system follows a deterministic pipeline:
1. PM reads TASK_LIST.md and creates planning documents
2. Designer creates UX specifications
3. Frontend/Backend developers build in parallel
4. Tester validates all deliverables
5. PM performs final validation

Each agent works autonomously within its defined scope, with the PM managing transitions and ensuring deliverables are complete before handoffs.

## Environment Configuration

- **OPENAI_API_KEY**: Required in .env file
- **Model**: Uses "gpt-5" (preview/internal)
- **MCP Timeout**: 360000 seconds (100 hours)
- **Sandbox Policy**: Automatic file operations enabled

## Validation and Testing

The repository includes comprehensive validation prompts in `.codex/prompts/`:
- `validate_workflow.md` - Validates multi-agent implementation
- `audit_backend.md` - Checks API compliance
- `deepreview.md` - Performs specification analysis
- `specdiff.md` - Compares implementation vs spec

Use these prompts with Codex CLI for quality assurance.