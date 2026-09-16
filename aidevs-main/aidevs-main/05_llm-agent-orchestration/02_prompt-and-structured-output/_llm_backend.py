"""Prompt 실험 예제가 공통으로 사용하는 Mini Agent 02 API Client입니다."""

import os
from typing import Any

import httpx
from dotenv import load_dotenv


load_dotenv()
# 모든 실험이 같은 Backend와 Provider를 사용해야 Prompt만 공정하게 비교할 수 있습니다.
BASE_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000")
PROVIDER = os.getenv("PROMPT_EXAMPLE_PROVIDER", "openai")


def generate_text(system_prompt: str, message: str) -> dict[str, Any]:
    # Provider SDK를 예제마다 반복하지 않고 Mini Agent의 공통 API를 호출합니다.
    response = httpx.post(
        f"{BASE_URL}/api/generate",
        json={
            "provider": PROVIDER,
            "system_prompt": system_prompt,
            "message": message,
        },
        timeout=90,
    )
    response.raise_for_status()  # 4xx·5xx를 정상 결과처럼 비교하지 않도록 즉시 실패시킵니다.
    return response.json()


def generate_structured(
    schema_type: str, system_prompt: str, message: str
) -> dict[str, Any]:
    # 자유 응답과 달리 Schema 종류까지 Backend에 전달합니다.
    response = httpx.post(
        f"{BASE_URL}/api/structured/generate",
        json={
            "provider": PROVIDER,
            "schema_type": schema_type,
            "system_prompt": system_prompt,
            "message": message,
        },
        timeout=90,
    )
    response.raise_for_status()
    return response.json()


def print_result(label: str, result: dict[str, Any]) -> None:
    print(f"\n===== {label} =====")
    print(f"{result['provider']} · {result['model']} · {result['latency_ms']}ms")
    print(result["content"])


def print_connection_help(error: httpx.HTTPError) -> None:
    print("Mini Agent 02 Backend 호출 실패:", error)
    print("Backend를 실행하고 BACKEND_API_URL을 확인하세요.")
    print("실제 차이를 보려면 PROMPT_EXAMPLE_PROVIDER를 gemini, openai, ollama 중 하나로 설정하세요.")
