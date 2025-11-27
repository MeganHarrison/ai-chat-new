# ================================================================
# MULTI-AGENT WORKFLOW — CLEAN REWRITE (STRICT GATED VERSION)
# ================================================================
# This workflow is engineered according to:
# - REQUIREMENTS.md
# - AGENT_TASKS.md
# - OpenAI Codex engineering best-practices
#
# STRICT enforcement of all deliverables:
# Designer → Frontend + Backend → Tester
# ================================================================

import asyncio
import os
import sys
from dotenv import load_dotenv

from agents import (
    Agent,
    ModelSettings,
    Runner,
    set_default_openai_api,
)
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.mcp import MCPServerStdio
from openai.types.shared import Reasoning

load_dotenv(override=True)
set_default_openai_api(os.getenv("OPENAI_API_KEY"))

SHIM_PATH = os.path.join(os.path.dirname(__file__), "codex_mcp_shim.py")

# ================================================================
# STRICT FILE ENFORCEMENT HELPERS — RUN BY PM
# ================================================================
REQUIRED_PM_FILES = [
    "REQUIREMENTS.md",
    "AGENT_TASKS.md",
    "TEST.md",
]

REQUIRED_DESIGN_FILES = [
    "design/design_spec.md",
    "design/wireframe.md",
]

REQUIRED_FRONTEND_FILES = [
    "frontend/index.html",
    "frontend/styles.css",
    "frontend/main.js",
]

REQUIRED_BACKEND_FILES = [
    "backend/package.json",
    "backend/server.js",
    "backend/routes/message.js",
    "backend/routes/rag.js",
    "backend/routes/recommend.js",
    "backend/routes/support.js",
    "backend/routes/memory.js",
    "backend/routes/carousel.js",
]

REQUIRED_WIDGET_FILES = [
    "widget/widget.js",
    "widget/widget.css",
    "widget/chat-window.html",
]

REQUIRED_CONVERSATION_FILES = [
    "conversation/flow.json",
    "conversation/offroute.json",
    "conversation/recommendation_rules.json",
]

REQUIRED_TEST_FILES = [
    "tests/TEST_PLAN.md",
]


def file_exists(path: str) -> bool:
    return os.path.exists(os.path.join(os.getcwd(), path))


def all_exist(files: list[str]) -> bool:
    return all(file_exists(f) for f in files)


