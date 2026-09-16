"""상품 API에서 사용하는 요청/응답 모델입니다."""

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    """POST /products 요청 Body 모델입니다."""

    name: str = Field(min_length=1, examples=["무선 키보드"])
    description: str = Field(min_length=1, examples=["개발자용 텐키리스 키보드"])
    price: int = Field(gt=0, examples=[89000])


class ProductPublic(BaseModel):
    """클라이언트에게 공개할 상품 응답 모델입니다."""

    id: int
    name: str
    description: str
    price: int
