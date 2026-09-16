"""상품 데이터 처리 로직을 모아 둔 solution 파일입니다."""

from app.schemas.product_schema import ProductCreate, ProductPublic


products: dict[int, dict[str, int | str]] = {
    1: {
        "id": 1,
        "name": "FastAPI 교재",
        "description": "API 서버 개발 입문 교재",
        "price": 18000,
    },
    2: {
        "id": 2,
        "name": "AI 실습 노트",
        "description": "LLM API와 백엔드 연결 실습용 노트",
        "price": 12000,
    },
}

next_product_id = 3


def list_products() -> list[ProductPublic]:
    """전체 상품 목록을 ProductPublic 목록으로 반환합니다."""

    return [ProductPublic(**product) for product in products.values()]


def search_products(keyword: str) -> list[ProductPublic]:
    """상품명 또는 설명에서 keyword를 검색합니다."""

    normalized = keyword.strip().lower()
    if not normalized:
        return list_products()

    matched = []
    for product in products.values():
        name = str(product["name"]).lower()
        description = str(product["description"]).lower()
        if normalized in name or normalized in description:
            matched.append(ProductPublic(**product))

    return matched


def get_product(product_id: int) -> ProductPublic | None:
    """상품 id로 상품 1개를 조회합니다."""

    product = products.get(product_id)
    if product is None:
        return None

    return ProductPublic(**product)


def create_product(product: ProductCreate) -> ProductPublic:
    """새 상품을 생성하고 ProductPublic으로 반환합니다."""

    global next_product_id

    created = {
        "id": next_product_id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
    }
    products[next_product_id] = created
    next_product_id += 1

    return ProductPublic(**created)
