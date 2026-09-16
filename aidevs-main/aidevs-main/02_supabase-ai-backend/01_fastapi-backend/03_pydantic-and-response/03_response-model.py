"""Response Model 예제입니다.

이 파일은 Response Model 개념을 나누어 읽고 실행해 보기 위한 학습용 파일입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\03_pydantic-and-response
    uvicorn 03_response-model:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn 03_response-model:app --reload

response_model은 API 응답으로 내보낼 데이터의 모양을 제한합니다.
내부 데이터에 internal_note 같은 값이 있어도 응답 모델에 없으면 밖으로 나가지 않습니다.
"""

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# FastAPI 앱 객체입니다.
# uvicorn 실행 명령의 마지막 `:app`은 아래 변수 이름 `app`과 연결됩니다.
app = FastAPI(title="Response Model Practice")


class MemoPublic(BaseModel):
    """외부에 공개해도 되는 메모 응답 모델입니다."""

    # 응답에 포함해도 되는 필드만 여기에 적습니다.
    # 아래 memos 데이터에는 internal_note가 있지만 이 모델에는 없습니다.
    id: int
    title: str
    content: str
    tags: list[str]


memos: dict[int, dict[str, Any]] = {
    1: {
        "id": 1,
        "title": "응답 모델 연습",
        "content": "response_model이 어떤 필드를 내보내는지 확인합니다.",
        "tags": ["response"],
        # 이 값은 서버 내부에서만 쓰는 값입니다.
        # MemoPublic에 없기 때문에 응답에는 포함되지 않습니다.
        "internal_note": "응답으로 내보내면 안 되는 내부 메모입니다.",
    }
}


# response_model=MemoPublic은 "이 API 응답은 MemoPublic 모양으로 내보내라"는 뜻입니다.
# 반환 데이터에 MemoPublic에 없는 필드가 있으면 FastAPI가 응답에서 제외합니다.
@app.get("/memos/{memo_id}", response_model=MemoPublic)
def get_memo(memo_id: int):
    """메모 정보를 반환하지만 internal_note는 응답에서 제외됩니다."""

    # 요청한 id의 메모가 없으면 404 오류를 반환합니다.
    if memo_id not in memos:
        raise HTTPException(status_code=404, detail="Memo not found")

    # 실제 dict에는 internal_note가 들어 있지만, response_model 때문에 밖으로 나가지 않습니다.
    return memos[memo_id]
