r"""상품 API 구조 분리 과제 solution 테스트입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\20_assignments\assignment-100_product-api-structure-refactor\solution
    python -m pytest -s
"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    print("1. GET /health 상태 확인 API를 호출합니다.")
    response = client.get("/health")

    print("   응답:", response.status_code, response.json())
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_products():
    print("2. GET /products 상품 목록 API를 호출합니다.")
    response = client.get("/products")

    print("   응답:", response.status_code, response.json())
    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 2
    assert body["data"][0]["id"] == 1


def test_search_products():
    print("3. GET /products/search 상품 검색 API를 호출합니다.")
    response = client.get("/products/search", params={"keyword": "AI"})

    print("   응답:", response.status_code, response.json())
    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 1
    assert "AI" in body["data"][0]["name"] or "AI" in body["data"][0]["description"]


def test_get_product():
    print("4. GET /products/1 상품 단건 조회 API를 호출합니다.")
    response = client.get("/products/1")

    print("   응답:", response.status_code, response.json())
    assert response.status_code == 200
    assert response.json()["name"] == "FastAPI 교재"


def test_get_missing_product_returns_404():
    print("5. GET /products/999 없는 상품 조회 API를 호출합니다.")
    response = client.get("/products/999")

    print("   응답:", response.status_code, response.json())
    assert response.status_code == 404


def test_create_product():
    print("6. POST /products 새 상품 생성 API를 호출합니다.")
    response = client.post(
        "/products",
        json={
            "name": "무선 마우스",
            "description": "USB-C 충전식 마우스",
            "price": 45000,
        },
    )

    print("   응답:", response.status_code, response.json())
    assert response.status_code == 201
    body = response.json()
    assert body["id"] >= 3
    assert body["name"] == "무선 마우스"