# ================================================================
# MAIN WORKFLOW
# ================================================================
async def main() -> None:
    async with MCPServerStdio(
        name="Codex CLI",
        params={"command": sys.executable, "args": [SHIM_PATH]},
        client_session_timeout_seconds=360000,
    ) as codex_mcp:

        # ------------------------------------------------------------
        # DESIGNER
        # ------------------------------------------------------------
        designer = Agent(
            name="Designer",
            instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are the Designer for the Nutrition Solutions AI Sales Coach.

SOURCE OF TRUTH:
- REQUIREMENTS.md
- AGENT_TASKS.md

DELIVERABLES (write to /design):
  - design_spec.md
  - wireframe.md

REQUIREMENT SUMMARY:
You must document:
- Entire guided conversation flow
- Off-route logic
- Active Client Support flow
- RAG usage rules
- Brand-voice notes
- ChatKit layout, bubble sequencing
- Carousel placement logic
- Widget interaction behavior

YOUR CONTRACT:
- Do NOT invent new features.
- Follow REQUIREMENTS.md exactly.
- Create required files using Codex MCP:
    {{ "approval-policy": "never", "sandbox": "workspace-write" }}
- When both design files exist, transfer_to_project_manager_agent.
""",
            model="gpt-5",
            mcp_servers=[codex_mcp],
        )

        # ------------------------------------------------------------
        # FRONTEND
        # ------------------------------------------------------------
        frontend = Agent(
            name="Frontend Developer",
            instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are the Frontend Developer.

SOURCE OF TRUTH:
- REQUIREMENTS.md
- AGENT_TASKS.md
- design/design_spec.md

DELIVERABLES (write to /frontend):
  - index.html
  - styles.css
  - main.js

Also required (write to /widget):
  - widget.js (universal embed widget)
  - widget.css
  - chat-window.html

Also required (write to /conversation):
  - flow.json
  - offroute.json
  - recommendation_rules.json

RULES:
- Build the Intercom-style floating chat widget using ChatKit.
- Implement deterministic state machine in main.js.
- Implement UI for guided flow, off-route responses, and carousel.
- DO NOT add frameworks.
- All file paths must match AGENT_TASKS.md exactly.

When all frontend + widget + conversation files exist, transfer_to_project_manager_agent.
""",
            model="gpt-5",
            mcp_servers=[codex_mcp],
        )

        # ------------------------------------------------------------
        # BACKEND
        # ------------------------------------------------------------
        backend = Agent(
            name="Backend Developer",
            instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are the Backend Developer.

SOURCE OF TRUTH:
- REQUIREMENTS.md
- AGENT_TASKS.md

DELIVERABLES (write to /backend):
  - package.json
  - server.js
  - routes/message.js
  - routes/rag.js
  - routes/recommend.js
  - routes/support.js
  - routes/memory.js
  - routes/carousel.js

ROUTE REQUIREMENTS:
- /api/message → orchestrates Agents SDK
- /api/rag → Supabase vector search
- /api/recommend → plan synthesis
- /api/memory/store, /fetch → memory system
- /api/support → Active Client escalation
- /api/carousel → filtered testimonials

RULES:
- Keep code minimal and readable.
- No unnecessary dependencies.
- Must integrate Supabase where required.

When all backend route files exist, transfer_to_project_manager_agent.
""",
            model="gpt-5",
            mcp_servers=[codex_mcp],
        )

        # ------------------------------------------------------------
        # TESTER
        # ------------------------------------------------------------
        tester = Agent(
            name="Tester",
            instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are the Tester.

SOURCE OF TRUTH:
- REQUIREMENTS.md
- AGENT_TASKS.md
- TEST.md

DELIVERABLES (write to /tests):
  - TEST_PLAN.md

Optionally:
  - test.sh

You must validate:
- Guided flow
- Off-route logic
- RAG responses
- Support escalation path
- Carousel filtering
- Recommendation engine logic
- Widget / ChatKit behaviors
- Backend API correctness

When TEST_PLAN.md exists, transfer_to_project_manager_agent.
""",
            model="gpt-5",
            mcp_servers=[codex_mcp],
        )

        # ------------------------------------------------------------
        # PROJECT MANAGER (STRICT ENFORCEMENT)
        # ------------------------------------------------------------
        pm = Agent(
            name="Project Manager",
            model="gpt-5",
            mcp_servers=[codex_mcp],
            model_settings=ModelSettings(reasoning=Reasoning(effort="medium")),
            instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are the Project Manager.

Your job is to:
1. Generate REQUIREMENTS.md, AGENT_TASKS.md, and TEST.md.
2. Enforce STRICT gating.

=======================================================
STRICT GATING LOGIC
=======================================================

STEP 1 — PM CREATES:
  - REQUIREMENTS.md
  - AGENT_TASKS.md
  - TEST.md

Do not proceed until ALL THREE FILES EXIST.

STEP 2 — HANDOFF TO DESIGNER
Wait until BOTH:
  - design/design_spec.md
  - design/wireframe.md
exist.

STEP 3 — PARALLEL HANDOFF:
When design files exist → handoff to:
  - Frontend Developer
  - Backend Developer

STEP 4 — BACKEND MUST PRODUCE:
    ALL backend route files (8 total)

STEP 5 — FRONTEND MUST PRODUCE:
    ALL frontend files
    ALL widget files
    ALL conversation JSON configs

STEP 6 — When ALL frontend + backend files exist → handoff to Tester.

STEP 7 — TESTER MUST PRODUCE:
  - tests/TEST_PLAN.md

When TEST_PLAN.md exists → workflow complete.

=======================================================
RULES:
=======================================================
- You must ALWAYS check file existence before handoff.
- If files are missing, instruct the responsible agent to create them.
- Never guess or invent deliverables.
- Use Codex MCP for file creation:
    {{ "approval-policy": "never", "sandbox": "workspace-write" }}
- No status updates — just enforce gating and move agents forward.

""",
            handoffs=[designer, frontend, backend, tester],
        )

        # Link reverse handoffs
        designer.handoffs = [pm]
        frontend.handoffs = [pm]
        backend.handoffs = [pm]
        tester.handoffs = [pm]

        # ------------------------------------------------------------
        # INITIAL TASK LIST
        # ------------------------------------------------------------
        task_list = """
Build the Nutrition Solutions AI Sales Coach — a conversion-optimized, Intercom-style chat widget using ChatKit + Agents SDK + Supabase, strictly following REQUIREMENTS.md and AGENT_TASKS.md.
"""

        result = await Runner.run(pm, task_list, max_turns=40)
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
