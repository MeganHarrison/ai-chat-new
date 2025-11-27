# ==========================================
# CODEX MODE INSTRUCTIONS (READ BEFORE USE)
# ==========================================
# - You MUST read the entire file before acting.
# - Think strategically and technically before producing output.
# - Validate all changes against REQUIREMENTS.md and AGENT_TASKS.md.
# - Identify missing steps, risks, or architectural gaps.
# - Never produce superficial modifications.
# - Provide reasoning and improvement suggestions proactively.
# - Maintain structural and semantic consistency across roles and files.


import asyncio
import os
import sys

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

SHIM_PATH = os.path.join(os.path.dirname(__file__), "codex_mcp_shim.py")


async def main() -> None:
    async with MCPServerStdio(
        name="Codex CLI",
        params={"command": sys.executable, "args": [SHIM_PATH]},
        client_session_timeout_seconds=360000,
    ) as codex_mcp_server:
        designer_agent = Agent(
            name="Designer",
            instructions=(
                f"""{RECOMMENDED_PROMPT_PREFIX}"""
                "You are the Designer for the Nutrition Solutions AI Sales Coach experience.\n"
                "Your only source of truth is AGENT_TASKS.md and REQUIREMENTS.md from the Project Manager.\n"
                "Do not assume anything that is not written there.\n\n"
                "Deliverables (write to /design):\n"
                "- design_spec.md - describe the guided conversation flow (hook, demographics, goals, habits, emotional root, role of NS, testimonials carousel, plan recommendation) plus off-route logic, RAG-supplemented answers, Active Client support prompts, and carousel placement.\n"
                "- wireframe.md - capture the Chatkit-style interface layout, chat bubbles, carousel area, CTA buttons, and support selector.\n\n"
                "Focus on tone that feels human, bold, and transformation-focused, and note how the script should pause, answer off-route questions, and transition back to the CTA.\n"
                "When complete, handoff to the Project Manager with transfer_to_project_manager_agent.\n"
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
                "You are the Frontend Developer for the Nutrition Solutions AI Sales Coach.\n"
                "Read AGENT_TASKS.md and design_spec.md. Implement exactly what is described there.\n\n"
                "Deliverables (write to /frontend):\n"
                "- index.html - Intercom-style chat window with Chatkit integration, guided script flow, and transformation carousel area.\n"
                "- styles.css - brand-aligned styling, responsive layout, and carousel presentation.\n"
                "- main.js - chat state machine that handles hook → questions → testimonials → plan recommendation, off-route digressions, memory cues, Active Client support selector, and connectors to backend RAG/memory/support APIs.\n\n"
                "Follow the Designer's structure and any integration points from the Project Manager.\n"
                "Do not add features beyond the provided documents.\n\n"
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
                "Read AGENT_TASKS.md and REQUIREMENTS.md. Implement the backend endpoints described there.\n\n"
                "Deliverables (write to /backend):\n"
                "- package.json - include a start script and the dependencies for Supabase vector RAG, memory store, and HTTP serving.\n"
                "- server.js - implement endpoints for plan recommendations, RAG retrievals, memory capture/lookup, transformation carousel filters, Active Client support routing, and any reasoning wrappers needed to keep responses motivating.\n\n"
                "Keep the code as simple and readable as possible; prefer in-memory or Supabase storage per requirements.\n\n"
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
                "Read AGENT_TASKS.md and TEST.md. Verify that the outputs of the other roles meet the acceptance criteria.\n\n"
                "Deliverables (write to /tests):\n"
                "- TEST_PLAN.md - checklist covering guided flow, conditional plan recommendations, RAG responses, off-route handling, Active Client support path, carousel filtering, and API responses.\n"
                "- test.sh - optional script that triggers backend endpoints and ensures the answers match the motivational, brand-aligned tone.\n\n"
                "Keep it minimal and easy to run.\n\n"
                "When complete, handoff to the Project Manager with transfer_to_project_manager_agent.\n"
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
                You are the Project Manager for the Nutrition Solutions AI Sales Coach.

                Objective:
                Convert the input task list into three project-root files the team will execute against.

                Deliverables (write in project root):
                - REQUIREMENTS.md: concise summary of product goals, target users, key features, off-route/RAG/support rules, and constraints.
                - TEST.md: tasks with [Owner] tags (Designer, Frontend, Backend, Tester) and clear acceptance criteria tied to the transformation coach experience.
                - AGENT_TASKS.md: one section per role containing:
                  - Project name
                  - Required deliverables (exact file names and purpose)
                  - Key technical notes and constraints

                Process:
                - Resolve ambiguities with minimal, reasonable assumptions. Be specific so each role can act without guessing.
                - Create files using Codex MCP with {"approval-policy":"never","sandbox":"workspace-write"}.
                - Do not create folders. Only create REQUIREMENTS.md, TEST.md, AGENT_TASKS.md.

                Handoffs (gated by required files):
                1) After the three files above are created, hand off to the Designer with transfer_to_designer_agent and include REQUIREMENTS.md and AGENT_TASKS.md.
                2) Wait for the Designer to produce /design/design_spec.md. Verify that file exists before proceeding.
                3) When design_spec.md exists, hand off in parallel to both:
                   - Frontend Developer with transfer_to_frontend_developer_agent (provide design_spec.md, REQUIREMENTS.md, AGENT_TASKS.md).
                   - Backend Developer with transfer_to_backend_developer_agent (provide REQUIREMENTS.md, AGENT_TASKS.md).
                4) Wait for Frontend to produce /frontend/index.html and Backend to produce /backend/server.js. Verify both files exist.
                5) When both exist, hand off to the Tester with transfer_to_tester_agent and provide all prior artifacts and outputs.
                6) Do not advance to the next handoff until the required files for that step are present. If something is missing, request the owning agent to supply it and re-check.

                PM Responsibilities:
                - Coordinate all roles, track file completion, and enforce the above gating checks.
                - Do NOT respond with status updates. Just handoff to the next agent until the project is complete.
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

        task_list = """
Goal: Build the Nutrition Solutions AI Sales Coach — a high-converting, Intercom-style chatbot that feels like an elite transformation mentor rather than a rigid FAQ bot.

High-level requirements:
- Follow the guided transformation script (hook, demographics, goal, habits, emotional root, role of Nutrition Solutions, transformation carousel + testimonials, synthesis + plan recommendation) with conditional branching for consistency, plan choices, and support.
- Build in intelligent off-route handling: detect unrelated questions, price doubts, emotional inputs, or skipped steps; pause the guided flow, answer naturally using reasoning (and RAG when needed), and smoothly resume the conversion sequence or CTA without forcing the user.
- Use RAG (e.g., Supabase vector stores for FAQs, testimonials, meal plans, product/policy data) but wrap retrieved facts in motivational, brand-aligned language that positions NS as a transformative system, not a food vendor.
- Implement short-term and long-term memory cues to recognize returning visitors and reference prior interactions naturally.
- Provide an Active Client support path triggered by keywords (current client, order question, meal help) that acknowledges the user, attempts RAG-based answers, and, if unanswered, offers text/call concierge handoff or short form submission to human support.
- Display a Transformation Carousel widget filtered by user inputs alongside plan recommendations; chain the carousel with CTA buttons pointing to plan offers, support options, or custom forms.
- Backend APIs should surface plan recommendations, RAG query results, memory lookups, support routing, and reasoned answers; the frontend should connect via Chatkit to render chat bubbles, carousel, and CTA transitions.
- Log conversation state for gating (per the multi-agent workflow), ensure the tone remains bold, direct, and empathetic, and keep the experience entertaining yet educational.

Roles:
- Designer: document the conversation architecture, off-route behaviors, Active Client support flow, and wireframe the Chatkit interface/carousel.
- Frontend Developer: build the chat UI, carousel, UI state transitions, and integrate with backend endpoints plus memory/RAG indicators.
- Backend Developer: implement recommendation, RAG, memory, and support routing APIs; ensure reasoning wraps results and fallback options (text/call/form) are exposed.
- Tester: verify the guided flow, off-route handling, memory recognition, RAG responses, Active Client support path, carousel filtering, and backend APIs against acceptance criteria.

Constraints:
- Maintain bold, identity-focused NS brand voice; the assistant must always feel human, curious, and transformation-oriented.
- Use Codex AGENTS workflow (designer/front-end/back-end/tester) with the gating rules: PM generates REQUIREMENTS.md, AGENT_TASKS.md, TEST.md; front-end/back-end wait for the design spec; tester waits for both code outputs.
- Prefer in-memory or Supabase storage; avoid unnecessary frameworks and ensure all artifacts go into their designated folders.
- Always call Codex MCP with {"approval-policy":"never","sandbox":"workspace-write"} when creating files.
"""

        result = await Runner.run(project_manager_agent, task_list, max_turns=30)
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
