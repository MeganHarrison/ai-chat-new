#!/usr/bin/env python3
"""
Shim that proxies between the Agents SDK and the Codex CLI MCP server.
It intercepts Codex-specific `codex/event` notifications and remaps them
to standard `notifications/message` events so downstream MCP clients
stop emitting validation warnings.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from typing import Any


CODEX_CMD = ["npx", "-y", "@openai/codex", "mcp-server"]


def _transform_codex_event(raw: bytes) -> bytes:
    """Convert codex/event messages into standard MCP notifications."""
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return raw

    if isinstance(payload, dict) and payload.get("method") == "codex/event":
        msg: Any = payload.get("params", {}).get("msg")
        transformed = {
            "jsonrpc": "2.0",
            "method": "notifications/message",
            "params": {
                "level": "info",
                "data": msg,
            },
        }
        return (json.dumps(transformed) + "\n").encode("utf-8")

    return raw


async def _pump_stdin(writer: asyncio.StreamWriter) -> None:
    loop = asyncio.get_running_loop()
    while True:
        data = await loop.run_in_executor(None, sys.stdin.buffer.readline)
        if not data:
            writer.close()
            await writer.wait_closed()
            break
        writer.write(data)
        await writer.drain()


async def _pump_stdout(reader: asyncio.StreamReader) -> None:
    loop = asyncio.get_running_loop()
    while True:
        data = await reader.readline()
        if not data:
            break
        transformed = _transform_codex_event(data)
        sys.stdout.buffer.write(transformed)
        await loop.run_in_executor(None, sys.stdout.buffer.flush)


async def main() -> int:
    proc = await asyncio.create_subprocess_exec(
        *CODEX_CMD,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=sys.stderr,
    )

    assert proc.stdin is not None
    assert proc.stdout is not None

    await asyncio.gather(
        _pump_stdin(proc.stdin),
        _pump_stdout(proc.stdout),
    )

    return await proc.wait()


if __name__ == "__main__":
    try:
        raise SystemExit(asyncio.run(main()))
    except KeyboardInterrupt:
        # Allow clean exit if parent terminates.
        raise SystemExit(1)
