from fastapi.testclient import TestClient

from app.main import app
from app.routers import product_router
from app.schemes.product_scheme import ProductPublic


client = TestClient(app)


def test_product_create_returns_created_product(monkeypatch):
    monkeypatch.setattr(product_router, "product_create", lambda product: product)
    payload = {"id": 1, "name": "T-shirt", "price": 15000}

    response = client.post("/product/create", json=payload)

    assert response.status_code == 200
    assert response.json() == payload


def test_product_get_returns_product_for_id(monkeypatch):
    monkeypatch.setattr(
        product_router,
        "product_get",
        lambda product_id: ProductPublic(id=product_id, name="T-shirt", price=15000),
    )

    response = client.get("/product/get/42")

    assert response.status_code == 200
    assert response.json() == {"id": 42, "name": "T-shirt", "price": 15000}


def test_product_get_all_returns_products(monkeypatch):
    products = [ProductPublic(id=1, name="T-shirt", price=15000)]
    monkeypatch.setattr(product_router, "product_get_all", lambda: products)

    response = client.get("/product/getall")

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "T-shirt", "price": 15000}]


def test_product_get_rejects_non_integer_id():
    response = client.get("/product/get/not-a-number")

    assert response.status_code == 422
