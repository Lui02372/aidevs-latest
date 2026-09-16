"""FastAPI 404, 405, 422를 재현하는 예제입니다.

실행:
    python -m uvicorn broken_api:app --reload --host 127.0.0.1 --port 8092

이 파일의 코드는 문법적으로는 정상입니다.
다만 일부 요청을 잘못 보내면 FastAPI의 대표 오류를 확인할 수 있습니다.
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(title="Lab 02 Broken API")


class ChatRequest(BaseModel):
    """POST /ai/chat 요청 Body입니다."""

    message: str = Field(min_length=1, examples=["FastAPI 오류를 설명해줘"])


@app.get("/health")
def health() -> dict[str, str]:
    """서버가 켜져 있는지 확인합니다."""

    return {"status": "ok"}


@app.post("/ai/chat")
def chat(request: ChatRequest) -> dict[str, str]:
    """message 필드를 받아 간단한 답변을 반환합니다."""

    return {
        "message": request.message,
        "answer": f"'{request.message}'에 대한 lab용 응답입니다.",
    }
