"""FastAPI 첫 실행용 main.py 파일입니다.

FastAPI 서버를 실행할 때는 보통 `uvicorn main:app --reload` 명령을 사용합니다.
이 명령이 동작하려면 현재 폴더에 main.py 파일이 있고,
그 안에 app = FastAPI() 형태의 변수가 있어야 합니다.
"""

from fastapi import FastAPI


# FastAPI 객체는 API 서버의 중심입니다.
# app이라는 이름은 uvicorn main:app 명령에서 사용하는 app과 연결됩니다.
app = FastAPI(
    title="JMLEE FastAPI",
    description="FastAPI 서버가 어떻게 시작되는지 확인하는 첫 예제입니다.",
    version="1.0.0",
)


@app.get("/")
def read_root() -> dict[str, str]:
    """브라우저에서 http://127.0.0.1:8000/ 로 접속했을 때 실행됩니다."""

    # FastAPI는 Python dict를 자동으로 JSON 응답으로 변환합니다.
    return {
        "message": "Hello, FastAPI",
        "next": "Open /docs to see Swagger UI",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    """서버가 살아 있는지 확인하는 가장 기본적인 점검용 API입니다."""

    return {"status": "ok"}

    
@app.get("/search")
def health_check() -> dict[str, str]:
    """서버가 살아 있는지 확인하는 가장 기본적인 점검용 API입니다."""
    return {"status": "search ok"}