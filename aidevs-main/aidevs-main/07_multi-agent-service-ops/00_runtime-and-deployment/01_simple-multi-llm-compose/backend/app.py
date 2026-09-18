# [학습] lru_cache는 아래 의존성 생성 함수의 결과를 재사용하여 요청마다 연결 객체를 새로 만들지 않게 한다.
from functools import lru_cache
# [학습] Annotated는 타입에 의존성 정보를 붙이고, Literal은 허용할 문자열 목록을 제한한다.
from typing import Annotated, Literal

# [학습] FastAPI는 라우트를 등록하고 Depends는 필요한 객체를 공급하며 HTTPException은 HTTP 오류를 표현한다.
from fastapi import Depends, FastAPI, HTTPException
# [학습] BaseModel과 Field로 요청 JSON의 필드 타입·길이·형식을 검증한다.
from pydantic import BaseModel, Field

# [학습] 실제 Redis·PostgreSQL·모델 통신은 services 모듈에 맡기고 이 파일은 요청 순서를 조율한다.
from services import MultiLLMChatService, PostgresRepository, RedisSessionStore


# [학습] 이 app 객체를 Dockerfile의 uvicorn app:app이 가져와 HTTP 서버로 제공한다.
app = FahstAPI(title="Multi-LLM Runtime Demo", version="2.0.0")


# [학습] 메모 POST 요청의 입력 계약이다. 두 문자열은 필수이며 빈 문자열과 과도한 길이는 거부된다.
class NoteRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    message: str = Field(min_length=1, max_length=500)


# [학습] 채팅 POST 요청의 입력 계약이다. 검증에 실패하면 chat 함수 실행 전 422 응답이 발생한다.
class ChatRequest(BaseModel):
    # [학습] 세션 식별자는 영문·숫자·밑줄·하이픈만 허용한다. 이것은 형식 검사이며 로그인 인증은 아니다.
    session_id: str = Field(min_length=1, max_length=100, pattern=r"^[a-zA-Z0-9_-]+$")
    message: str = Field(min_length=1, max_length=2000)
    # [학습] provider는 셋 중 하나여야 한다. ollama_model을 생략하면 gemma를 선택한다.
    provider: Literal["openai", "gemini", "ollama"]
    ollama_model: Literal["gemma", "llama"] = "gemma"


# [학습] 데코레이터는 바로 아래 함수를 감싼다. 인수가 없는 함수이므로 프로세스 안에서 같은 객체가 재사용된다.
@lru_cache
def get_redis_store() -> RedisSessionStore:
    return RedisSessionStore()


# [학습] DB 객체도 재사용하지만 실제 DB 연결은 Repository의 각 메서드에서 열고 닫는다.
@lru_cache
def get_database() -> PostgresRepository:
    return PostgresRepository()


# [학습] 모델 서비스 객체의 생성만 캐시한다. 질문별 모델 응답을 캐시하는 기능은 아니다.
@lru_cache
def get_llm() -> MultiLLMChatService:
    return MultiLLMChatService()


# [학습] 라우트 매개변수에 이 타입 별칭을 쓰면 FastAPI가 Depends의 함수를 호출해 객체를 주입한다.
RedisDep = Annotated[RedisSessionStore, Depends(get_redis_store)]
DatabaseDep = Annotated[PostgresRepository, Depends(get_database)]
LLMDep = Annotated[MultiLLMChatService, Depends(get_llm)]


# [학습] GET 경로와 함수를 연결한다. 이 경로는 저장소나 모델을 호출하지 않는 생존 확인이다.
@app.get("/health/live")
def live() -> dict:
    return {"status": "ok", "service": "backend"}


# [학습] 일반 상태 조회는 의존성을 검사하지만 상태가 나빠도 반환 자체의 HTTP 코드는 기본 200이다.
@app.get("/health")
def health(redis_store: RedisDep, database: DatabaseDep, llm: LLMDep) -> dict:
    # [학습] 먼저 실패를 기본값으로 두고, 실제 검사에 성공한 항목을 아래에서 갱신한다.
    checks: dict[str, object] = {
        "backend": True,
        "redis": False,
        "database": False,
        "database_schema": False,
        # [학습] 딕셔너리 컴프리헨션으로 공급자별 설정 여부를 만든다. 키 존재·플래그 검사일 뿐 실제 모델 호출은 아니다.
        "providers": {name: llm.configured(name) for name in llm.PROVIDERS},
    }
    # [학습] errors에는 실패한 의존성만 담는다. 다른 의존성 검사를 계속하기 위해 각각 예외를 잡는다.
    errors = {}
    for name, dependency in (("redis", redis_store), ("database", database)):
        try:
            checks[name] = dependency.ping()
        except Exception as error:
            errors[name] = f"{type(error).__name__}: {error}"
    # [학습] DB에 연결됐을 때만 앱 전용 테이블 존재 여부를 추가 검사한다.
    if checks["database"]:
        try:
            checks["database_schema"] = database.schema_ready()
        except Exception as error:
            errors["database_schema"] = f"{type(error).__name__}: {error}"
    # [학습] 삼항 표현식으로 저장소와 스키마가 모두 준비되면 ok, 하나라도 아니면 degraded를 선택한다.
    return {
        "status": (
            "ok"
            if checks["redis"] and checks["database"] and checks["database_schema"]
            else "degraded"
        ),
        "checks": checks,
        "errors": errors,
    }


# [학습] Compose의 healthcheck가 호출하는 준비 확인 경로다. 위 health의 결과를 HTTP 상태로도 전달한다.
@app.get("/health/ready")
def ready(redis_store: RedisDep, database: DatabaseDep, llm: LLMDep) -> dict:
    """의존성을 포함해 신규 요청을 받을 준비가 됐는지 확인합니다."""
    result = health(redis_store, database, llm)
    # [학습] raise는 정상 반환을 중단한다. HTTPException의 detail에 상세 검사 결과가 들어간다.
    if result["status"] != "ok":
        raise HTTPException(status_code=503, detail=result)
    return result


