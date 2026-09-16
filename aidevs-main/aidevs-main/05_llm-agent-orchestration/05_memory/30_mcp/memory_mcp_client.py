"""Streamable HTTP로 Memory MCP Tool을 호출하는 최소 Client입니다."""

import asyncio
import os

from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


load_dotenv()
MCP_URL = os.getenv("MEMORY_MCP_URL", "http://127.0.0.1:8012/mcp")


async def main() -> None:
    async with streamable_http_client(MCP_URL) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("사용 가능한 Tool:", [tool.name for tool in tools.tools])

            saved = await session.call_tool(
                "save_memory",
                {"key": "food_restriction", "value": "해산물 알레르기"},
            )
            print("저장 결과:", saved.structuredContent or saved.content)

            selected = await session.call_tool(
                "find_relevant_memories",
                {"question": "부산에서 식당을 추천해줘"},
            )
            print("관련 Memory:", selected.structuredContent or selected.content)


if __name__ == "__main__":
    asyncio.run(main())
