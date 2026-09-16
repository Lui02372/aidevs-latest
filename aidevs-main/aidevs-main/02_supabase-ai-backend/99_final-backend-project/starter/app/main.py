r"""최종 백엔드 프로젝트를 시작할 때 사용하는 가장 작은 FastAPI 파일입니다.

실행 위치:
    C:\aidev\02_supabase-ai-backend\99_final-backend-project\starter

실행 명령:
    uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

확인 주소:
    http://127.0.0.1:8000/health
    http://127.0.0.1:8000/docs

이 파일의 목적:
    1. 최종 프로젝트를 복잡한 구조로 바로 시작하지 않고, 서버 실행부터 확인합니다.
    2. `/health` API 하나만 먼저 만들고 Swagger UI에서 호출해 봅니다.
    3. 이후 상품 API, AI 설명 생성 API, Supabase 저장 기능을 하나씩 추가합니다.
"""

from fastapi import FastAPI

# FastAPI 객체는 백엔드 서버의 시작점입니다.
# title 값은 Swagger UI 상단에 표시되므로 프로젝트 이름을 구분하는 데 도움이 됩니다.
app = FastAPI(title="Final Backend Project Starter")


@app.get("/health")
def health() -> dict[str, str]:
    """프로젝트 서버가 정상 실행 중인지 확인하는 가장 작은 API입니다.

    처음 백엔드를 만들 때는 DB나 AI API를 붙이기 전에 `/health`부터 확인하는 것이 좋습니다.
    이 API가 성공하면 Python, FastAPI, uvicorn 실행 환경은 정상이라고 볼 수 있습니다.
    """

    return {
        "status": "ok",
        "message": "final project starter is running",
    }
