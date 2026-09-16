#ai_agent.py


import asyncio
import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import AsyncOpenAI

from _stdio_client import connect_to_travel_server


ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
INSTRUCTIONS = (
    "당신은 한국 여행 도우미입니다. 사용자 요청에 필요한 Tool을 모두 호출하기 "
    "전에는 최종 답변을 작성하지 마세요. 날씨와 호텔을 함께 요청하면 두 Tool을 "
    "모두 호출하세요. Tool 결과만 근거로 한국어 최종 답변을 작성하세요."
)


def to_openai_tool(tool) -> dict[str, Any]:
    """MCP Tool Schema를 OpenAI Responses API의 Function Tool로 변환합니다."""
    raw = tool.model_dump(by_alias=True)
    return {
        "type": "function",
        "name": tool.name,
        "description": tool.description or "",
        "parameters": raw["inputSchema"],
        "strict": False,
    }


def text_result(result) -> str:
    return "\n".join(
        content.text for content in result.content if hasattr(content, "text")
    )


async def answer(question: str) -> dict[str, Any]:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY가 필요합니다.")

    trace: list[dict[str, Any]] = []

    async with AsyncOpenAI() as client, connect_to_travel_server() as session:
        discovered = (await session.list_tools()).tools
        available = {tool.name for tool in discovered}
        openai_tools = [to_openai_tool(tool) for tool in discovered]
        response = await client.responses.create(
            model=OPENAI_MODEL,
            instructions=INSTRUCTIONS,
            input=question,
            tools=openai_tools,
            parallel_tool_calls=True,
        )

        tool_calls = [item for item in response.output if item.type == "function_call"]
        if not tool_calls:
            return {
                "question": question,
                "model": OPENAI_MODEL,
                "discovered_tools": sorted(available),
                "llm_calls": 1,
                "trace": trace,
                "answer": response.output_text,
            }

        tool_outputs = []
        for call in tool_calls:
            if call.name not in available:
                raise ValueError(f"MCP Server가 제공하지 않는 Tool입니다: {call.name}")
            arguments = json.loads(call.arguments)
            if not isinstance(arguments, dict):
                raise ValueError("Tool arguments는 JSON Object여야 합니다.")

            result = await session.call_tool(call.name, arguments)
            result_text = text_result(result)
            trace.append({
                "tool": call.name,
                "arguments": arguments,
                "is_error": bool(result.isError),
                "result": result_text,
            })
            tool_outputs.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": result_text,
            })

        final_response = await client.responses.create(
            model=OPENAI_MODEL,
            instructions=INSTRUCTIONS,
            previous_response_id=response.id,
            input=tool_outputs,
        )
        return {
            "question": question,
            "model": OPENAI_MODEL,
            "discovered_tools": sorted(available),
            "llm_calls": 2,
            "trace": trace,
            "answer": final_response.output_text,
        }


async def main() -> None:
    # result = await answer("부산 날씨 알려주세요.")
    # result = await answer("부산 날씨와 15만원 이하 호텔을 찾아 주세요.")
    # result = await answer("부산에서 15만원 이하 호텔을 찾아 주세요.")
    result = await answer("부산 강변이 보이는 호텔을 찾아줘.")

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
