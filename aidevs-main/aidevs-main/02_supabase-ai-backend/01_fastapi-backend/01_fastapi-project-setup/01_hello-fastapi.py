"""FastAPI 첫 번째 예제.

이 파일은 첫 FastAPI 코드 구조를 읽어보기 위한 학습용 파일입니다.
파일명에 번호와 하이픈(-)이 들어 있지만, 수업에서는 uvicorn 실행 형태를 일관되게 확인합니다.

이 파일을 실행할 때는 `uvicorn 01_hello-fastapi:app --reload` 명령을 사용합니다.
만약 실행 환경에서 해당 명령이 오류가 나면 `python -m uvicorn 01_hello-fastapi:app --reload`로 실행합니다.
기본 프로젝트 실행 흐름은 같은 폴더의 `main.py`로도 비교해 확인합니다.

실행 방법:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\01_fastapi-project-setup
    uvicorn 01_hello-fastapi:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn 01_hello-fastapi:app --reload

main.py 기준 실행:
    uvicorn main:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn main:app --reload

주의:
    파일명에 하이픈(-)이 들어 있으면 일부 환경에서 import가 불편할 수 있습니다.
    실제 프로젝트에서는 보통 `main.py` 같은 단순한 파일명을 사용합니다.
"""

from fastapi import FastAPI


# FastAPI 객체는 API 서버의 중심입니다.
# 이 객체에 GET, POST 같은 엔드포인트를 하나씩 등록합니다.
app = FastAPI(
    title="Hello FastAPI",
    description="FastAPI 서버가 어떻게 시작되는지 확인하는 첫 예제입니다.",
    version="1.0.0",
)


@app.get("/")
def read_root():
    """브라우저에서 http://127.0.0.1:8000/ 로 접속했을 때 실행됩니다."""

    # FastAPI는 Python dict를 자동으로 JSON 응답으로 변환합니다.
    return {
        "message": "Hello, FastAPI Im Hungry",
        "next": "Open /docs to see Swagger UI",
    }


@app.get("/health")
def health_check():
    """서버가 살아 있는지 확인하는 가장 기본적인 점검용 API입니다."""

    return {"status": "okbary"}

@app.get("/login")
def health_check():
    """서버가 살아 있는지 확인하는 가장 기본적인 점검용 API입니다."""

    return {"status": "login ok"}

@app.get("/logout")
def health_check():
    """서버가 살아 있는지 확인하는 가장 기본적인 점검용 API입니다."""

    return {"status": "logout ok"}