from functools import lru_cache
from typing import Annotated, Literal

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

from services import MultiLLMChatService, PostgresRepository, RedisSessionStore


app = FastAPI(title="Multi-LLM Runtime Demo", version="2.0.0")


class NoteRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    message: str = Field(min_length=1, max_length=500)


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=100, pattern=r"^[a-zA-Z0-9_-]+$")
    message: str = Field(min_length=1, max_length=2000)
    provider: Literal["openai", "gemini", "ollama"]
    ollama_model: Literal["gemma", "llama"] = "gemma"


@lru_cache
def get_redis_store() -> RedisSessionStore:
    return RedisSessionStore()


@lru_cache
def get_database() -> PostgresRepository:
    return PostgresRepository()


@lru_cache
def get_llm() -> MultiLLMChatService:
    return MultiLLMChatService()


RedisDep = Annotated[RedisSessionStore, Depends(get_redis_store)]
DatabaseDep = Annotated[PostgresRepository, Depends(get_database)]
LLMDep = Annotated[MultiLLMChatService, Depends(get_llm)]


@app.get("/health/live")
def live() -> dict:
    return {"status": "ok", "service": "backend"}


@app.get("/health")
def health(redis_store: RedisDep, database: DatabaseDep, llm: LLMDep) -> dict:
    checks: dict[str, object] = {
        "backend": True,
        "redis": False,
        "database": False,
        "database_schema": False,
        "providers": {name: llm.configured(name) for name in llm.PROVIDERS},
    }
    errors = {}
    for name, dependency in (("redis", redis_store), ("database", database)):
        try:
            checks[name] = dependency.ping()
        except Exception as error:
            errors[name] = f"{type(error).__name__}: {error}"
    if checks["database"]:
        try:
            checks["database_schema"] = database.schema_ready()
        except Exception as error:
            errors["database_schema"] = f"{type(error).__name__}: {error}"
    return {
        "status": (
            "ok"
            if checks["redis"] and checks["database"] and checks["database_schema"]
            else "degraded"
        ),
        "checks": checks,
        "errors": errors,
    }


@app.get("/health/ready")
def ready(redis_store: RedisDep, database: DatabaseDep, llm: LLMDep) -> dict:
    """의존성을 포함해 신규 요청을 받을 준비가 됐는지 확인합니다."""
    result = health(redis_store, database, llm)
    if result["status"] != "ok":
        raise HTTPException(status_code=503, detail=result)
    return result


@app.post("/api/notes", status_code=201)
def create_note(payload: NoteRequest, redis_store: RedisDep, database: DatabaseDep) -> dict:
    try:
        note = database.add_note(payload.name, payload.message)
    except Exception as error:
        raise HTTPException(status_code=503, detail=f"PostgreSQL 연결 실패: {error}") from error
    warning = None
    request_count = None
    try:
        request_count = redis_store.record_request(payload.message)
    except Exception as error:
        warning = f"메모는 저장했지만 Redis 통계 기록에 실패했습니다: {error}"
    return {"note": note, "request_count": request_count, "warning": warning}


@app.get("/api/notes")
def get_notes(database: DatabaseDep) -> dict:
    try:
        return {"notes": database.list_notes()}
    except Exception as error:
        raise HTTPException(status_code=503, detail=f"PostgreSQL 연결 실패: {error}") from error


@app.get("/api/stats")
def get_stats(redis_store: RedisDep) -> dict:
    try:
        return redis_store.stats()
    except Exception as error:
        raise HTTPException(status_code=503, detail=f"Redis 연결 실패: {error}") from error


@app.post("/api/chat")
def chat(payload: ChatRequest, redis_store: RedisDep, database: DatabaseDep, llm: LLMDep) -> dict:
    if not llm.configured(payload.provider):
        raise HTTPException(status_code=503, detail=f"{payload.provider} 설정을 확인하세요.")
    try:
        recent = redis_store.load_session(payload.session_id)
        database.add_chat_message(payload.session_id, "user", payload.message)
        reply = llm.reply(
            payload.provider,
            payload.message,
            recent,
            ollama_model=payload.ollama_model,
        )
        database.add_chat_message(payload.session_id, "assistant", reply.text)
        redis_store.append_session(payload.session_id, [
            {"role": "user", "content": payload.message},
            {"role": "assistant", "content": reply.text},
        ])
        request_count = redis_store.record_request(payload.message)
    except Exception as error:
        raise HTTPException(status_code=503, detail=f"Chat 처리 실패: {error}") from error
    return {
        "session_id": payload.session_id,
        "answer": reply.text,
        "provider": reply.provider,
        "model": reply.model,
        "request_count": request_count,
        "fallback_used": False,
    }


@app.get("/api/chat/{session_id}")
def get_chat_history(session_id: str, database: DatabaseDep) -> dict:
    try:
        return {"session_id": session_id, "messages": database.list_chat(session_id)}
    except Exception as error:
        raise HTTPException(status_code=503, detail=f"PostgreSQL 연결 실패: {error}") from error


@app.delete("/api/sessions/{session_id}")
def reset_current_session(session_id: str, redis_store: RedisDep) -> dict:
    try:
        redis_store.clear_session(session_id)
    except Exception as error:
        raise HTTPException(status_code=503, detail=f"Redis 연결 실패: {error}") from error
    return {"session_id": session_id, "redis_session_cleared": True, "postgres_history_preserved": True}
