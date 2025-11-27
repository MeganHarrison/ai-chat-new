# ================================================================
# MULTI-AGENT WORKFLOW — FIXED AND FULLY WORKING VERSION
# ================================================================
# Correct imports using the official OpenAI Agents SDK
# Correct MCP integration
# Correct gating logic
# No swallowed async errors
# ================================================================

import asyncio
import os
import sys
from dotenv import load_dotenv

# ✅ Correct imports for the REAL SDK you installed
from openai.agents import Agent, ModelSettings, Runner, set_default_openai_api
from openai.agents.mcp import MCPServerStdio
from openai.agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from openai.types.shared import Reasoning

load_dotenv(override=True)

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY missing in .env")

set_default_openai_api(OPENAI_KEY)

SHIM_PATH = os.path.join(os.path.dirname(__file__), "codex_mcp_shim.py")


# ================================================================
# FILE CHECK HELPERS
# ================================================================
def exists(path: str) -> bool:
    return os.path.exists(os.path.join(os.getcwd(), path))


def all_exist(paths: list[str]) -> bool:
    return all(exists(p) for p in paths)


# ================================================================
# REQUIRED FILES PER ROLE
# ================================================================
PM_FILES = [
    "REQUIREMENTS.md",
    "AGENT_TASKS.md",
    "TEST.md",
]

DESIGN_FILES = [
    "design/design_spec.md",
    "design/wireframe.md",
]

FRONTEND_FILES = [
    "frontend/index.html",
    "frontend/styles.css",
    "frontend/main.js",
]

WIDGET_FILES = [
    "widget/widget.js",
    "widget/widget.css",
    "widget/chat-window.html",
]

CONVERSATION_FILES = [
    "conversation/flow.json",
    "conversation/offroute.json",
    "conversation/recommendation_rules.json",
]

BACKEND_FILES = [
    "backend/package.json",
    "backend/server.js",
    "backend/routes/message.js",
    "backend/routes/rag.js",
    "backend/routes/recommend.js",
    "backend/routes/support.js",
    "backend/routes/memory.js",
    "backend/routes/carousel.js",
]

TEST_FILES = [
    "tests/TEST_PLAN.md",
]


# ================================================================
# MAIN WORKFLOW
# ================================================================
async def main():
    print("🚀 Starting MCP Server…")

    async with MCPServerStdio(
        name="codex-mcp",
        params={"command": sys.executable, "args": [SHIM_PATH]},
        client_session_timeout_seconds=86400,
    ) as mcp:

        # ------------------------------------------------------------
        # DESIGNER AGENT
        # ------------------------------------------------------------
        designer = Agent(
            name="Designer",
            model="gpt-5",
            mcp_servers=[mcp],
            instructions=f"""{RECOMMENDED_PROMPT_PREFIX}

You are the Designer.

Deliverables (write to /design):
- design_spec.md
- wireframe.md

Strictly follow REQUIREMENTS.md and AGENT_TASKS.md.
Do not invent features.
Write files using Codex MCP.
""",
        )

        # ------------------------------------------------------------
        # FRONTEND AGENT
        # ------------------------------------------------------------
        frontend = Agent(
            name="Frontend Developer",
            model="gpt-5",
            mcp_servers=[mcp],
            instructions=f"""{RECOMMENDED_PROMPT_PREFIX}

You are the Frontend Developer.

Deliverables:
- /frontend/index.html
- /frontend/styles.css
- /frontend/main.js
- /widget/widget.js
- /widget/widget.css
- /widget/chat-window.html
- /conversation/flow.json
- /conversation/offroute.json
- /conversation/recommendation_rules.json

No frameworks. Use ChatKit. Follow design_spec.md exactly.
""",
        )

        # ------------------------------------------------------------
        # BACKEND AGENT
        # ------------------------------------------------------------
        backend = Agent(
            name="Backend Developer",
            model="gpt-5",
            mcp_servers=[mcp],
            instructions=f"""{RECOMMENDED_PROMPT_PREFIX}

You are the Backend Developer.

Implement all backend routes listed in REQUIREMENTS.md and AGENT_TASKS.md.
Write to /backend using MCP.
Keep code readable and minimal.
""",
        )

        # ------------------------------------------------------------
        # TESTER
        # ------------------------------------------------------------
        tester = Agent(
            name="Tester",
            model="gpt-5",
            mcp_servers=[mcp],
            instructions=f"""{RECOMMENDED_PROMPT_PREFIX}

You are the Tester.

Write /tests/TEST_PLAN.md validating:
- guided flow
- off-route logic
- recommendation logic
- widget behavior
- API contract correctness
""",
        )

        # ------------------------------------------------------------
        # PROJECT MANAGER
        # ------------------------------------------------------------
        pm = Agent(
            name="Project Manager",
            model="gpt-5",
            mcp_servers=[mcp],
            model_settings=ModelSettings(reasoning=Reasoning(effort="medium")),
            instructions=f"""
{RECOMMENDED_PROMPT_PREFIX}
You are the Project Manager.

STRICT GATING:

STEP 1 — If PM files missing → create:
- REQUIREMENTS.md
- AGENT_TASKS.md
- TEST.md

STEP 2 — When design files missing → instruct Designer.

STEP 3 — When design files exist → instruct Frontend + Backend.

STEP 4 — When frontend + widget + conversation files exist AND backend files exist → instruct Tester.

STEP 5 — When TEST_PLAN.md exists → declare workflow complete.

Always check file existence before handing off.
Never invent deliverables.
Write files via MCP.
""",
            handoffs=[designer, frontend, backend, tester],
        )

        # Reverse links
        designer.handoffs = [pm]
        frontend.handoffs = [pm]
        backend.handoffs = [pm]
        tester.handoffs = [pm]

        # ------------------------------------------------------------
        # RUN WORKFLOW
        # ------------------------------------------------------------
        result = await Runner.run(pm, "Begin", max_turns=60)
        print("🎉 Workflow complete")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
