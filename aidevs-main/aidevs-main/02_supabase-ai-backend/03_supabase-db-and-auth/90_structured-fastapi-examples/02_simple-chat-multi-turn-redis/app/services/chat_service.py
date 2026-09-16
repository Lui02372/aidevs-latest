"""Redis List와 TTL로 멀티턴 Gemini 대화를 처리합니다."""

import json
import os
from urllib.parse import quote
from uuid import uuid4

import httpx
from fastapi import HTTPException

import app.core.config  # .env 파일을 읽습니다.
from app.core.gemini import get_gemini_client
from app.schemas.chat_schema import ChatRequest, ChatResponse, ConversationMessage


TTL_SECONDS = 1800
HISTORY_LIMIT = 12


def redis_command(*parts: str) -> dict:
    """Upstash Redis REST API로 Redis 명령을 실행합니다."""

    rest_url = os.getenv("UPSTASH_REDIS_REST_URL")
    rest_token = os.getenv("UPSTASH_REDIS_REST_TOKEN")
    if not rest_url:
        raise HTTPException(500, "UPSTASH_REDIS_REST_URL이 없습니다. .env 파일을 확인하세요.")
    if not rest_token:
        raise HTTPException(500, "UPSTASH_REDIS_REST_TOKEN이 없습니다. .env 파일을 확인하세요.")

    url = f"{rest_url.rstrip('/')}/{'/'.join(quote(part, safe='') for part in parts)}"
    try:
        response = httpx.get(url, headers={"Authorization": f"Bearer {rest_token}"}, timeout=10)
        response.raise_for_status()
    except httpx.HTTPError as error:
        raise HTTPException(502, f"Redis 호출 실패: {error}") from error
    return response.json()


def redis_key(conversation_id: str) -> str:
    return f"ex90:multi-turn:{conversation_id}:messages"


def get_messages(conversation_id: str) -> list[ConversationMessage]:
    """Redis List에서 현재 세션의 대화 문맥을 읽습니다."""

    result = redis_command("lrange", redis_key(conversation_id), "0", "-1")
    return [ConversationMessage(**json.loads(item)) for item in result.get("result", [])]


def save_message(conversation_id: str, role: str, content: str) -> None:
    """메시지를 Redis List 끝에 저장하고 TTL을 다시 30분으로 설정합니다."""

    key = redis_key(conversation_id)
    redis_command("rpush", key, json.dumps({"role": role, "content": content}))
    redis_command("expire", key, str(TTL_SECONDS))


def make_prompt(history: list[ConversationMessage], message: str) -> str:
    """최근 대화와 새 질문을 Gemini 프롬프트로 만듭니다."""

    lines = ["당신은 초보자에게 쉽게 설명하는 AI 도우미입니다."]
    for item in history[-HISTORY_LIMIT:]:
        speaker = "사용자" if item.role == "user" else "AI"
        lines.append(f"{speaker}: {item.content}")
    lines.append(f"사용자: {message}")
    lines.append("AI:")
    return "\n".join(lines)


def create_gemini_answer(prompt: str) -> tuple[str, str]:
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    client = get_gemini_client()
    try:
        response = client.models.generate_content(model=model, contents=prompt)
    except Exception as error:
        raise HTTPException(502, f"Gemini 호출 실패: {error}") from error
    return response.text or "", model


def chat(request: ChatRequest) -> ChatResponse:
    """Redis의 이전 문맥을 사용해 Gemini 답변을 만들고 세션을 갱신합니다."""

    conversation_id = str(request.conversation_id) if request.conversation_id else str(uuid4())
    history = get_messages(conversation_id)
    answer, model = create_gemini_answer(make_prompt(history, request.message))
    save_message(conversation_id, "user", request.message)
    save_message(conversation_id, "assistant", answer)

    return ChatResponse(
        conversation_id=conversation_id,
        user_message=request.message,
        assistant_message=answer,
        model=model,
        context_messages=len(history),
        ttl_seconds=TTL_SECONDS,
    )


def clear_conversation(conversation_id: str) -> int:
    """Redis에 저장된 대화 세션을 삭제합니다."""

    return int(redis_command("del", redis_key(conversation_id)).get("result", 0))
