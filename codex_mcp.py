import asyncio
import os
import sys

from agents import Agent, Runner
from agents.mcp import MCPServerStdio

SHIM_PATH = os.path.join(os.path.dirname(__file__), "codex_mcp_shim.py")


async def main() -> None:
    async with MCPServerStdio(
        name="Codex CLI",
        params={
            "command": sys.executable,
            "args": [SHIM_PATH],
        },
        client_session_timeout_seconds=360000,
    ) as codex_mcp_server:
        print("Codex MCP server started.")
        # More logic coming in the next sections.
        return


if __name__ == "__main__":
    asyncio.run(main())
