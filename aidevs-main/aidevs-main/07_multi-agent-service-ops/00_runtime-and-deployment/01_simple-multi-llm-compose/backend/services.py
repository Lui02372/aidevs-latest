# [학습] 타입 힌트의 평가를 미뤄 타입 이름을 함수 정의 시점에 즉시 계산하지 않게 한다.
from __future__ import annotations

# [학습] json은 Redis에 저장할 문자열 변환, os는 프로세스 환경변수 읽기에 사용한다.
import json
import os
# [학습] dataclass는 데이터 객체의 생성자를 만들고 Any는 DB 값처럼 여러 타입이 올 수 있음을 표시한다.
from dataclasses import dataclass
from typing import Any

# [학습] httpx는 Ollama HTTP 요청, psycopg는 PostgreSQL, redis는 Redis 서버 통신을 담당한다.
import httpx
import psycopg
import redis
# [학습] dict_row는 SQL 조회 결과를 열 이름으로 접근할 수 있는 딕셔너리 행으로 받게 한다.
from psycopg.rows import dict_row


# [학습] frozen=True인 데이터 클래스는 생성 후 필드 재대입을 막는다. 공급자·모델·답변을 하나로 반환한다.
@dataclass(frozen=True)
class LLMReply:
    provider: str
    model: str
    text: str


# [학습] 객체는 Redis 클라이언트와 보존 시간 상태를 가진다. 영구 채팅 기록은 이 클래스의 책임이 아니다.
class RedisSessionStore:
    # [학습] url은 생략 가능하다. None이면 환경변수 또는 기본 주소를 쓰며 TTL 기본값 1800초는 30분이다.
    def __init__(self, url: str | None = None, ttl_seconds: int = 1800) -> None:
        # [학습] from_url로 접속 설정을 만들고 실제 명령 메서드에서 Redis와 통신한다.
        self.client = redis.from_url(
            url or os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0"),
            # [학습] decode_responses=True이면 Redis 바이트 응답을 Python 문자열로 받는다.
            decode_responses=True,
        )
        self.ttl_seconds = ttl_seconds

    # [학습] PING의 결과를 bool로 반환하여 /health의 상태 검사에 연결한다.
    def ping(self) -> bool:
        return bool(self.client.ping())

    # [학습] 요청 횟수는 세션별이 아닌 공용 키에 누적한다. incr와 set 두 명령을 하나의 트랜잭션으로 묶지는 않는다.
    def record_request(self, text: str) -> int:
        count = int(self.client.incr("runtime_demo:request_count"))
        # [학습] 최근 질문에만 TTL을 붙인다. 위 누적 횟수 키에는 이 코드에서 만료 시간을 설정하지 않는다.
        self.client.set("runtime_demo:recent_request", text, ex=self.ttl_seconds)
        return count

    # [학습] 키가 없으면 get은 None을 반환할 수 있다. 횟수는 or 0으로 초기값을 정한 뒤 정수로 바꾼다.
    def stats(self) -> dict[str, Any]:
        return {
            "request_count": int(self.client.get("runtime_demo:request_count") or 0),
            "recent_request": self.client.get("runtime_demo:recent_request"),
        }

    # [학습] 세션 ID를 키 이름에 넣어 대화를 구분하고 저장된 JSON 문자열 각각을 dict로 복원한다.
    def load_session(self, session_id: str) -> list[dict[str, str]]:
        key = f"runtime_demo:session:{session_id}"
        # [학습] lrange의 0, -1은 처음부터 끝까지이며 리스트 컴프리헨션은 각 메시지에 같은 변환을 적용한다.
        return [json.loads(item) for item in self.client.lrange(key, 0, -1)]

    # [학습] 입력은 role/content 딕셔너리들의 목록이며 반환값 없이 Redis에 반영한다.
    def append_session(self, session_id: str, messages: list[dict[str, str]]) -> None:
        key = f"runtime_demo:session:{session_id}"
        # [학습] 빈 목록일 때 RPUSH에 값 없이 요청하지 않도록 분기한다.
        if messages:
            # [학습] ensure_ascii=False는 한글을 그대로 JSON에 남긴다. *는 만든 목록을 RPUSH의 여러 인수로 펼친다.
            self.client.rpush(key, *[json.dumps(item, ensure_ascii=False) for item in messages])
        # [학습] 마지막 12개 메시지만 남기고 세션의 TTL을 갱신한다. 12개는 질문·답변 6쌍에 해당할 수 있다.
        self.client.ltrim(key, -12, -1)
        self.client.expire(key, self.ttl_seconds)

    # [학습] 현재 세션 키 하나만 삭제한다. 요청 통계와 PostgreSQL 기록은 여기서 다루지 않는다.
    def clear_session(self, session_id: str) -> None:
        self.client.delete(f"runtime_demo:session:{session_id}")


