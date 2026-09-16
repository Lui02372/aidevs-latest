r"""Backend를 통해 GPT, Gemini, Ollama/Llama를 같은 방식으로 호출합니다.

실행 전 준비:
    cd C:\mini_agent_st\mini_agent_01_llm\backend
    uvicorn app.main:app --reload --port 8000

다른 주소를 사용하면 PYTHON_AGENT_API_URL 환경 변수로 지정합니다.
"""

import os

import httpx
from dotenv import load_dotenv


load_dotenv()
BASE_URL = os.getenv("PYTHON_AGENT_API_URL", "http://127.0.0.1:8000")

# 이전 과정에서 사용한 Gemini를 기준점으로 삼고 GPT, Local Llama 순서로 비교합니다.
for provider in ("gemini", "openai", "ollama"):
    try:
        response = httpx.post(
            f"{BASE_URL}/api/generate",
            json={
                "provider": provider,
                "message": "부산 2박 여행을 준비할 때 먼저 확인할 것은 무엇인가요?",
            },
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        print(provider, data["model"], data["latency_ms"], data["content"])
    except httpx.HTTPError as error:
        print(provider, "호출 실패:", error)
