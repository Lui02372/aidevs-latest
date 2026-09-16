from fastapi.testclient import TestClient

from app import app, get_database, get_llm, get_redis_store
from services import LLMReply


class FakeRedis:
    def __init__(self) -> None:
        self.count = 0
        self.sessions = {}

    def ping(self): return True
    def record_request(self, text): self.count += 1; return self.count
    def stats(self): return {"request_count": self.count, "recent_request": None}
    def load_session(self, session_id): return list(self.sessions.get(session_id, []))
    def append_session(self, session_id, messages): self.sessions.setdefault(session_id, []).extend(messages)
    def clear_session(self, session_id): self.sessions.pop(session_id, None)


class FakeDatabase:
    def __init__(self) -> None:
        self.notes, self.messages = [], []

    def ping(self): return True
    def schema_ready(self): return True
    def add_note(self, name, message):
        item = {"id": len(self.notes) + 1, "name": name, "message": message}; self.notes.append(item); return item
    def list_notes(self, limit=50): return list(reversed(self.notes))[:limit]
    def add_chat_message(self, session_id, role, content):
        item = {"id": len(self.messages) + 1, "session_id": session_id, "role": role, "content": content}; self.messages.append(item); return item
    def list_chat(self, session_id, limit=100): return [item for item in self.messages if item["session_id"] == session_id][:limit]


class FakeLLM:
    PROVIDERS = ("openai", "gemini", "ollama")
    def configured(self, provider): return provider != "ollama"
    def reply(self, provider, message, recent, ollama_model="gemma"):
        model = ollama_model if provider == "ollama" else f"{provider}-test"
        return LLMReply(provider, model, f"실제 계약 테스트: {message}")


fake_redis, fake_database = FakeRedis(), FakeDatabase()
app.dependency_overrides[get_redis_store] = lambda: fake_redis
app.dependency_overrides[get_database] = lambda: fake_database
app.dependency_overrides[get_llm] = lambda: FakeLLM()
client = TestClient(app)


def test_health_shows_each_provider() -> None:
    result = client.get("/health").json()
    assert result["checks"]["providers"] == {"openai": True, "gemini": True, "ollama": False}


def test_selected_provider_is_visible_and_history_is_saved() -> None:
    result = client.post("/api/chat", json={
        "session_id": "travel-01", "message": "부산 여행 준비를 알려줘", "provider": "gemini",
    })
    assert result.status_code == 200
    assert result.json()["provider"] == "gemini"
    assert result.json()["fallback_used"] is False
    assert len(client.get("/api/chat/travel-01").json()["messages"]) == 2


def test_unconfigured_provider_is_not_replaced_with_mock() -> None:
    result = client.post("/api/chat", json={
        "session_id": "travel-02", "message": "질문", "provider": "ollama",
    })
    assert result.status_code == 503
    assert "ollama" in result.json()["detail"]
