import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from agents import (
    Agent,
    ModelSettings,
    Runner,
    WebSearchTool,
    set_default_openai_api,
)
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.mcp import MCPServerStdio
from openai.types.shared import Reasoning

load_dotenv(override=True)
set_default_openai_api(os.getenv("OPENAI_API_KEY"))

SHIM_PATH = Path(__file__).with_name("codex_mcp_shim.py")


async def main() -> None:
    async with MCPServerStdio(
        name="Codex CLI",
        params={"command": sys.executable, "args": [str(SHIM_PATH)]},
        client_session_timeout_seconds=360000,
    ) as codex_mcp_server:
        designer_agent = Agent(
            name="Designer",
            instructions=(
                f"""{RECOMMENDED_PROMPT_PREFIX}"""
                "You are the Designer.\n"
                "Your only source of truth is REQUIREMENTS.md and AGENT_TASKS.md from the Project Manager. Do not assume anything else.\n\n"
                "Deliverables (write to /design):\n"
                "- design_spec.md: document the full guided conversation flow, off-route logic, Active Client Support path, brand voice guidance, Transformation Carousel placement, user-state transitions, message timing/bubble sequencing, and widget interaction rules.\n"
                "- wireframe.md: text/ASCII structural layout of the widget showing chat window anatomy, CTA/quick replies, carousel placement diagrams, and other major UI regions.\n\n"
                "Do not write code or JSON—produce implementation-ready docs that match REQUIREMENTS.md exactly.\n"
                "When complete, handoff to the Project Manager with transfer_to_project_manager.\n"
                "When creating files, call Codex MCP with {\"approval-policy\":\"never\",\"sandbox\":\"workspace-write\"}."
            ),
            model="gpt-5",
            tools=[WebSearchTool()],
            mcp_servers=[codex_mcp_server],
        )

        frontend_developer_agent = Agent(
            name="Frontend Developer",
            instructions=(
                f"""{RECOMMENDED_PROMPT_PREFIX}"""
                "You are the Frontend Developer.\n"
                "Use REQUIREMENTS.md, AGENT_TASKS.md, and the Designer’s files as your blueprint.\n\n"
                "Deliverables:\n"
                "- /frontend/index.html, /frontend/styles.css, /frontend/main.js implementing the ChatKit-powered chat interface, deterministic guided-flow state machine, off-route handling hooks, CTA logic, and Transformation Carousel rendering.\n"
                "- /widget/widget.js, /widget/widget.css, /widget/chat-window.html to provide the Intercom-style embed bubble with scoped styles safe for any host page.\n"
                "- /conversation/flow.json, /conversation/offroute.json, /conversation/recommendation_rules.json capturing the guided script, off-route responses, and plan recommendation rules.\n\n"
                "Use vanilla JS only, scope CSS to avoid leakage (Shadow DOM or equivalent), and match the Designer’s structure precisely. Implement the Transformation Carousel and link to backend endpoints as defined in REQUIREMENTS.md.\n"
                "When complete, handoff to the Project Manager with transfer_to_project_manager_agent.\n"
                "When creating files, call Codex MCP with {\"approval-policy\":\"never\",\"sandbox\":\"workspace-write\"}."
            ),
            model="gpt-5",
            mcp_servers=[codex_mcp_server],
        )

        backend_developer_agent = Agent(
            name="Backend Developer",
            instructions=(
                f"""{RECOMMENDED_PROMPT_PREFIX}"""
                "You are the Backend Developer.\n"
                "Read AGENT_TASKS.md and REQUIREMENTS.md. Implement exactly what they describe.\n\n"
                "Deliverables:\n"
                "- /backend/package.json with scripts for running the Node 18+ server.\n"
                "- /backend/server.js wiring Express, middleware, logging, and the API surface.\n"
                "- /backend/routes/message.js, rag.js, recommend.js, support.js, memory.js, carousel.js implementing Agents SDK orchestration, Supabase vector search, plan synthesis, memory store/fetch, support routing, and carousel filtering logic.\n\n"
                "Expose GET /api/health, POST /api/message, POST /api/rag, POST /api/recommend, POST /api/memory/store, POST /api/memory/fetch, GET /api/carousel, POST /api/support. Integrate Agents SDK, Supabase, Active Client Support routing, and analytics logging per REQUIREMENTS.md. Keep dependencies minimal and code clear.\n"
                "When complete, handoff to the Project Manager with transfer_to_project_manager_agent.\n"
                "When creating files, call Codex MCP with {\"approval-policy\":\"never\",\"sandbox\":\"workspace-write\"}."
            ),
            model="gpt-5",
            mcp_servers=[codex_mcp_server],
        )

        tester_agent = Agent(
            name="Tester",
            instructions=(
                f"""{RECOMMENDED_PROMPT_PREFIX}"""
                "You are the Tester.\n"
                "Read AGENT_TASKS.md, REQUIREMENTS.md, TEST.md, and every produced artifact. Validate guided flow behavior, off-route handling, RAG-backed responses, plan recommendations, Active Client Support logic, carousel filtering, widget/embedding, backend API correctness, and file-structure compliance.\n\n"
                "Deliverables (write to /tests):\n"
                "- TEST_PLAN.md outlining deterministic manual or scripted test coverage for the scope above.\n"
                "- Optional test.sh for smoke checks or API calls if useful.\n\n"
                "Reference concrete files and acceptance criteria. When complete, handoff to the Project Manager with transfer_to_project_manager.\n"
                "When creating files, call Codex MCP with {\"approval-policy\":\"never\",\"sandbox\":\"workspace-write\"}."
            ),
            model="gpt-5",
            mcp_servers=[codex_mcp_server],
        )

        project_manager_agent = Agent(
            name="Project Manager",
            instructions=(
                f"""{RECOMMENDED_PROMPT_PREFIX}"""
                """
                You are the Project Manager.

                Objective:
                Convert TASK_LIST.md into the three root-level documents the team executes against.

                Deliverables (write in project root):
                - REQUIREMENTS.md: concise narrative of goals, users, key features, and constraints.
                - TEST.md: acceptance criteria grouped by [Owner] tags (Designer, Frontend Developer, Backend Developer, Tester).
                - AGENT_TASKS.md: one section per role describing the project name, exact file deliverables (paths/names), and critical constraints/notes they must follow.

                Process:
                - Read TASK_LIST.md only. Interpret it into deterministic instructions—never invent extra files or rename anything.
                - Create files using Codex MCP with {"approval-policy":"never","sandbox":"workspace-write"}.
                - Do NOT perform design, frontend, backend, or testing work.

                Gated handoffs (use os.path.exists to check files):
                0) Before generating or rewriting any file, check if it already exists with the correct name. If so, skip recreating it and proceed to the next required gate.
                1) Once REQUIREMENTS.md, AGENT_TASKS.md, and TEST.md exist, hand off to the Designer via transfer_to_designer_agent (include REQUIREMENTS.md + AGENT_TASKS.md). Do not recreate these files if they are already present.
                2) Confirm BOTH /design/design_spec.md and /design/wireframe.md exist. If either is missing, instruct the Designer to deliver it; if both exist, skip re-running the Designer and move on.
                3) When both design files exist, hand off concurrently:
                   - transfer_to_frontend_developer_agent with REQUIREMENTS.md, AGENT_TASKS.md, design_spec.md, wireframe.md.
                   - transfer_to_backend_developer_agent with REQUIREMENTS.md and AGENT_TASKS.md.
                4) Frontend gate: require /frontend/index.html, /frontend/styles.css, /frontend/main.js, /widget/widget.js, /widget/widget.css, /widget/chat-window.html, /conversation/flow.json, /conversation/offroute.json, /conversation/recommendation_rules.json.
                5) Backend gate: require /backend/package.json, /backend/server.js, and /backend/routes/message.js, rag.js, recommend.js, support.js, memory.js, carousel.js.
                6) After both gates succeed, hand off to the Tester using transfer_to_tester_agent and provide all prior artifacts.
                7) Tester gate: ensure /tests/TEST_PLAN.md exists (and /tests/test.sh if they choose to create it) before proceeding.
                8) Perform a final audit confirming every deliverable listed in AGENT_TASKS.md exists before ending the workflow.

                PM Responsibilities:
                - Enforce the strict file/directory naming rules from AGENTS.md.
                - Redirect agents if requirements, formats, or file names are incorrect.
                - Communicate only via handoffs—no free-form status messages.
                """
            ),
            model="gpt-5",
            model_settings=ModelSettings(
                reasoning=Reasoning(effort="medium"),
            ),
            handoffs=[designer_agent, frontend_developer_agent, backend_developer_agent, tester_agent],
            mcp_servers=[codex_mcp_server],
        )

        designer_agent.handoffs = [project_manager_agent]
        frontend_developer_agent.handoffs = [project_manager_agent]
        backend_developer_agent.handoffs = [project_manager_agent]
        tester_agent.handoffs = [project_manager_agent]

        task_list = Path("TASK_LIST.md").read_text()

        result = await Runner.run(project_manager_agent, task_list, max_turns=30)
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
