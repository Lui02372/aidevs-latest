# product_service.py
from app.schemes.product_scheme import ProductPublic

# 1. 입력
def product_create(product:ProductPublic) -> ProductPublic:
    print("Database 에 입력이 처리 됩니다....")
    return product

# 2. 전체조회
def product_get_all() -> list[ProductPublic]:
    result = [];
    result.append(ProductPublic(
        id = 100,
        name = "pants01",
        price = 20000
    ))
    result.append(ProductPublic(
        id = 101,
        name = "pants02",
        price = 30000
    ))
    result.append(ProductPublic(
        id = 102,
        name = "pants03",
        price = 40000
    ))
    return result

# 3. 한개조회
def product_get(product_id:int) -> ProductPublic:
    get_product = ProductPublic(
        id = product_id,
        name = "크록스",
        price = 30000
    )

    return get_product