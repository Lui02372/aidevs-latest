"""Request Body 예제.

이 파일은 Request Body 개념을 나누어 읽고 실행해 보기 위한 학습용 파일입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\02_routing-and-request
    uvicorn 04_request-body:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn 04_request-body:app --reload

Request Body는 클라이언트가 서버로 보내는 JSON 데이터입니다.
보통 POST, PUT 요청에서 사용합니다.
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field


# FastAPI 앱 객체입니다.
# uvicorn 실행 명령의 마지막 `:app`은 아래 변수 이름 `app`과 연결됩니다.
app = FastAPI(title="Request Body Practice")


class FeedbackRequest(BaseModel):
    """사용자 피드백 요청 데이터입니다."""

    # Request Body로 받을 JSON의 모양을 Pydantic 모델로 정의합니다.
    # user_name은 최소 1글자 이상이어야 합니다.
    user_name: str = Field(min_length=1, examples=["Alice"])
    # score는 1 이상 5 이하 숫자만 허용합니다.
    # 범위를 벗어나면 FastAPI가 자동으로 422 오류를 반환합니다.
    score: int = Field(ge=1, le=5, examples=[5])
    # comment는 최소 5글자 이상이어야 합니다.
    comment: str = Field(min_length=5, examples=["오늘 수업이 이해하기 쉬웠습니다."])


# POST 요청은 보통 새 데이터를 만들거나 사용자가 입력한 JSON을 서버로 보낼 때 사용합니다.
# 함수 인자 feedback: FeedbackRequest 때문에 FastAPI는 요청 Body를 FeedbackRequest로 검증합니다.
@app.post("/feedback")
def create_feedback(feedback: FeedbackRequest):
    """사용자 피드백 JSON을 받아 처리합니다."""

    # feedback은 Pydantic 모델 객체입니다.
    # model_dump()를 사용하면 JSON으로 응답하기 쉬운 dict 형태로 바꿀 수 있습니다.
    return {
        "message": "feedback received",
        "data": feedback.model_dump(),
    }
