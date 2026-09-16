"""Lab 01 solution: FastAPI 서버 시작하기.

??:
    uvicorn solution:app --reload

? ???? ??? ??:
    python -m uvicorn solution:app --reload
"""

from fastapi import FastAPI


app = FastAPI(title="Memo API Lab 01")


@app.get("/")
def read_root():
    """서버 첫 화면에서 확인할 환영 메시지를 반환합니다."""

    return {
        "message": "Welcome to Memo API Lab",
        "next": "Open /docs to test the API",
    }


@app.get("/health")
def health_check():
    """서버가 정상 실행 중인지 확인합니다."""

    return {"status": "ok"}
