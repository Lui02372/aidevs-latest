"""
[시나리오]
운영 화면에서 Agent가 어떤 Provider를 사용하는지와 실행 준비 여부를 확인합니다.

1. Supervisor와 Budget Agent는 OpenAI Key가 있는지 확인합니다.
2. Weather와 Itinerary Agent는 Gemini Key가 있는지 확인합니다.
3. Place Agent는 실제 Ollama `/api/tags`에 연결해 Llama 설치 여부를 확인합니다.
4. 상태 확인은 LLM 답변을 생성하지 않으므로 Token을 사용하지 않습니다.

[기대 결과]
각 Agent의 Provider·Model·configured 또는 reachable 상태가 출력됩니다. 연결 실패를
항상 정상으로 바꾸지 않고 오류를 그대로 표시합니다.

[학습 포인트]
Agent 상태와 Provider 상태는 다릅니다. Agent 코드는 준비되어 있어도 API Key나
로컬 Model이 없으면 실제 요청을 처리할 수 없습니다.
"""

import os

import httpx
from dotenv import load_dotenv


load_dotenv()

agent_providers = {
    "supervisor_agent": ("openai", os.getenv("OPENAI_MODEL", "gpt-4.1-mini")),
    "weather_agent": ("gemini", os.getenv("GEMINI_MODEL", "gemini-3.5-flash")),
    "place_agent": ("ollama", os.getenv("OLLAMA_MODEL", "llama3.2")),
    "budget_agent": ("openai", os.getenv("OPENAI_MODEL", "gpt-4.1-mini")),
    "itinerary_agent": ("gemini", os.getenv("GEMINI_MODEL", "gemini-3.5-flash")),
}


def provider_status_agent(agent_id: str, provider: str, model: str) -> dict[str, object]:
    if provider == "openai":
        return {"agent": agent_id, "provider": provider, "model": model, "configured": bool(os.getenv("OPENAI_API_KEY"))}
    if provider == "gemini":
        return {"agent": agent_id, "provider": provider, "model": model, "configured": bool(os.getenv("GEMINI_API_KEY"))}
    try:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
        response = httpx.get(f"{base_url}/api/tags", timeout=3)
        response.raise_for_status()
        models = [item["name"] for item in response.json().get("models", [])]
        installed = any(name == model or name.startswith(f"{model}:") for name in models)
        return {"agent": agent_id, "provider": provider, "model": model, "reachable": True, "model_installed": installed}
    except Exception as error:
        return {"agent": agent_id, "provider": provider, "model": model, "reachable": False, "error": str(error)}


for agent_id, provider_and_model in agent_providers.items():
    provider, model = provider_and_model
    print(provider_status_agent(agent_id, provider, model))
