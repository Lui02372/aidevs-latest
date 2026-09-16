"""상품 API 경로를 정의하는 파일입니다.

TODO를 채워서 테스트가 통과하도록 완성합니다.
"""

from fastapi import APIRouter, HTTPException, status

from app.schemas.product_schema import ProductCreate, ProductPublic
from app.services import product_service


router = APIRouter()


@router.get("/health")
def health_check():
    """TODO: 서버 상태 확인 응답을 완성하세요."""

    return {"status": "TODO"}


@router.get("/products")
def list_products():
    """TODO: 전체 상품 목록을 반환하세요."""

    products = []
    return {"count": len(products), "data": products}


@router.get("/products/search")
def search_products(keyword: str):
    """TODO: 상품명 또는 설명에서 keyword를 검색하세요."""

    products = product_service.search_products(keyword)
    return {"count": len(products), "data": products}


@router.get("/products/{product_id}", response_model=ProductPublic)
def get_product(product_id: int):
    """TODO: 상품 1개를 조회하고, 없으면 404를 반환하세요."""

    product = product_service.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.post("/products", response_model=ProductPublic, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    """TODO: 새 상품을 생성하세요."""

    return product_service.create_product(product)
