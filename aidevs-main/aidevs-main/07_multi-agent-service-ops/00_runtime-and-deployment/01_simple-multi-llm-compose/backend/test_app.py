# [학습] TestClient는 실제 포트를 열지 않고 FastAPI 앱에 요청하는 테스트용 클라이언트다.
from fastapi.testclient import TestClient

# [학습] 라우트 앱과 의존성 생성 함수를 가져와 실제 저장소 대신 아래 가짜 객체로 바꾼다.
from app import app, get_database, get_llm, get_redis_store
# [학습] 가짜 모델도 실제 서비스와 같은 LLMReply 반환 계약을 사용한다.
from services import LLMReply


# [학습] Redis의 일부 동작을 메모리에서 흉내 낸다. 네트워크·TTL·Redis 장애까지 검사하는 구현은 아니다.
class FakeRedis:
    # [학습] 각 객체의 상태로 횟수와 세션 사전을 저장한다.
    def __init__(self) -> None:
        self.count = 0
        self.sessions = {}

    # [학습] 한 줄 메서드도 일반 함수다. 세미콜론은 같은 줄의 문장을 나누며 원래 코드를 그대로 유지한다.
    def ping(self): return True
    def record_request(self, text): self.count += 1; return self.count
    def stats(self): return {"request_count": self.count, "recent_request": None}
    # [학습] 기록이 없으면 빈 목록을 복사해 반환한다. setdefault로 목록을 준비하고 extend로 여러 메시지를 추가한다.
    def load_session(self, session_id): return list(self.sessions.get(session_id, []))
    def append_session(self, session_id, messages): self.sessions.setdefault(session_id, []).extend(messages)
    # [학습] pop의 기본값 None 덕분에 없는 세션 삭제도 예외를 내지 않는다.
    def clear_session(self, session_id): self.sessions.pop(session_id, None)


# [학습] 실제 SQL 대신 리스트를 사용하므로 DB 연결·SQL 문법·트랜잭션을 확인하는 테스트는 아니다.
class FakeDatabase:
    def __init__(self) -> None:
        # [학습] 튜플 대입으로 서로 다른 빈 리스트를 notes와 messages에 각각 할당한다.
        self.notes, self.messages = [], []

    # [학습] 상태 검사 두 개는 항상 참이다. 저장 메서드는 목록 길이로 ID를 만들고 같은 항목을 반환한다.
    def ping(self): return True
    def schema_ready(self): return True
    def add_note(self, name, message):
        item = {"id": len(self.notes) + 1, "name": name, "message": message}; self.notes.append(item); return item
    # [학습] reversed와 슬라이스로 최신 메모부터 제한 개수만 반환한다.
    def list_notes(self, limit=50): return list(reversed(self.notes))[:limit]
    # [학습] 대화 메시지를 메모리 목록에 추가한 뒤 세션 ID로 필터링하여 조회한다.
    def add_chat_message(self, session_id, role, content):
        item = {"id": len(self.messages) + 1, "session_id": session_id, "role": role, "content": content}; self.messages.append(item); return item
    def list_chat(self, session_id, limit=100): return [item for item in self.messages if item["session_id"] == session_id][:limit]


# [학습] 가짜 LLM은 외부 호출을 하지 않는다. 테스트용으로 Ollama만 미설정 상태를 흉내 낸다.
class FakeLLM:
    PROVIDERS = ("openai", "gemini", "ollama")
    def configured(self, provider): return provider != "ollama"
    def reply(self, provider, message, recent, ollama_model="gemma"):
        # [학습] 조건 표현식과 f-string으로 공급자를 알아볼 수 있는 고정 응답을 만든다.
        model = ollama_model if provider == "ollama" else f"{provider}-test"
        return LLMReply(provider, model, f"실제 계약 테스트: {message}")


# [학습] 파일 전체 테스트가 가짜 객체를 공유한다. 각 테스트마다 초기화하는 fixture는 없다.
fake_redis, fake_database = FakeRedis(), FakeDatabase()
# [학습] dependency_overrides는 Depends가 호출할 함수를 교체한다. lambda는 값을 돌려주는 짧은 익명 함수다.
app.dependency_overrides[get_redis_store] = lambda: fake_redis
app.dependency_overrides[get_database] = lambda: fake_database
app.dependency_overrides[get_llm] = lambda: FakeLLM()
# [학습] 오버라이드 설정 후 클라이언트를 만들므로 아래 요청은 메모리의 가짜 의존성을 사용한다.
client = TestClient(app)


# [학습] 공급자별 설정 상태가 API 응답의 올바른 위치에 있는지 assert로 확인한다.
def test_health_shows_each_provider() -> None:
    result = client.get("/health").json()
    assert result["checks"]["providers"] == {"openai": True, "gemini": True, "ollama": False}


# [학습] 채팅 성공 HTTP 코드·선택 공급자·대체 없음·질문과 답변 두 행 저장을 함께 확인한다.
def test_selected_provider_is_visible_and_history_is_saved() -> None:
    result = client.post("/api/chat", json={
        "session_id": "travel-01", "message": "부산 여행 준비를 알려줘", "provider": "gemini",
    })
    assert result.status_code == 200
    assert result.json()["provider"] == "gemini"
    assert result.json()["fallback_used"] is False
    assert len(client.get("/api/chat/travel-01").json()["messages"]) == 2


# [학습] 미설정 공급자를 선택하면 가짜 성공 대신 503과 공급자 이름을 반환하는지 확인한다.
def test_unconfigured_provider_is_not_replaced_with_mock() -> None:
    result = client.post("/api/chat", json={
        "session_id": "travel-02", "message": "질문", "provider": "ollama",
    })
    assert result.status_code == 503
    assert "ollama" in result.json()["detail"]
