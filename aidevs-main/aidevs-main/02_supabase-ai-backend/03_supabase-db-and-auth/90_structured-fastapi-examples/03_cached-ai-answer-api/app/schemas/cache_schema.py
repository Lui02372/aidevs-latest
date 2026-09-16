"""Redis 캐시 응답 모델입니다."""

from pydantic import BaseModel


class CachedAnswerResponse(BaseModel):
    """캐시 조회 결과를 화면/API에 반환할 때 사용하는 모델입니다."""

    question: str
    answer: str
    # cached=True이면 Redis에서 기존 답변을 읽은 것이고,
    # cached=False이면 이번 요청에서 새 답변을 만든 것입니다.
    cached: bool
    ttl_seconds: int
