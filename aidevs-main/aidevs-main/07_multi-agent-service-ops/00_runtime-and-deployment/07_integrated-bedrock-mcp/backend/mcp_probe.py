"""실제 MCP 서버에서 tool/resource 목록과 자료를 읽는다. --city를 주면 유료 LLM 없이 날씨를 조회한다."""
import argparse
import asyncio
import json
from app import mcp_session, RESOURCE_URI


async def probe(city):
    async with mcp_session() as session:
        print("tools:", [tool.name for tool in (await session.list_tools()).tools])
        print("resources:", [str(item.uri) for item in (await session.list_resources()).resources])
        result = await session.read_resource(RESOURCE_URI)
        print("resource:", "\n".join(item.text for item in result.contents if hasattr(item, "text")))
        if city:
            result = await session.call_tool("get_weather", {"city": city, "day": "tomorrow"})
            if result.isError: raise RuntimeError(result)
            print("tool result:", json.dumps(result.model_dump(mode="json"), ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--city")
    asyncio.run(probe(parser.parse_args().city))
