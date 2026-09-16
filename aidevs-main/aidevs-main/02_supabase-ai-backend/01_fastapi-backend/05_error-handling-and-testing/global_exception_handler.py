"""전역 예외 처리(Exception Handler) 예제.

실행:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\05_error-handling-and-testing
    uvicorn global_exception_handler:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn global_exception_handler:app --reload

확인:
    http://127.0.0.1:8000/items/1
    http://127.0.0.1:8000/items/999

서비스를 만들다 보면 오류가 여러 곳에서 발생합니다.
각 API마다 오류 응답 형식이 다르면 프론트엔드가 처리하기 어렵습니다.

전역 예외 처리는 특정 오류가 발생했을 때 응답 모양을 하나로 맞추는 방법입니다.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse


# FastAPI 앱 객체입니다.
# `uvicorn global_exception_handler:app --reload`에서 마지막 `app`이 이 변수입니다.
app = FastAPI(title="Global Exception Handler Practice")


# ServiceError는 우리 서비스에서 의도적으로 발생시키는 오류입니다.
# 예: 상품 없음, 권한 없음, 포인트 부족 같은 비즈니스 규칙 위반
class ServiceError(Exception):
    """서비스 규칙 위반을 표현하기 위한 수업용 예외 클래스입니다.

    Python 기본 예외를 그대로 사용해도 되지만,
    이렇게 직접 예외 클래스를 만들면 "우리 서비스에서 의도한 오류"를
    더 명확하게 구분할 수 있습니다.
    """

    def __init__(self, error_code: str, message: str, status_code: int = 400):
        # error_code는 프론트엔드나 로그에서 오류 종류를 구분하기 위한 코드입니다.
        self.error_code = error_code
        # message는 사용자나 개발자가 읽을 수 있는 설명입니다.
        self.message = message
        # status_code는 HTTP 응답 상태 코드입니다.
        self.status_code = status_code


# @app.exception_handler(ServiceError)는 ServiceError가 발생했을 때 실행될 공통 처리기입니다.
# 각 API마다 같은 오류 응답을 직접 만들지 않아도 됩니다.
@app.exception_handler(ServiceError)
def handle_service_error(request, exc: ServiceError):
    """ServiceError가 발생하면 항상 같은 JSON 형식으로 응답합니다."""

    # JSONResponse를 직접 만들면 상태 코드와 응답 JSON 구조를 원하는 대로 정할 수 있습니다.
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.message,
            },
        },
)


# 예제를 위한 임시 데이터입니다.
# 실제 서비스에서는 Supabase 같은 데이터베이스에서 조회합니다.
items = {
    1: {"id": 1, "name": "Python note"},
    2: {"id": 2, "name": "FastAPI note"},
}


# /items/{item_id}에서 없는 id를 요청하면 ServiceError를 발생시킵니다.
# 발생한 ServiceError는 위의 handle_service_error가 받아서 표준 JSON 응답으로 바꿉니다.
@app.get("/items/{item_id}")
def get_item(item_id: int):
    """상품을 조회하고, 없으면 표준 오류 응답을 반환합니다."""

    if item_id not in items:
        raise ServiceError(
            error_code="ITEM_NOT_FOUND",
            message="요청한 상품을 찾을 수 없습니다.",
            status_code=404,
        )

    return {
        "success": True,
        "data": items[item_id],
    }
