"""테스트 클라이언트에서 사용할 작은 FastAPI 앱입니다.

직접 서버 실행:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\05_error-handling-and-testing
    uvicorn app_for_test:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn app_for_test:app --reload

테스트 스크립트 실행:
    python 05_simple-test-client.py

이 파일은 05_simple-test-client.py에서 import해서 사용합니다.
TestClient를 사용할 때는 uvicorn 서버를 직접 띄우지 않아도 API를 호출해 볼 수 있습니다.
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field


# FastAPI 앱 객체입니다.
# `uvicorn app_for_test:app --reload`에서 마지막 `app`이 이 변수입니다.
app = FastAPI(title="App For Test")


class MessageRequest(BaseModel):
    """POST /messages 요청 Body의 모양입니다."""

    # text는 최소 1글자 이상이어야 합니다.
    # 비어 있으면 FastAPI가 자동으로 422 오류를 반환합니다.
    text: str = Field(min_length=1, examples=["hello"])


# 테스트에서 가장 먼저 확인하기 좋은 상태 확인 API입니다.
@app.get("/health")
def health_check():
    return {"status": "ok"}


# TestClient가 POST 요청과 Request Body 처리를 확인할 때 사용하는 API입니다.
@app.post("/messages")
def create_message(request: MessageRequest):
    # request는 MessageRequest 모델로 검증된 값입니다.
    # len(request.text)로 입력 문자열 길이를 함께 반환합니다.
    return {
        "message": "created",
        "data": {
            "text": request.text,
            "length": len(request.text),
        },
    }