# [학습] Repository는 라우트 대신 SQL과 연결 수명을 관리한다. 생성자는 접속 문자열만 보관한다.
class PostgresRepository:
    def __init__(self, url: str | None = None) -> None:
        # [학습] 인수 → DATABASE_URL → 수업용 기본 주소 순서로 선택한다. 실제 환경값은 문서나 로그에 복사하지 않는다.
        self.url = url or os.getenv(
            "DATABASE_URL",
            "postgresql://agent_user:agent_pwd@127.0.0.1:5433/agent_db",
        )

    # [학습] SELECT 1은 데이터 변경 없이 연결을 검사한다. fetchone 결과는 기본 설정에서 한 원소 튜플이다.
    def ping(self) -> bool:
        # [학습] with가 연결과 커서를 정리한다. 연결 블록은 정상 종료 시 커밋, 예외 시 롤백 후 연결을 닫는다.
        with psycopg.connect(self.url) as connection, connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            return cursor.fetchone() == (1,)

    def schema_ready(self) -> bool:
        """이 Application이 사용하는 Schema와 두 Table이 모두 있는지 확인합니다."""
        # [학습] to_regclass로 두 테이블 이름이 존재하는지 검사한다. 열 타입·인덱스까지 검사하는 코드는 아니다.
        with psycopg.connect(self.url) as connection, connection.cursor() as cursor:
            cursor.execute(
                """SELECT
                       to_regclass('simple_multi_llm.notes') IS NOT NULL
                       AND to_regclass('simple_multi_llm.chat_messages') IS NOT NULL"""
            )
            return cursor.fetchone() == (True,)

    # [학습] 검증된 이름·메모를 받아 생성된 행을 반환한다. INSERT와 RETURNING을 한 SQL로 수행한다.
    def add_note(self, name: str, message: str) -> dict[str, Any]:
        with psycopg.connect(self.url, row_factory=dict_row) as connection, connection.cursor() as cursor:
            # [학습] SQL의 %s와 값 튜플을 분리하여 드라이버가 매개변수를 처리하게 한다. 문자열 조립으로 값을 끼우지 않는다.
            cursor.execute(
                "INSERT INTO simple_multi_llm.notes (name, message) VALUES (%s, %s) RETURNING id, name, message, created_at",
                (name, message),
            )
            # [학습] 행 하나를 일반 dict로 돌려주면 FastAPI가 날짜 등의 값을 JSON 표현으로 직렬화한다.
            return dict(cursor.fetchone())

    # [학습] 기본 limit=50이며 id 내림차순으로 최신 메모를 조회한다.
    def list_notes(self, limit: int = 50) -> list[dict[str, Any]]:
        with psycopg.connect(self.url, row_factory=dict_row) as connection, connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, message, created_at FROM simple_multi_llm.notes ORDER BY id DESC LIMIT %s",
                # [학습] (limit,)의 쉼표는 한 원소 튜플을 뜻한다. 괄호만 쓰면 정수 그대로라 매개변수 묶음이 아니다.
                (limit,),
            )
            # [학습] fetchall의 각 행을 dict로 바꾸어 목록으로 반환한다. 결과가 없으면 빈 목록이다.
            return [dict(row) for row in cursor.fetchall()]

    # [학습] 질문 또는 답변 한 개를 독립 연결에서 저장한다. 두 번의 호출은 서로 다른 트랜잭션이다.
    def add_chat_message(self, session_id: str, role: str, content: str) -> dict[str, Any]:
        with psycopg.connect(self.url, row_factory=dict_row) as connection, connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO simple_multi_llm.chat_messages (session_id, role, content) VALUES (%s, %s, %s) RETURNING id, session_id, role, content, created_at",
                (session_id, role, content),
            )
            return dict(cursor.fetchone())

    # [학습] 세션별 기록을 id 오름차순으로 최대 100개 반환한다. 대화가 길어지면 가장 오래된 100개가 선택된다.
    def list_chat(self, session_id: str, limit: int = 100) -> list[dict[str, Any]]:
        with psycopg.connect(self.url, row_factory=dict_row) as connection, connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, session_id, role, content, created_at FROM simple_multi_llm.chat_messages WHERE session_id = %s ORDER BY id ASC LIMIT %s",
                (session_id, limit),
            )
            return [dict(row) for row in cursor.fetchall()]


