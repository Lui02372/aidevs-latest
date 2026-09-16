"""PostgreSQL 기반 사용자 범위 Memory 저장소입니다."""

from __future__ import annotations

import re
from typing import Any
from uuid import uuid4

ALLOWED_KEYS = {"transportation", "food_restriction", "hotel_preference"}
SENSITIVE_KEYS = {"password", "card_number", "passport_number", "api_key", "access_token"}
SENSITIVE_PATTERNS = (
    re.compile(r"(?i)(password|api[_ -]?key|access[_ -]?token|비밀번호)\s*[:=]?\s*\S+"),
    re.compile(r"(?<!\d)(?:\d[ -]?){15,16}(?!\d)"),
)


def validate_memory(key: str, value: str) -> None:
    if key in SENSITIVE_KEYS or key not in ALLOWED_KEYS:
        raise ValueError("저장이 허용되지 않은 Memory key입니다.")
    if any(pattern.search(value) for pattern in SENSITIVE_PATTERNS):
        raise ValueError("Memory 값에 민감정보가 포함되어 있습니다.")


def select_relevant(items: list[dict[str, Any]], question: str) -> list[dict[str, Any]]:
    keys: list[str] = []
    if any(word in question for word in ("이동", "교통", "경로")):
        keys.append("transportation")
    if any(word in question for word in ("음식", "식당", "먹")):
        keys.append("food_restriction")
    if any(word in question for word in ("호텔", "숙소")):
        keys.append("hotel_preference")
    return [item for item in items if item["key"] in keys]


class PostgresMemoryStore:
    """모든 SQL에 인증된 user_id 범위를 강제합니다."""

    def __init__(self, database_url: str, user_id: str) -> None:
        self.database_url = database_url
        self.user_id = user_id

    def _connect(self):
        import psycopg

        return psycopg.connect(self.database_url, connect_timeout=3)

    @staticmethod
    def _item(row: tuple[Any, ...]) -> dict[str, Any]:
        return {"id": str(row[0]), "key": row[1], "value": row[2]}

    def save(self, key: str, value: str) -> dict[str, Any]:
        validate_memory(key, value)
        with self._connect() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO user_memories (id, user_id, memory_key, memory_value)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_id, memory_key)
                DO UPDATE SET memory_value = EXCLUDED.memory_value, updated_at = NOW()
                RETURNING id, memory_key, memory_value
                """,
                (uuid4(), self.user_id, key, value),
            )
            return self._item(cursor.fetchone())

    def list(self) -> list[dict[str, Any]]:
        with self._connect() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, memory_key, memory_value
                FROM user_memories WHERE user_id = %s ORDER BY created_at
                """,
                (self.user_id,),
            )
            return [self._item(row) for row in cursor.fetchall()]

    def delete(self, memory_id: str) -> bool:
        with self._connect() as connection, connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM user_memories WHERE user_id = %s AND id = %s",
                (self.user_id, memory_id),
            )
            return cursor.rowcount == 1

    def relevant(self, question: str) -> list[dict[str, Any]]:
        return select_relevant(self.list(), question)
