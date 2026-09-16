"""
시나리오
CI Runner에는 실제 OpenAI·Gemini Key와 Open-Meteo 연결이 없습니다. 따라서 Weather MCP와
LLM 응답만 Fake 함수로 교체하고, Backend Agent가 Tool Result를 응답 계약에 포함하는지
확인합니다. 외부 서비스 장애와 무관하게 코드 변경으로 계약이 깨졌는지를 판별합니다.
"""

from fastapi.testclient import TestClient

import app as backend_app


class FakeStateStore:
    def __init__(self): self.values = {}
    def progress(self, run_id, percent, stage, message): self.values[run_id] = {"run_id": run_id, "progress": percent, "stage": stage, "message": message}
    def get_progress(self, run_id): return self.values.get(run_id, {})
    def cached_weather(self, city, day): return None
    def cache_weather(self, city, day, value): print("cache", city, day, value)


class FakeRepository:
    def __init__(self): self.saved = []
    def save(self, run_id, payload, model, tool_result, answer): self.saved.append({"run_id": run_id, "city": payload.city, "model": model})
    def list_runs(self, limit=20): return self.saved


async def fake_weather_tool(city: str, day: str) -> dict:
    return {
        "success": True,
        "city": city,
        "date": "2026-09-09",
        "temperature_max": 24.0,
        "temperature_min": 16.0,
        "precipitation_probability": 20,
        "source": "Fake Open-Meteo",
    }


def fake_generate_answer(provider: str, weather: dict) -> tuple[str, str]:
    return f"{weather['city']}은 가벼운 겉옷이 필요합니다.", "fake-model"


def test_live_health() -> None:
    client = TestClient(backend_app.app)
    response = client.get("/health/live")
    print(response.json())
    assert response.status_code == 200


def test_weather_agent_contract(monkeypatch) -> None:
    fake_state = FakeStateStore()
    fake_repository = FakeRepository()
    monkeypatch.setattr(backend_app, "call_weather_tool", fake_weather_tool)
    monkeypatch.setattr(backend_app, "generate_answer", fake_generate_answer)
    monkeypatch.setattr(backend_app, "state_store", fake_state)
    monkeypatch.setattr(backend_app, "repository", fake_repository)
    client = TestClient(backend_app.app)
    response = client.post(
        "/api/weather",
        json={"city": "서울", "day": "tomorrow", "provider": "openai"},
    )
    started = response.json()
    progress = fake_state.get_progress(started["run_id"])
    result = __import__("json").loads(progress["message"])
    print(started, result)
    assert response.status_code == 202
    assert result["tool"] == "get_weather"
    assert result["tool_result"]["city"] == "서울"
    assert result["model"] == "fake-model"
    assert result["cache_hit"] is False
    assert progress["stage"] == "completed"
    assert len(fake_repository.saved) == 1
