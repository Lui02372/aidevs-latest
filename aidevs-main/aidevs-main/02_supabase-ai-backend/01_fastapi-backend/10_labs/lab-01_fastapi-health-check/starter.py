"""Lab 01 starter: FastAPI 서버 시작하기.

TODO를 채워서 가장 작은 FastAPI 서버를 완성합니다.

??:
    uvicorn starter:app --reload

? ???? ??? ??:
    python -m uvicorn starter:app --reload
"""

from fastapi import FastAPI


# TODO: title 값을 "Memo API Lab 01"처럼 알아보기 쉬운 이름으로 바꿔 보세요.
app = FastAPI(title="TODO")


@app.get("/")
def read_root():
    """브라우저에서 서버 첫 화면을 확인하는 API입니다."""

    # TODO: 환영 메시지를 반환해 보세요.
    return {"message": "TODO"}


@app.get("/health")
def health_check():
    """서버 상태를 확인하는 API입니다."""

    # TODO: status 값이 ok가 되도록 수정해 보세요.
    return {"status": "TODO"}
