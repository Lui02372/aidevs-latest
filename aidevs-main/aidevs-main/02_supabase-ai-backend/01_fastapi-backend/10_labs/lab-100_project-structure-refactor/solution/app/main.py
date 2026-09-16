r"""프로젝트 구조를 나눈 FastAPI 앱의 실행 시작점입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\10_labs\lab-100_project-structure-refactor\solution
    uvicorn app.main:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn app.main:app --reload

`app.main:app`은 "app 폴더 안의 main.py 파일에 있는 app 변수"라는 뜻입니다.
"""

from fastapi import FastAPI

from app.routers.memo_router import router as memo_router


# FastAPI 서버 객체를 만듭니다.
# 실제 API 경로는 app/routers/memo_router.py에 나누어 두고,
# 여기서는 라우터를 연결하는 역할만 담당합니다.
app = FastAPI(title="Mini Memo API - Structured")
app.include_router(memo_router)
