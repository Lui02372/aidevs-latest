r"""99_final-backend-project solution의 FastAPI 진입점입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\99_final-backend-project\solution
    ..\..\.venv\Scripts\Activate.ps1
    uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

확인:
    http://127.0.0.1:8000/health
    http://127.0.0.1:8000/docs

이 파일의 역할:
    1. FastAPI 앱 객체를 만듭니다.
    2. routers 폴더에 분리해 둔 API 라우터를 앱에 연결합니다.
    3. 실제 API 로직은 이 파일에 길게 작성하지 않고, router/service/schema 파일로 나눕니다.

초보자가 기억할 점:
    `uvicorn app.main:app`에서 앞의 `app.main`은 이 파일의 위치를 뜻하고,
    뒤의 `app`은 아래에서 만든 FastAPI 변수 이름을 뜻합니다.
"""

from fastapi import FastAPI

from app.routers.product_router import router as product_router


# FastAPI 객체를 생성합니다.
# title은 Swagger UI 문서 제목으로 보입니다.
app = FastAPI(title="Final Backend Project Solution")

# product_router 안에 정의한 `/health`, `/products`, `/service-logs` API를 앱에 등록합니다.
# 라우터를 분리하면 main.py가 짧아지고, 기능별 파일 구조를 만들기 쉬워집니다.
app.include_router(product_router)
