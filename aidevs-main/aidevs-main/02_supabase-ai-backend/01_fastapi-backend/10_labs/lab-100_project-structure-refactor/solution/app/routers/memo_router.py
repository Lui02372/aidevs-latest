from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.memo_schema import MemoCreate, MemoListResponse, MemoPublic
from app.services import memo_service


router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    """서버 상태 확인 endpoint입니다."""

    return {"status": "ok"}


@router.get("/memos", response_model=MemoListResponse)
def list_memos() -> MemoListResponse:
    """전체 메모를 조회합니다."""

    items = memo_service.list_memos()
    return MemoListResponse(count=len(items), data=items)


@router.get("/memos/search", response_model=MemoListResponse)
def search_memos(keyword: str = "", limit: int = Query(default=10, ge=1, le=20)) -> MemoListResponse:
    """키워드로 메모를 검색합니다."""

    items = memo_service.search_memos(keyword=keyword, limit=limit)
    return MemoListResponse(count=len(items), data=items)


@router.get("/memos/{memo_id}", response_model=MemoPublic)
def get_memo(memo_id: int) -> MemoPublic:
    """메모 1개를 조회합니다."""

    memo = memo_service.get_memo(memo_id)
    if memo is None:
        raise HTTPException(status_code=404, detail="Memo not found")
    return memo


@router.post("/memos", status_code=status.HTTP_201_CREATED, response_model=MemoPublic)
def create_memo(memo: MemoCreate) -> MemoPublic:
    """새 메모를 생성합니다."""

    return memo_service.create_memo(memo)
