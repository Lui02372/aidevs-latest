from fastapi.testclient import TestClient

from app.main import app
from app.routers import chat_router
from app.schemes.chat_scheme import ChatResponse


client = TestClient(app)


def test_chat_gemini_returns_service_response(monkeypatch):
    def fake_call_gemini(request):
        assert request.user_id == "user-1"
        assert request.prompt == "Hello"
        return ChatResponse(answer="Mocked Gemini answer")

    monkeypatch.setattr(chat_router, "call_gemini", fake_call_gemini)

    response = client.post(
        "/chat/gemini",
        json={"user_id": "user-1", "prompt": "Hello"},
    )

    assert response.status_code == 200
    assert response.json() == {"answer": "Mocked Gemini answer"}


def test_chat_gemini_rejects_empty_prompt():
    response = client.post(
        "/chat/gemini",
        json={"user_id": "user-1", "prompt": ""},
    )

    assert response.status_code == 422
