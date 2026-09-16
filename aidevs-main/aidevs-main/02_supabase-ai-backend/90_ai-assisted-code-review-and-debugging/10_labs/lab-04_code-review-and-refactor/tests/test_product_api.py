"""messy_product_api의 기본 동작 테스트입니다.

실행:
    python -m pytest tests

이 테스트는 리팩토링 전후에 기능이 유지되는지 확인하는 기준선입니다.
"""

from fastapi.testclient import TestClient

from messy_product_api import app, products, questions


client = TestClient(app)


def setup_function() -> None:
    """각 테스트가 독립적으로 실행되도록 memory list를 비웁니다."""

    products.clear()
    questions.clear()


def test_create_and_list_product() -> None:
    """상품 생성 후 목록에서 확인합니다."""

    response = client.post("/products", json={"name": "AI 학습 노트", "price": 12000})
    assert response.status_code == 200
    product = response.json()
    assert product["name"] == "AI 학습 노트"

    list_response = client.get("/products")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_create_question_for_product() -> None:
    """상품에 질문을 추가하고 조회합니다."""

    product = client.post("/products", json={"name": "AI 학습 노트", "price": 12000}).json()
    response = client.post(
        f"/products/{product['id']}/questions",
        json={"message": "초보자에게 적합한가요?"},
    )
    assert response.status_code == 200
    assert response.json()["product_id"] == product["id"]

    list_response = client.get(f"/products/{product['id']}/questions")
    assert len(list_response.json()) == 1


def test_question_for_missing_product_returns_404() -> None:
    """없는 상품에 질문을 달면 404를 반환합니다."""

    response = client.post(
        "/products/missing/questions",
        json={"message": "초보자에게 적합한가요?"},
    )
    assert response.status_code == 404
