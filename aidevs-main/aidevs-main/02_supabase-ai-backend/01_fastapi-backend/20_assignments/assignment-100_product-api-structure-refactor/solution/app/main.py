r"""상품 API 구조 분리 과제의 solution 실행 시작점입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\20_assignments\assignment-100_product-api-structure-refactor\solution
    uvicorn app.main:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn app.main:app --reload
"""

from fastapi import FastAPI

from app.routers.product_router import router as product_router


app = FastAPI(title="Product API Structure Assignment Solution")
app.include_router(product_router)
