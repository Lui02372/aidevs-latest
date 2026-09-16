"""
[MCP 연결 점검 시나리오]
전체 서비스를 실행하기 전에 MCP Server만 독립적으로 확인합니다. 실제 Open-Meteo 기반
Tool 결과 또는 연결 오류를 그대로 확인하여 Agent 문제와 Tool 문제를 분리합니다.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


MCP_URL = os.getenv("TRAVEL_MCP_URL", "http://127.0.0.1:8010/mcp")


async def call_travel_tool(name: str, arguments: dict[str, object]) -> dict[str, object]:
    async with streamable_http_client(MCP_URL) as streams:
        read_stream, write_stream = streams[0], streams[1]
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            available = {tool.name for tool in (await session.list_tools()).tools}
            if name not in available:
                raise RuntimeError(f"MCP Tool을 찾을 수 없습니다: {name}")
            result = await session.call_tool(name, arguments=arguments)
            if result.isError:
                messages = [getattr(item, "text", str(item)) for item in result.content]
                raise RuntimeError("; ".join(messages))
            structured = getattr(result, "structuredContent", None) or getattr(
                result, "structured_content", None
            )
            if structured:
                return structured
            for item in result.content:
                text = getattr(item, "text", None)
                if text:
                    return json.loads(text)
    raise RuntimeError("MCP Tool이 결과를 반환하지 않았습니다.")


async def main() -> None:
    city = sys.argv[1] if len(sys.argv) > 1 else "부산"
    print(json.dumps(await call_travel_tool("get_weather", {"city": city, "forecast_days": 3}), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
