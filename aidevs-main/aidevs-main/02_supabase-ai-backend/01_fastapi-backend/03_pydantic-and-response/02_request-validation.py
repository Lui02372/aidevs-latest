"""요청 데이터 검증 예제입니다.

이 파일은 요청 검증 개념을 나누어 읽고 실행해 보기 위한 학습용 파일입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\03_pydantic-and-response
    uvicorn 02_request-validation:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn 02_request-validation:app --reload

잘못된 요청이 들어오면 FastAPI는 자동으로 422 응답을 반환합니다.
이 예제에서는 필수값, 문자열 길이, 목록 길이를 검증합니다.
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field


# FastAPI 앱 객체입니다.
# uvicorn 실행 명령의 마지막 `:app`은 아래 변수 이름 `app`과 연결됩니다.
app = FastAPI(title="Request Validation Practice")


class MemoCreate(BaseModel):
    """메모 생성 요청 데이터입니다."""

    # min_length=1은 빈 문자열을 막기 위한 조건입니다.
    # max_length=50은 너무 긴 제목을 막습니다.
    title: str = Field(min_length=1, max_length=50, examples=["검증 연습"])

    # content도 최소 1글자 이상이어야 합니다.
    # 이 조건을 만족하지 않으면 create_memo 함수가 실행되기 전에 422가 반환됩니다.
    content: str = Field(min_length=1, max_length=500, examples=["잘못된 요청을 일부러 보내 봅니다."])

    # 태그는 5개까지만 받습니다.
    # default_factory=list는 tags를 생략했을 때 빈 목록을 새로 만들어 줍니다.
    tags: list[str] = Field(default_factory=list, max_length=5, examples=[["validation"]])


@app.post("/memos")
def create_memo(memo: MemoCreate):
    """요청 데이터가 조건을 만족하면 이 함수가 실행됩니다."""

    # 여기까지 왔다는 것은 요청 JSON이 MemoCreate 조건을 통과했다는 뜻입니다.
    # len(...) 값을 응답에 넣어 실제로 어떤 데이터가 들어왔는지 확인합니다.
    return {
        "message": "request validation passed",
        "title_length": len(memo.title),
        "content_length": len(memo.content),
        "tag_count": len(memo.tags),
    }
