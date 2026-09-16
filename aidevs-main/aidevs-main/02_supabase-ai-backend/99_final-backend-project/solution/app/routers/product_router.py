"""상품 API endpoint를 모아 둔 라우터 파일입니다.

라우터(router)는 FastAPI에서 API 주소를 기능별로 나누어 관리할 때 사용합니다.
이 파일은 최종 백엔드 프로젝트의 핵심 API 흐름을 보여 줍니다.

포함된 API:
    GET  /health
    POST /products
    GET  /products
    POST /products/{product_id}/ai-description
    GET  /service-logs

초보자가 읽는 순서:
    1. `/health`로 서버 상태를 확인합니다.
    2. `/products`에 상품을 등록합니다.
    3. `/products`로 등록된 상품 목록을 조회합니다.
    4. `/products/{product_id}/ai-description`로 mock AI 설명을 생성합니다.
    5. `/service-logs`로 어떤 작업이 기록되었는지 확인합니다.
"""

from fastapi import APIRouter, HTTPException

from app.schemas.product_schema import (
    AiDescriptionResponse,
    ProductCreate,
    ProductResponse,
    ServiceLogResponse,
)
from app.services.ai_service import build_mock_ai_description
from app.services.storage_service import (
    create_product,
    find_product,
    get_storage_mode,
    list_products,
    list_service_logs,
    save_log,
    update_ai_description,
)


# APIRouter는 API 묶음입니다.
# main.py에서 app.include_router(router)를 호출하면 아래 endpoint들이 FastAPI 앱에 연결됩니다.
router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """서버와 저장소 상태를 확인합니다.

    storage 값이 `memory`이면 Supabase 연결 없이 메모리 리스트를 사용 중입니다.
    storage 값이 `supabase`이면 `.env`의 Supabase 설정을 읽어 실제 DB를 사용 중입니다.
    """

    return {
        "status": "ok",
        "storage": get_storage_mode(),
        "message": "final backend project solution is running",
    }


@router.post("/products", response_model=ProductResponse)
def create_product_endpoint(payload: ProductCreate) -> dict:
    """상품을 등록합니다.

    payload는 사용자가 보낸 JSON 요청 Body입니다.
    ProductCreate 모델이 name, description, target_audience 값을 검증합니다.
    """

    return create_product(payload)


@router.get("/products", response_model=list[ProductResponse])
def list_products_endpoint() -> list[dict]:
    """등록된 상품 목록을 조회합니다."""

    return list_products()


@router.post("/products/{product_id}/ai-description", response_model=AiDescriptionResponse)
def generate_ai_description_endpoint(product_id: str) -> dict:
    """상품 ID를 받아 AI 설명을 생성합니다.

    이 solution에서는 비용과 API Key 문제를 줄이기 위해 실제 Gemini 호출 대신 mock 함수를 사용합니다.
    실제 LLM 호출로 바꾸고 싶다면 `app/services/ai_service.py`의 함수를 교체하면 됩니다.
    """

    product = find_product(product_id)
    if product is None:
        # 없는 상품 ID로 요청하면 404 오류를 반환합니다.
        # 동시에 서비스 로그에도 실패 기록을 남겨 나중에 운영 관점에서 확인할 수 있게 합니다.
        save_log("generate_ai_description", "failed", f"상품 없음: {product_id}")
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    ai_description = build_mock_ai_description(product)
    update_ai_description(product_id, ai_description)
    save_log("generate_ai_description", "success", f"mock 설명 생성: {product_id}")

    return {
        "product_id": product_id,
        "ai_description": ai_description,
        "actual_api_called": False,
        "provider": "mock",
        "model": "mock-product-description-v1",
    }


@router.get("/service-logs", response_model=list[ServiceLogResponse])
def list_service_logs_endpoint() -> list[dict]:
    """서비스에서 발생한 주요 작업 로그를 조회합니다.

    최종 프로젝트에서는 기능 구현뿐 아니라, 어떤 요청이 실행되었는지 기록하는 흐름도 중요합니다.
    """

    return list_service_logs()
