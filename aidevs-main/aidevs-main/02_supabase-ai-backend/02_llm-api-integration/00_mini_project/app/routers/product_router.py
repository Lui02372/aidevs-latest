# product_router.py

from fastapi import APIRouter
from app.schemes.product_scheme import ProductPublic
from app.services.product_service import product_get_all,product_get,product_create

product_router = APIRouter()

@product_router.post("/product/create")
def create(product:ProductPublic) -> ProductPublic:
    return product_create(product)

@product_router.get("/product/get/{product_id}")
def get(product_id:int) -> ProductPublic:
    return product_get(product_id)

@product_router.get("/product/getall")
def get_all() -> list[ProductPublic]:
    return product_get_all()