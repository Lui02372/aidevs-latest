"""두 stdio MCP Server와 순차 Tool Calling을 연결하는 Lab입니다.

질문에는 날씨 조회와 호텔 검색이 함께 들어 있지만 ``parallel_tool_calls=False``이므로
GPT는 한 응답에서 Tool을 최대 하나씩 제안합니다. 특히 취소 규정 조회에 필요한
``hotel_id``는 호텔 검색 결과에서 얻어야 하므로 Tool 결과를 GPT에 돌려주는 Agent
Loop가 필요합니다.

전체 흐름
    1. Client가 Weather MCP Server와 Hotel MCP Server를 각각 자식 프로세스로 실행합니다.
    2. 두 Server에서 ``tools/list``를 호출하고 Tool 이름 앞에 Server 이름을 붙입니다.
    3. GPT가 질문과 전체 Tool Schema를 보고 이번 단계에 필요한 Tool 하나를 선택합니다.
    4. 라우팅 테이블로 원래 Server와 Tool 이름을 찾아 ``tools/call``을 실행합니다.
    5. 결과를 ``function_call_output``으로 GPT에 돌려주고 3번부터 반복합니다.
    6. GPT가 Function Call 없이 답변하면 Loop를 종료합니다.

예상되는 핵심 호출
    - weather__get_current_weather(city="부산")
    - weather__get_weather_forecast(city="부산", days=1)
    - hotel__search_hotels(city="부산", max_price=150000)
    - hotel__get_cancellation_policy(hotel_id="hotel-busan-001")

LLM이 독립적인 날씨 Tool과 호텔 Tool의 순서를 정하므로 실제 순서는 달라질 수 있습니다.
다만 취소 규정 조회는 검색 결과의 hotel_id가 필요하므로 호텔 검색 뒤에 실행됩니다.
"""

import asyncio
import json
import os
import sys
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI


COURSE_ROOT = Path(__file__).resolve().parents[2]
LAB_DIR = Path(__file__).resolve().parent
SERVER_CONFIG_PATH = LAB_DIR / "mcp_servers.json"

load_dotenv(COURSE_ROOT / ".env")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
MAX_AGENT_ROUNDS = 8
QUESTION = (
    "부산의 현재 날씨와 내일 예보를 확인하고, 15만 원 이하 호텔을 찾은 뒤 "
    "검색된 호텔의 취소 규정을 알려줘."
    "관광지 정보도 함께 제공해 주세요."
)
INSTRUCTIONS = (
    "당신은 여행 계획 도우미입니다. 질문을 완전히 해결하는 데 필요한 Tool을 "
    "한 단계씩 사용하세요. 호텔 취소 규정은 반드시 먼저 호텔을 검색하여 얻은 "
    "hotel_id로 조회하세요. Tool 결과만 근거로 한국어 최종 답변을 작성하세요."
)


def to_openai_tool(server_name: str, tool) -> tuple[dict[str, Any], dict[str, str]]:
    """MCP Tool을 Server 이름이 포함된 OpenAI Function Tool로 변환합니다."""
    public_name = f"{server_name}__{tool.name}"
    raw = tool.model_dump(by_alias=True)
    openai_tool = {
        "type": "function",
        "name": public_name,
        "description": f"[{server_name} MCP Server] {tool.description or ''}",
        "parameters": raw["inputSchema"],
        "strict": False,
    }
    route = {"server": server_name, "tool": tool.name}
    return openai_tool, route


def text_result(result) -> str:
    """MCP CallToolResult의 TextContent를 GPT에 전달할 문자열로 합칩니다."""
    return "\n".join(
        content.text for content in result.content if hasattr(content, "text")
    )


async def open_session(
    stack: AsyncExitStack,
    config: dict[str, Any],
) -> ClientSession:
    """stdio Server 하나를 실행하고 초기화된 Session을 반환합니다."""
    command = config.get("command", sys.executable)
    args = [
        str(LAB_DIR / arg)
        if arg.endswith(".py") and not Path(arg).is_absolute()
        else arg
        for arg in config.get("args", [])
    ]
    parameters = StdioServerParameters(
        command=command,
        args=args,
        env=config.get("env"),
    )
    read_stream, write_stream = await stack.enter_async_context(
        stdio_client(parameters)
    )
    session = await stack.enter_async_context(
        ClientSession(read_stream, write_stream)
    )
    await session.initialize()
    return session


def load_server_configs() -> dict[str, dict[str, Any]]:
    """설정 파일에서 연결할 MCP Server 목록을 읽습니다."""
    configs = json.loads(SERVER_CONFIG_PATH.read_text(encoding="utf-8"))
    if not isinstance(configs, dict) or not configs:
        raise ValueError("mcp_servers.json에는 하나 이상의 Server 설정이 필요합니다.")
    if not all(isinstance(config, dict) for config in configs.values()):
        raise ValueError("각 Server 설정은 JSON Object여야 합니다.")
    return configs


async def open_sessions(
    stack: AsyncExitStack,
) -> dict[str, ClientSession]:
    """설정에 등록된 모든 MCP Server에 연결합니다."""
    sessions: dict[str, ClientSession] = {}
    for server_name, config in load_server_configs().items():
        sessions[server_name] = await open_session(stack, config)
    return sessions


async def answer(question: str) -> dict[str, Any]:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY가 필요합니다.")

    trace: list[dict[str, Any]] = []
    llm_calls = 0

    async with AsyncExitStack() as stack:
        sessions = await open_sessions(stack)
        client = await stack.enter_async_context(AsyncOpenAI())

        openai_tools: list[dict[str, Any]] = []
        routes: dict[str, dict[str, str]] = {}
        for server_name, session in sessions.items():
            discovered = (await session.list_tools()).tools
            for tool in discovered:
                openai_tool, route = to_openai_tool(server_name, tool)
                openai_tools.append(openai_tool)
                routes[openai_tool["name"]] = route

        previous_response_id: str | None = None
        input_items: str | list[dict[str, str]] = question

        for round_number in range(1, MAX_AGENT_ROUNDS + 1):
            response = await client.responses.create(
                model=OPENAI_MODEL,
                instructions=INSTRUCTIONS,
                input=input_items,
                previous_response_id=previous_response_id,
                tools=openai_tools,
                parallel_tool_calls=False,
            )
            llm_calls += 1
            tool_calls = [
                item for item in response.output if item.type == "function_call"
            ]

            if not tool_calls:
                return {
                    "question": question,
                    "model": OPENAI_MODEL,
                    "connected_servers": list(sessions),
                    "discovered_tools": sorted(routes),
                    "llm_calls": llm_calls,
                    "trace": trace,
                    "answer": response.output_text,
                }

            call = tool_calls[0]
            route = routes.get(call.name)
            if route is None:
                raise ValueError(f"연결된 MCP Server가 제공하지 않는 Tool입니다: {call.name}")

            arguments = json.loads(call.arguments)
            if not isinstance(arguments, dict):
                raise ValueError("Tool arguments는 JSON Object여야 합니다.")

            result = await sessions[route["server"]].call_tool(
                route["tool"],
                arguments,
            )
            result_text = text_result(result)
            trace.append({
                "round": round_number,
                "server": route["server"],
                "tool": route["tool"],
                "public_tool": call.name,
                "arguments": arguments,
                "is_error": bool(result.isError),
                "result": result_text,
            })

            previous_response_id = response.id
            input_items = [{
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": result_text,
            }]

    raise RuntimeError(f"최대 Agent 반복 횟수({MAX_AGENT_ROUNDS})를 초과했습니다.")


async def main() -> None:
    result = await answer(QUESTION)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
