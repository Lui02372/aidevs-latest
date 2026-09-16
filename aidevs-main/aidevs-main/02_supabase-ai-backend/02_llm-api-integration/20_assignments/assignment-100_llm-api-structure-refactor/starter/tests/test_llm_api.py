r"""LLM API 구조 분리 과제 테스트입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\02_llm-api-integration\20_assignments\assignment-100_llm-api-structure-refactor\starter
    python -m pytest -s

처음에는 TODO가 남아 있어 실패할 수 있습니다. 실패 메시지를 보고 코드를 완성합니다.
"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    print("1. GET /health 상태 확인 API를 호출합니다.")
    response = client.get("/health")

    print("   응답:", response.status_code, response.json())
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_single_turn_chat():
    print("2. POST /ai/chat single-turn API를 호출합니다.")
    response = client.post(
        "/ai/chat",
        json={
            "message": "FastAPI에서 Pydantic을 왜 사용하나요?",
            "memo_context": "Pydantic은 요청 데이터를 검증합니다.",
        },
    )

    print("   응답:", response.status_code, response.json())
    assert response.status_code == 200
    body = response.json()
    assert body["provider"] == "gemini"
    assert body["model"] == "gemini-2.5-flash-lite"
    assert body["actual_api_called"] is False
    assert "Pydantic" in body["answer"]
    assert len(body["messages_for_storage"]) == 2
    assert body["messages_for_storage"][0]["role"] == "user"
    assert body["messages_for_storage"][1]["role"] == "assistant"


def test_multi_turn_chat_with_history():
    print("3. POST /ai/chat-with-history multi-turn API를 호출합니다.")
    response = client.post(
        "/ai/chat-with-history",
        json={
            "message": "그 내용을 한 문장으로 요약해줘.",
            "history": [
                {"role": "user", "content": "LLM API의 message 구조를 배웠어."},
                {"role": "assistant", "content": "role과 content를 구분하는 것이 핵심입니다."},
            ],
        },
    )

    print("   응답:", response.status_code, response.json())
    assert response.status_code == 200
    body = response.json()
    assert body["actual_api_called"] is False
    assert "요약" in body["answer"] or "한 문장" in body["answer"]
    assert len(body["messages_for_storage"]) == 4
    assert body["messages_for_storage"][-2]["role"] == "user"
    assert body["messages_for_storage"][-1]["role"] == "assistant"
