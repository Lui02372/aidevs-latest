"""리뷰와 리팩토링 연습용 FastAPI 코드입니다.

실행:
    python -m uvicorn messy_product_api:app --reload --host 127.0.0.1 --port 8094

이 파일은 "동작은 하지만 구조가 아쉬운 코드"입니다.
수강생은 Codex에게 먼저 리뷰를 요청하고, 그 다음 리팩토링 계획을 받습니다.
"""

from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="Messy Product API")

# 전역 list는 작은 실습에서는 편하지만 실제 서비스 저장소로는 부족합니다.
products: list[dict] = []
questions: list[dict] = []


class ProductCreate(BaseModel):
    """상품 생성 요청 Body입니다."""

    name: str = Field(min_length=1, examples=["AI 학습 노트"])
    price: int = Field(ge=0, examples=[12000])


class QuestionCreate(BaseModel):
    """상품 질문 생성 요청 Body입니다."""

    message: str = Field(min_length=1, examples=["이 상품은 초보자에게 적합한가요?"])


@app.get("/health")
def health() -> dict[str, str]:
    """서버 실행 여부를 확인합니다."""

    return {"status": "ok"}


@app.post("/products")
def create_product(payload: ProductCreate) -> dict:
    """상품을 memory list에 저장합니다."""

    item = {"id": str(uuid4()), "name": payload.name, "price": payload.price}
    products.append(item)
    return item


@app.get("/products")
def list_products() -> list[dict]:
    """상품 목록을 반환합니다."""

    return products


@app.post("/products/{product_id}/questions")
def create_question(product_id: str, payload: QuestionCreate) -> dict:
    """상품에 질문을 추가합니다."""

    product = next((item for item in products if item["id"] == product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="product not found")

    item = {
        "id": str(uuid4()),
        "product_id": product_id,
        "message": payload.message,
        "answer": "mock 답변입니다. 실제 LLM 호출은 아직 하지 않습니다.",
    }
    questions.append(item)
    return item


@app.get("/products/{product_id}/questions")
def list_questions(product_id: str) -> list[dict]:
    """특정 상품의 질문 목록을 반환합니다."""

    return [item for item in questions if item["product_id"] == product_id]
