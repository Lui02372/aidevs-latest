from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

import httpx
import psycopg
import redis
from psycopg.rows import dict_row


@dataclass(frozen=True)
class LLMReply:
    provider: str
    model: str
    text: str


class RedisSessionStore:
    def __init__(self, url: str | None = None, ttl_seconds: int = 1800) -> None:
        self.client = redis.from_url(
            url or os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0"),
            decode_responses=True,
        )
        self.ttl_seconds = ttl_seconds

    def ping(self) -> bool:
        return bool(self.client.ping())

    def record_request(self, text: str) -> int:
        count = int(self.client.incr("runtime_demo:request_count"))
        self.client.set("runtime_demo:recent_request", text, ex=self.ttl_seconds)
        return count

    def stats(self) -> dict[str, Any]:
        return {
            "request_count": int(self.client.get("runtime_demo:request_count") or 0),
            "recent_request": self.client.get("runtime_demo:recent_request"),
        }

    def load_session(self, session_id: str) -> list[dict[str, str]]:
        key = f"runtime_demo:session:{session_id}"
        return [json.loads(item) for item in self.client.lrange(key, 0, -1)]

    def append_session(self, session_id: str, messages: list[dict[str, str]]) -> None:
        key = f"runtime_demo:session:{session_id}"
        if messages:
            self.client.rpush(key, *[json.dumps(item, ensure_ascii=False) for item in messages])
        self.client.ltrim(key, -12, -1)
        self.client.expire(key, self.ttl_seconds)

    def clear_session(self, session_id: str) -> None:
        self.client.delete(f"runtime_demo:session:{session_id}")


class PostgresRepository:
    def __init__(self, url: str | None = None) -> None:
        self.url = url or os.getenv(
            "DATABASE_URL",
            "postgresql://agent_user:agent_pwd@127.0.0.1:5433/agent_db",
        )

    def ping(self) -> bool:
        with psycopg.connect(self.url) as connection, connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            return cursor.fetchone() == (1,)

    def schema_ready(self) -> bool:
        """이 Application이 사용하는 Schema와 두 Table이 모두 있는지 확인합니다."""
        with psycopg.connect(self.url) as connection, connection.cursor() as cursor:
            cursor.execute(
                """SELECT
                       to_regclass('simple_multi_llm.notes') IS NOT NULL
                       AND to_regclass('simple_multi_llm.chat_messages') IS NOT NULL"""
            )
            return cursor.fetchone() == (True,)

    def add_note(self, name: str, message: str) -> dict[str, Any]:
        with psycopg.connect(self.url, row_factory=dict_row) as connection, connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO simple_multi_llm.notes (name, message) VALUES (%s, %s) RETURNING id, name, message, created_at",
                (name, message),
            )
            return dict(cursor.fetchone())

    def list_notes(self, limit: int = 50) -> list[dict[str, Any]]:
        with psycopg.connect(self.url, row_factory=dict_row) as connection, connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, message, created_at FROM simple_multi_llm.notes ORDER BY id DESC LIMIT %s",
                (limit,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def add_chat_message(self, session_id: str, role: str, content: str) -> dict[str, Any]:
        with psycopg.connect(self.url, row_factory=dict_row) as connection, connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO simple_multi_llm.chat_messages (session_id, role, content) VALUES (%s, %s, %s) RETURNING id, session_id, role, content, created_at",
                (session_id, role, content),
            )
            return dict(cursor.fetchone())

    def list_chat(self, session_id: str, limit: int = 100) -> list[dict[str, Any]]:
        with psycopg.connect(self.url, row_factory=dict_row) as connection, connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, session_id, role, content, created_at FROM simple_multi_llm.chat_messages WHERE session_id = %s ORDER BY id ASC LIMIT %s",
                (session_id, limit),
            )
            return [dict(row) for row in cursor.fetchall()]


class MultiLLMChatService:
    """실제 Provider를 명시적으로 선택합니다. 자동 Mock Fallback은 없습니다."""

    PROVIDERS = ("openai", "gemini", "ollama")

    def configured(self, provider: str) -> bool:
        if provider == "openai":
            return bool(os.getenv("OPENAI_API_KEY"))
        if provider == "gemini":
            return bool(os.getenv("GEMINI_API_KEY"))
        if provider == "ollama":
            return os.getenv("OLLAMA_ENABLED", "false").lower() in {"1", "true", "yes"}
        return False

    def model(self, provider: str, ollama_model: str = "gemma") -> str:
        if provider == "ollama" and ollama_model not in {"gemma", "llama"}:
            raise ValueError(f"지원하지 않는 Ollama 모델 선택입니다: {ollama_model}")
        models = {
            "openai": os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            "gemini": os.getenv("GEMINI_MODEL", "gemini-3.5-flash"),
            "ollama": (
                os.getenv("GEMMA_MODEL", "gemma3:4b")
                if ollama_model == "gemma"
                else os.getenv("OLLAMA_MODEL", "llama3.2")
            ),
        }
        if provider not in models:
            raise ValueError(f"지원하지 않는 Provider입니다: {provider}")
        return models[provider]

    @staticmethod
    def _prompt(message: str, recent_messages: list[dict[str, str]]) -> str:
        history = "\n".join(
            f"{item['role']}: {item['content']}" for item in recent_messages[-6:]
        )
        return (
            "당신은 초보자용 여행 준비 도우미입니다. 실제 예약이나 결제를 수행하지 말고 "
            "짧고 안전한 여행 준비 조언만 제공하세요.\n"
            f"최근 대화:\n{history or '(첫 대화)'}\n사용자 질문: {message}"
        )

    def reply(
        self,
        provider: str,
        message: str,
        recent_messages: list[dict[str, str]],
        ollama_model: str = "gemma",
    ) -> LLMReply:
        if provider not in self.PROVIDERS:
            raise ValueError(f"지원하지 않는 Provider입니다: {provider}")
        if not self.configured(provider):
            raise RuntimeError(f"{provider} 설정을 확인하세요.")
        prompt = self._prompt(message, recent_messages)
        model = self.model(provider, ollama_model)
        if provider == "openai":
            from openai import OpenAI

            response = OpenAI().responses.create(model=model, input=prompt)
            text = response.output_text
        elif provider == "gemini":
            from google import genai

            gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
            response = gemini_client.models.generate_content(
                model=model, contents=prompt
            )
            text = response.text
        else:
            base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434").rstrip("/")
            response = httpx.post(
                f"{base_url}/api/chat",
                json={"model": model, "messages": [{"role": "user", "content": prompt}], "stream": False},
                timeout=90,
            )
            response.raise_for_status()
            text = response.json()["message"]["content"]
        if not text:
            raise RuntimeError(f"{provider}가 텍스트 응답을 반환하지 않았습니다.")
        return LLMReply(provider=provider, model=model, text=text)
