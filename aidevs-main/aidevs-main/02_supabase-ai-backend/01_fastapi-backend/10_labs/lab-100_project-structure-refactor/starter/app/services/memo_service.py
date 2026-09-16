from typing import Any

from app.schemas.memo_schema import MemoCreate, MemoPublic


memos: dict[int, dict[str, Any]] = {
    1: {
        "id": 1,
        "title": "FastAPI 구조 분리",
        "content": "router, schema, service로 역할을 나눕니다.",
        "tags": ["fastapi", "structure"],
        "internal_note": "API 응답에 포함되면 안 되는 내부 값입니다.",
    }
}
next_memo_id = 2


def to_public_memo(memo: dict[str, Any]) -> MemoPublic:
    """내부 dict에서 공개 응답 모델로 변환합니다."""

    return MemoPublic(**memo)


def list_memos() -> list[MemoPublic]:
    """전체 메모 목록을 반환합니다."""

    return [to_public_memo(memo) for memo in memos.values()]


def search_memos(keyword: str, limit: int) -> list[MemoPublic]:
    """제목 또는 본문에 keyword가 포함된 메모를 검색합니다."""

    normalized_keyword = keyword.lower()
    result = [
        to_public_memo(memo)
        for memo in memos.values()
        if normalized_keyword in memo["title"].lower()
        or normalized_keyword in memo["content"].lower()
    ]
    return result[:limit]


def get_memo(memo_id: int) -> MemoPublic | None:
    """메모 1개를 조회합니다."""

    memo = memos.get(memo_id)
    if memo is None:
        return None
    return to_public_memo(memo)


def create_memo(memo: MemoCreate) -> MemoPublic:
    """TODO: 새 메모를 저장하고 공개 응답 모델로 반환합니다."""

    return MemoPublic(id=0, title=memo.title, content=memo.content, tags=memo.tags)