# [학습] 여러 공급자를 지원하지만 요청마다 하나만 선택하는 서비스다. Multi-Agent 조율 객체는 없다.
class MultiLLMChatService:
    """실제 Provider를 명시적으로 선택합니다. 자동 Mock Fallback은 없습니다."""

    # [학습] 튜플 상수는 허용된 공급자 목록이며 상태 검사와 요청 처리 양쪽에서 재사용한다.
    PROVIDERS = ("openai", "gemini", "ollama")

    # [학습] 환경변수의 존재나 플래그만 확인한다. API 키 유효성·모델 설치·네트워크 연결을 검증하지 않는다.
    def configured(self, provider: str) -> bool:
        if provider == "openai":
            return bool(os.getenv("OPENAI_API_KEY"))
        if provider == "gemini":
            return bool(os.getenv("GEMINI_API_KEY"))
        if provider == "ollama":
            # [학습] 문자열을 소문자로 맞춰 1/true/yes 중 하나인지 검사한다. 환경변수는 문자열로 전달된다.
            return os.getenv("OLLAMA_ENABLED", "false").lower() in {"1", "true", "yes"}
        return False

    # [학습] 공급자와 Ollama 선택을 받아 실제 모델명을 고른다. 기본값은 코드 설정이며 현재 이용 가능성의 증거는 아니다.
    def model(self, provider: str, ollama_model: str = "gemma") -> str:
        # [학습] 서비스를 API 밖에서 직접 호출해도 잘못된 Ollama 선택을 거부하도록 다시 검사한다.
        if provider == "ollama" and ollama_model not in {"gemma", "llama"}:
            raise ValueError(f"지원하지 않는 Ollama 모델 선택입니다: {ollama_model}")
        models = {
            "openai": os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            "gemini": os.getenv("GEMINI_MODEL", "gemini-3.5-flash"),
            # [학습] 조건 표현식으로 gemma이면 GEMMA_MODEL, 아니면 OLLAMA_MODEL을 선택한다.
            "ollama": (
                os.getenv("GEMMA_MODEL", "gemma3:4b")
                if ollama_model == "gemma"
                else os.getenv("OLLAMA_MODEL", "llama3.2")
            ),
        }
        # [학습] 사전에 없는 공급자는 명확한 ValueError를 내고, 정상일 때 모델 문자열 하나를 반환한다.
        if provider not in models:
            raise ValueError(f"지원하지 않는 Provider입니다: {provider}")
        return models[provider]

    # [학습] staticmethod는 self 없이 부를 수 있는 도우미다. 전달받은 값만으로 프롬프트 문자열을 만든다.
    @staticmethod
    def _prompt(message: str, recent_messages: list[dict[str, str]]) -> str:
        # [학습] 제너레이터 표현식으로 마지막 6개 메시지를 한 줄씩 만들고 join으로 연결한다. Redis 보관 12개와 다르다.
        history = "\n".join(
            f"{item['role']}: {item['content']}" for item in recent_messages[-6:]
        )
        # [학습] 괄호 안의 인접 문자열은 하나로 이어진다. 안내문·최근 문맥·현재 질문을 단일 텍스트로 구성한다.
        return (
            "당신은 초보자용 여행 준비 도우미입니다. 실제 예약이나 결제를 수행하지 말고 "
            "짧고 안전한 여행 준비 조언만 제공하세요.\n"
            f"최근 대화:\n{history or '(첫 대화)'}\n사용자 질문: {message}"
        )

    # [학습] 입력은 공급자·질문·최근 대화·모델 선택이며 반환은 타입이 정해진 LLMReply 객체다.
    def reply(
        self,
        provider: str,
        message: str,
        recent_messages: list[dict[str, str]],
        ollama_model: str = "gemma",
    ) -> LLMReply:
        # [학습] 잘못된 공급자 또는 미설정 상태를 실제 외부 호출 전에 다시 막는다.
        if provider not in self.PROVIDERS:
            raise ValueError(f"지원하지 않는 Provider입니다: {provider}")
        if not self.configured(provider):
            raise RuntimeError(f"{provider} 설정을 확인하세요.")
        # [학습] 공통 프롬프트와 모델명을 먼저 만든 뒤 공급자에 맞는 분기 하나만 실행한다.
        prompt = self._prompt(message, recent_messages)
        model = self.model(provider, ollama_model)
        if provider == "openai":
            # [학습] 분기 안의 import는 해당 공급자를 선택할 때 SDK를 불러오는 지연 import다.
            from openai import OpenAI

            # [학습] OpenAI SDK의 Responses API를 동기 호출하고 응답 객체의 output_text를 읽는다.
            response = OpenAI().responses.create(model=model, input=prompt)
            text = response.output_text
        elif provider == "gemini":
            from google import genai

            # [학습] 지역 변수로 Gemini 클라이언트를 유지한 상태에서 generate_content를 호출한다. 명시적 close는 없다.
            gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
            response = gemini_client.models.generate_content(
                model=model, contents=prompt
            )
            text = response.text
        else:
            # [학습] Ollama 기본 주소 끝의 /를 제거해 아래 경로를 붙일 때 //가 생기지 않게 한다.
            base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434").rstrip("/")
            # [학습] Ollama는 SDK 대신 HTTP POST를 쓴다. 90초 timeout과 stream=False로 한 번에 JSON 답변을 받는다.
            response = httpx.post(
                f"{base_url}/api/chat",
                json={"model": model, "messages": [{"role": "user", "content": prompt}], "stream": False},
                timeout=90,
            )
            # [학습] 실패 HTTP 상태이면 여기서 예외가 나서 JSON 내용 읽기로 진행하지 않는다.
            response.raise_for_status()
            text = response.json()["message"]["content"]
        # [학습] 공급자 응답에 텍스트가 없으면 성공 객체를 만들지 않고 예외로 상위 라우트에 전달한다.
        if not text:
            raise RuntimeError(f"{provider}가 텍스트 응답을 반환하지 않았습니다.")
        # [학습] 공급자별 응답 형식을 공통 객체로 통일해 app.py가 동일한 필드로 처리하게 한다.
        return LLMReply(provider=provider, model=model, text=text)
