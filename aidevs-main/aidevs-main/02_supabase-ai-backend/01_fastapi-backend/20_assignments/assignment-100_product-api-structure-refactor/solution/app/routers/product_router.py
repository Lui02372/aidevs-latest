"""상품 API 경로를 정의하는 solution 파일입니다."""

from fastapi import APIRouter, HTTPException, status

from app.schemas.product_schema import ProductCreate, ProductPublic
from app.services import product_service


router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    """서버 상태 확인 응답을 반환합니다."""

    return {"status": "ok"}


@router.get("/products")
def list_products() -> dict[str, list[ProductPublic] | int]:
    """전체 상품 목록을 반환합니다."""

    products = product_service.list_products()
    return {"count": len(products), "data": products}


@router.get("/products/search")
def search_products(keyword: str) -> dict[str, list[ProductPublic] | int]:
    """상품명 또는 설명에서 keyword를 검색합니다."""

    products = product_service.search_products(keyword)
    return {"count": len(products), "data": products}


@router.get("/products/{product_id}", response_model=ProductPublic)
def get_product(product_id: int) -> ProductPublic:
    """상품 1개를 조회하고, 없으면 404를 반환합니다."""

    product = product_service.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.post("/products", response_model=ProductPublic, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate) -> ProductPublic:
    """새 상품을 생성합니다."""

    return product_service.create_product(product)
