"""API 요청과 응답 데이터 형태를 정의하는 Pydantic 모델 파일입니다.

Pydantic 모델을 사용하면 FastAPI가 다음 일을 자동으로 도와줍니다.

1. 요청 Body의 필수값과 타입을 검사합니다.
2. Swagger UI에 요청/응답 예시 구조를 보여 줍니다.
3. 함수에서 사용하는 데이터 형태를 명확하게 문서화합니다.

초보자가 기억할 점:
    `ProductCreate`는 클라이언트가 서버로 보내는 요청 모델입니다.
    `ProductResponse`처럼 `Response`가 붙은 모델은 서버가 클라이언트로 돌려주는 응답 모델입니다.
"""

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    """상품 등록 요청 Body입니다.

    예시 JSON:
        {
            "name": "AI 노트",
            "description": "학습 내용을 정리하는 노트",
            "target_audience": "입문자"
        }
    """

    name: str = Field(min_length=1, description="상품 이름")
    description: str = Field(min_length=1, description="상품 기본 설명")
    target_audience: str = Field(default="초보자", min_length=1, description="주요 대상")


class ProductResponse(BaseModel):
    """상품 등록 또는 상품 목록 조회 시 반환되는 응답 모델입니다."""

    id: str
    name: str
    description: str
    target_audience: str
    ai_description: str | None = None
    created_at: str


class AiDescriptionResponse(BaseModel):
    """AI 상품 설명 생성 API의 응답 모델입니다."""

    product_id: str
    ai_description: str
    actual_api_called: bool
    provider: str
    model: str


class ServiceLogResponse(BaseModel):
    """서비스 로그 조회 API의 응답 모델입니다."""

    id: str
    action: str
    status: str
    detail: str | None = None
    created_at: str
