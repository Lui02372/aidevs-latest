import asyncio
import json
from contextlib import asynccontextmanager
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

import app as backend
from test_app import FakeRepository, FakeStateStore, fake_weather_tool, fake_guide


def test_openai_uses_resource_and_skill(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "test-model")
    def create(**kwargs):
        assert kwargs["model"] == "test-model"
        assert "날씨 브리핑 절차" in kwargs["input"]
        assert "섭씨 안내 resource" in kwargs["input"]
        assert "서울" in kwargs["input"]
        return SimpleNamespace(output_text="서울 날씨입니다.")
    monkeypatch.setattr(backend, "OpenAI", lambda: SimpleNamespace(responses=SimpleNamespace(create=create)))
    assert backend.generate_answer("openai", {"city": "서울"}, "섭씨 안내 resource") == ("서울 날씨입니다.", "test-model")


def test_openai_missing_key_reports_configuration_error(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        backend.generate_answer("openai", {}, "guide")


def test_bedrock_is_not_an_accepted_provider():
    response = TestClient(backend.app).post("/api/weather", json={"city": "서울", "provider": "bedrock"})
    assert response.status_code == 422
    assert backend.WeatherRequest(city="서울").provider == "openai"


def test_gemini_uses_resource_and_skill(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("GEMINI_MODEL", "test-gemini")
    def generate_content(**kwargs):
        assert kwargs["model"] == "test-gemini"
        assert "날씨 브리핑 절차" in kwargs["contents"]
        assert "resource guide" in kwargs["contents"]
        return SimpleNamespace(text="날씨 답변")
    monkeypatch.setattr(backend.genai, "Client", lambda **kwargs: SimpleNamespace(models=SimpleNamespace(generate_content=generate_content)))
    assert backend.generate_answer("gemini", {"city": "서울"}, "resource guide") == ("날씨 답변", "test-gemini")


def test_resource_read_contract(monkeypatch):
    class Session:
        async def read_resource(self, uri):
            assert uri == "weather://guide/forecast"
            return SimpleNamespace(contents=[SimpleNamespace(text="resource text")])
    @asynccontextmanager
    async def session(): yield Session()
    monkeypatch.setattr(backend, "mcp_session", session)
    assert asyncio.run(backend.read_weather_guide()) == "resource text"


def test_resource_failure_marks_run_failed_and_does_not_save(monkeypatch):
    state, repo = FakeStateStore(), FakeRepository()
    async def broken_guide(): raise RuntimeError("resource offline")
    monkeypatch.setattr(backend, "state_store", state)
    monkeypatch.setattr(backend, "repository", repo)
    monkeypatch.setattr(backend, "call_weather_tool", fake_weather_tool)
    monkeypatch.setattr(backend, "read_weather_guide", broken_guide)
    response = TestClient(backend.app).post("/api/weather", json={"city": "서울", "provider": "openai"})
    progress = state.get_progress(response.json()["run_id"])
    assert progress["stage"] == "failed"
    assert "resource offline" in progress["message"]
    assert repo.saved == []


def test_cache_hit_skips_tool_but_reads_resource(monkeypatch):
    state, repo = FakeStateStore(), FakeRepository()
    state.cached_weather = lambda *args: {"success": True, "city": "서울"}
    async def forbidden(*args): raise AssertionError("cache hit must not call tool")
    monkeypatch.setattr(backend, "state_store", state)
    monkeypatch.setattr(backend, "repository", repo)
    monkeypatch.setattr(backend, "call_weather_tool", forbidden)
    monkeypatch.setattr(backend, "read_weather_guide", fake_guide)
    def answer(provider, weather, guide):
        assert guide == "기온은 섭씨, 강수는 확률입니다."
        return "답변", "fake"
    monkeypatch.setattr(backend, "generate_answer", answer)
    response = TestClient(backend.app).post("/api/weather", json={"city": "서울"})
    progress = state.get_progress(response.json()["run_id"])
    assert progress["stage"] == "completed"
    assert json.loads(progress["message"])["cache_hit"] is True
    assert len(repo.saved) == 1


def test_mcp_server_registers_tool_and_resource():
    import importlib.util
    from pathlib import Path
    path = Path(__file__).parents[1] / "mcp_server" / "server.py"
    spec = importlib.util.spec_from_file_location("weather07_server", path)
    server = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(server)
    async def inspect():
        assert "get_weather" in [tool.name for tool in await server.mcp.list_tools()]
        assert backend.RESOURCE_URI in [str(resource.uri) for resource in await server.mcp.list_resources()]
        result = await server.mcp.read_resource(backend.RESOURCE_URI)
        assert list(result)
    asyncio.run(inspect())


def test_real_mcp_http_resource_roundtrip():
    import importlib.util
    from pathlib import Path
    spec = importlib.util.spec_from_file_location("weather07_http", Path(__file__).parents[1] / "mcp_server" / "server.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    headers = {"Accept": "application/json, text/event-stream"}
    with TestClient(module.mcp.streamable_http_app(), base_url="http://weather-mcp:8010") as client:
        init = client.post("/mcp", headers=headers, json={"jsonrpc": "2.0", "id": 1,
            "method": "initialize", "params": {"protocolVersion": "2025-03-26", "capabilities": {},
            "clientInfo": {"name": "test", "version": "1"}}})
        assert init.status_code == 200
        assert "resources" in init.json()["result"]["capabilities"]
        response = client.post("/mcp", headers=headers, json={"jsonrpc": "2.0", "id": 2,
            "method": "resources/read", "params": {"uri": backend.RESOURCE_URI}})
        assert response.status_code == 200
        assert "Open-Meteo" in response.json()["result"]["contents"][0]["text"]
