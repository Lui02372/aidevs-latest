"""표준 응답 구조 예제입니다.

이 파일은 표준 응답 구조 개념을 나누어 읽고 실행해 보기 위한 학습용 파일입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\03_pydantic-and-response
    uvicorn 04_standard-response:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn 04_standard-response:app --reload

API가 많아질수록 응답 모양이 제각각이면 프론트엔드에서 처리하기 어렵습니다.
이 예제에서는 success, message, data 형태로 응답을 통일합니다.
"""

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel


# FastAPI 앱 객체입니다.
# uvicorn 실행 명령의 마지막 `:app`은 아래 변수 이름 `app`과 연결됩니다.
app = FastAPI(title="Standard Response Practice")


class ApiResponse(BaseModel):
    """수업용 표준 응답 모델입니다."""

    # success는 요청 처리 성공 여부를 나타냅니다.
    success: bool
    # message는 사용자가 보거나 프론트엔드가 표시할 수 있는 짧은 설명입니다.
    message: str
    # data는 실제 데이터입니다. 목록, 객체, None 등 여러 모양이 올 수 있어 Any를 사용합니다.
    data: Any | None = None


# response_model=ApiResponse를 사용하면 이 API는 항상 ApiResponse 모양으로 응답합니다.
@app.get("/memos", response_model=ApiResponse)
def list_memos():
    """메모 목록을 표준 응답 구조로 반환합니다."""

    # 예제를 단순하게 하기 위해 함수 안에서 임시 메모 목록을 만듭니다.
    memos = [
        {
            "id": 1,
            "title": "표준 응답 구조",
            "content": "success, message, data 구조를 연습합니다.",
            "tags": ["api", "response"],
        }
    ]

    # Pydantic 모델 객체를 직접 반환해도 FastAPI가 JSON으로 변환해 줍니다.
    return ApiResponse(
        success=True,
        message="memos loaded",
        data=memos,
    )


@app.get("/empty", response_model=ApiResponse)
def empty_response():
    """데이터가 없어도 응답 구조는 유지합니다."""

    # 데이터가 없을 때도 success, message, data 필드를 유지하면
    # 프론트엔드에서 응답을 처리하는 코드가 단순해집니다.
    return ApiResponse(
        success=True,
        message="no data yet",
        data=None,
    )