# [학습] 검증된 payload를 받아 메모 생성 성공 시 201을 반환한다.
@app.post("/api/notes", status_code=201)
def create_note(payload: NoteRequest, redis_store: RedisDep, database: DatabaseDep) -> dict:
    try:
        # [학습] 영구 저장을 먼저 수행한다. 이 호출 실패 시 Redis 통계로 진행하지 않고 503을 반환한다.
        note = database.add_note(payload.name, payload.message)
    except Exception as error:
        # [학습] from error는 원래 예외와 HTTP 오류의 연결을 보존해 원인 추적에 도움을 준다.
        raise HTTPException(status_code=503, detail=f"PostgreSQL 연결 실패: {error}") from error
    # [학습] Redis가 실패해도 메모 저장은 이미 끝났으므로 null 기본값과 warning을 함께 반환할 수 있다.
    warning = None
    request_count = None
    try:
        request_count = redis_store.record_request(payload.message)
    except Exception as error:
        warning = f"메모는 저장했지만 Redis 통계 기록에 실패했습니다: {error}"
    return {"note": note, "request_count": request_count, "warning": warning}


# [학습] 조회는 DB만 필요하다. Repository의 기본 제한으로 최신 메모를 최대 50개 돌려준다.
@app.get("/api/notes")
def get_notes(database: DatabaseDep) -> dict:
    try:
        return {"notes": database.list_notes()}
    except Exception as error:
        raise HTTPException(status_code=503, detail=f"PostgreSQL 연결 실패: {error}") from error


# [학습] Redis 통계 전용 API이며 현재 화면에는 이 경로를 호출하는 버튼이 없다.
@app.get("/api/stats")
def get_stats(redis_store: RedisDep) -> dict:
    try:
        return redis_store.stats()
    except Exception as error:
        raise HTTPException(status_code=503, detail=f"Redis 연결 실패: {error}") from error


# [학습] 대표 채팅 흐름: 설정 확인 → Redis 문맥 → DB 사용자 저장 → 모델 → DB 답변 → Redis 갱신.
@app.post("/api/chat")
def chat(payload: ChatRequest, redis_store: RedisDep, database: DatabaseDep, llm: LLMDep) -> dict:
    # [학습] 선택한 공급자가 설정되지 않았으면 저장과 모델 호출에 들어가기 전에 503으로 중단한다.
    if not llm.configured(payload.provider):
        raise HTTPException(status_code=503, detail=f"{payload.provider} 설정을 확인하세요.")
    # [학습] 아래 작업들은 순차 실행되지만 전체를 묶는 하나의 트랜잭션은 아니다. 중간 실패 때 앞선 DB 저장은 남는다.
    try:
        # [학습] 이전 대화 문맥은 Redis에서 읽는다. PostgreSQL의 전체 기록을 모델에 다시 전달하지 않는다.
        recent = redis_store.load_session(payload.session_id)
        database.add_chat_message(payload.session_id, "user", payload.message)
        # [학습] 일반 동기 함수 호출이다. 작업 큐에 등록하거나 스트리밍하는 코드가 아니다.
        reply = llm.reply(
            payload.provider,
            payload.message,
            recent,
            # [학습] 이름을 지정하는 키워드 인수로 Ollama의 하위 모델 선택을 서비스에 전달한다.
            ollama_model=payload.ollama_model,
        )
        # [학습] 답변을 영구 저장한 다음 두 메시지를 Redis에 함께 추가한다.
        database.add_chat_message(payload.session_id, "assistant", reply.text)
        redis_store.append_session(payload.session_id, [
            {"role": "user", "content": payload.message},
            {"role": "assistant", "content": reply.text},
        ])
        # [학습] 채팅 처리가 끝난 뒤 전역 요청 횟수와 최근 요청을 갱신한다.
        request_count = redis_store.record_request(payload.message)
    # [학습] 저장소나 모델에서 예외가 나면 성공 JSON 대신 503을 돌려준다. 자동 대체 모델 호출은 없다.
    except Exception as error:
        raise HTTPException(status_code=503, detail=f"Chat 처리 실패: {error}") from error
    # [학습] 일반 dict가 JSON 응답이 된다. 별도 response_model은 없으며 fallback_used는 항상 False다.
    return {
        "session_id": payload.session_id,
        "answer": reply.text,
        "provider": reply.provider,
        "model": reply.model,
        "request_count": request_count,
        "fallback_used": False,
    }


# [학습] 중괄호 부분은 URL 경로 인수다. 화면 기록은 Redis가 아닌 PostgreSQL에서 읽는다.
@app.get("/api/chat/{session_id}")
def get_chat_history(session_id: str, database: DatabaseDep) -> dict:
    try:
        return {"session_id": session_id, "messages": database.list_chat(session_id)}
    except Exception as error:
        raise HTTPException(status_code=503, detail=f"PostgreSQL 연결 실패: {error}") from error


# [학습] 새 대화 버튼이 이전 세션의 Redis 문맥만 지운다. DB의 영구 대화 기록은 삭제하지 않는다.
@app.delete("/api/sessions/{session_id}")
def reset_current_session(session_id: str, redis_store: RedisDep) -> dict:
    try:
        redis_store.clear_session(session_id)
    except Exception as error:
        raise HTTPException(status_code=503, detail=f"Redis 연결 실패: {error}") from error
    return {"session_id": session_id, "redis_session_cleared": True, "postgres_history_preserved": True}
