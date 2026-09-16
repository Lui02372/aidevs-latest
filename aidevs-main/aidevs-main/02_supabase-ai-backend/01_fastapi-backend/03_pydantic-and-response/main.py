"""Pydantic 요청 검증과 응답 모델을 한 번에 연습하는 FastAPI 예제입니다.

이 단원은 02_routing-and-request에서 만든 메모 API 흐름을 이어갑니다.
앞 단원에서는 URL, HTTP Method, Path Parameter, Query Parameter를 배웠고,
이번 단원에서는 "요청 데이터의 모양"과 "응답 데이터의 모양"을 명확히 정합니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\03_pydantic-and-response
    uvicorn main:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn main:app --reload

브라우저:
    http://127.0.0.1:8000/docs
"""

# Any는 "어떤 타입의 데이터든 올 수 있다"는 뜻입니다.
# 표준 응답의 data에는 메모 1개, 메모 목록, None 등 여러 형태가 들어갈 수 있어 사용합니다.
from typing import Any

# FastAPI:
#   API 서버 객체를 만들 때 사용합니다.
# HTTPException:
#   데이터가 없거나 잘못된 요청일 때 직접 HTTP 오류를 반환할 때 사용합니다.
# status:
#   201, 404 같은 상태 코드를 숫자 대신 의미 있는 이름으로 쓰기 위해 사용합니다.
from fastapi import FastAPI, HTTPException, status

# BaseModel:
#   요청/응답 데이터의 모양을 class로 정의할 때 사용합니다.
# Field:
#   문자열 길이, 예시, 설명 같은 세부 검증 조건을 붙일 때 사용합니다.
from pydantic import BaseModel, Field


# 이 파일은 01~04 개념 파일에서 배운 Pydantic 요청 검증,
# response_model, 표준 응답 구조를 하나의 메모 API로 합친 통합 예제입니다.
# uvicorn 명령의 `main:app`은 "main.py 파일 안의 app 변수"라는 뜻입니다.
app = FastAPI(
    # title, description, version은 Swagger UI 문서에 표시됩니다.
    # 기능 동작에는 직접 영향을 주지 않지만, API 문서를 이해하기 쉽게 만듭니다.
    title="Memo API - Pydantic And Response Practice",
    description="메모 API를 사용해 요청 검증, 응답 모델, 표준 응답 구조를 연습합니다.",
    version="1.0.0",
)


class MemoCreate(BaseModel):
    """클라이언트가 새 메모를 만들 때 보내야 하는 요청 데이터입니다.

    BaseModel을 상속하면 FastAPI가 이 클래스의 타입 힌트와 Field 조건을 읽어서
    요청 JSON을 자동으로 검사합니다. 조건을 만족하지 못하면 엔드포인트 함수가
    실행되기 전에 FastAPI가 422 오류를 반환합니다.
    """

    # title 필드는 문자열(str)이어야 합니다.
    # min_length=1이므로 빈 문자열 ""은 허용하지 않습니다.
    # max_length=50이므로 너무 긴 제목도 막습니다.
    # examples와 description은 Swagger UI에서 예시와 설명으로 보입니다.
    title: str = Field(
        min_length=1,
        max_length=50,
        examples=["FastAPI 복습"],
        description="메모 제목입니다. 비어 있을 수 없고 50자 이하여야 합니다.",
    )
    # content도 문자열이며, 본문이 비어 있지 않도록 검증합니다.
    # 수강생은 Swagger UI에서 일부러 빈 문자열을 보내 422 오류를 확인해 볼 수 있습니다.
    content: str = Field(
        min_length=1,
        max_length=500,
        examples=["오늘 배운 Path Parameter와 Query Parameter를 정리합니다."],
        description="메모 본문입니다. 비어 있을 수 없고 500자 이하여야 합니다.",
    )
    # tags는 문자열 목록(list[str])입니다.
    # default_factory=list는 요청 JSON에서 tags를 생략했을 때 빈 목록 []을 넣어 줍니다.
    # max_length=5는 태그를 최대 5개까지만 받겠다는 뜻입니다.
    tags: list[str] = Field(
        default_factory=list,
        max_length=5,
        examples=[["fastapi", "backend"]],
        description="메모를 분류하기 위한 태그 목록입니다. 최대 5개까지 허용합니다.",
    )


class MemoPublic(BaseModel):
    """API 응답으로 외부에 공개해도 되는 메모 데이터입니다.

    실제 서버 내부 데이터에는 관리용 값이나 민감한 값이 함께 들어갈 수 있습니다.
    response_model에 이 모델을 지정하면 여기에 정의된 필드만 응답으로 나갑니다.
    """

    # MemoPublic은 "밖으로 보여 줄 메모 모양"입니다.
    # 서버 내부 값인 internal_note는 여기에 적지 않습니다.
    id: int
    title: str
    content: str
    tags: list[str]


class ApiResponse(BaseModel):
    """프론트엔드가 공통으로 처리하기 쉬운 표준 응답 구조입니다."""

    # success, message, data를 모든 응답에서 반복하면 프론트엔드 처리가 쉬워집니다.
    # success=True이면 정상 처리, False이면 실패 처리처럼 사용할 수 있습니다.
    success: bool
    # message는 화면에 보여 줄 짧은 안내 문구나 개발자가 확인할 메시지입니다.
    message: str
    # data는 실제 응답 데이터입니다.
    # Any | None은 "어떤 데이터든 가능하고, 데이터가 없으면 None도 가능하다"는 뜻입니다.
    data: Any | None = None


# 아직 데이터베이스를 배우기 전이므로 메모 데이터를 메모리 변수에 저장합니다.
# 서버를 재시작하면 이 데이터는 초기값으로 돌아갑니다.
# dict[int, dict[str, Any]]는 "정수 id를 key로 사용하고, 값은 메모 dict"라는 뜻입니다.
memos: dict[int, dict[str, Any]] = {
    1: {
        "id": 1,
        "title": "FastAPI 시작",
        "content": "GET, POST, PUT, DELETE의 차이를 정리합니다.",
        "tags": ["fastapi", "api"],
        # internal_note는 서버 내부 관리용 값입니다.
        # MemoPublic 응답 모델에 없기 때문에 GET /memos/1 응답에는 포함되지 않습니다.
        "internal_note": "수업 확인 메모: 02 단원과 연결해서 설명합니다.",
    }
}
# 새 메모를 만들 때 사용할 다음 id 값입니다.
# 현재 1번 메모가 있으므로 다음 생성 id는 2부터 시작합니다.
next_memo_id = 2


# /health는 가장 단순한 실행 확인용 API입니다.
# 서버를 켠 뒤 브라우저나 PowerShell에서 먼저 확인하기 좋습니다.
@app.get("/health")
def health_check() -> dict[str, str]:
    """서버가 정상적으로 실행 중인지 확인하는 가장 단순한 엔드포인트입니다."""

    # 반환한 dict는 FastAPI가 자동으로 JSON 응답으로 바꿔 줍니다.
    return {"status": "ok"}


# @app.post("/memos")는 POST /memos 주소를 만듭니다.
# response_model=ApiResponse는 응답을 ApiResponse 구조로 맞추겠다는 뜻입니다.
# status_code=201은 "새 데이터 생성 성공"을 의미합니다.
@app.post("/memos", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
def create_memo(memo: MemoCreate) -> ApiResponse:
    """새 메모를 생성합니다.

    memo 매개변수의 타입이 MemoCreate이므로 FastAPI는 요청 Body를 자동 검증합니다.
    예를 들어 title이 비어 있거나 tags가 5개를 넘으면 이 함수는 실행되지 않고
    FastAPI가 422 Validation Error를 먼저 반환합니다.
    """

    # next_memo_id는 함수 밖에서 만든 변수입니다.
    # 함수 안에서 값을 증가시키려면 global로 "바깥 변수를 수정하겠다"고 알려야 합니다.
    global next_memo_id

    # 요청 Body가 MemoCreate 조건을 통과하면 여기에서 새 메모 dict를 만듭니다.
    # internal_note는 서버 내부 관리용 값이라 응답으로 그대로 내보내지 않습니다.
    new_memo = {
        "id": next_memo_id,
        "title": memo.title,
        "content": memo.content,
        "tags": memo.tags,
        "internal_note": "새로 생성된 메모의 서버 내부 관리 값입니다.",
    }

    # 메모리 저장소에 새 메모를 저장합니다.
    # key는 메모 id이고, value는 메모 전체 dict입니다.
    memos[next_memo_id] = new_memo
    # 다음 POST 요청에서 같은 id를 쓰지 않도록 1 증가시킵니다.
    next_memo_id += 1

    # ApiResponse.data는 Any 타입이므로 내부 값을 그대로 넣을 수도 있습니다.
    # 다만 응답에 내보낼 값만 담기 위해 MemoPublic으로 한 번 정리합니다.
    # **new_memo는 dict의 key/value를 MemoPublic 생성자 인자로 풀어서 넣는 문법입니다.
    # internal_note는 MemoPublic에 없는 필드이므로 응답용 데이터에서 제외됩니다.
    public_memo = MemoPublic(**new_memo).model_dump()

    # Pydantic 모델 객체를 반환하면 FastAPI가 JSON으로 변환합니다.
    return ApiResponse(
        success=True,
        message="memo created",
        data=public_memo,
    )


@app.get("/memos/{memo_id}", response_model=MemoPublic)
def get_memo(memo_id: int) -> dict[str, Any]:
    """메모 1개를 조회합니다.

    내부 데이터에는 internal_note가 있지만 response_model=MemoPublic을 사용했기 때문에
    실제 응답에는 id, title, content, tags만 포함됩니다.
    """

    # memo_id는 URL 경로에서 들어오는 Path Parameter입니다.
    # 함수 인자 타입이 int이므로 FastAPI가 숫자로 변환합니다.
    if memo_id not in memos:
        # 요청 형식은 맞지만 해당 id의 데이터가 없으면 404 Not Found를 반환합니다.
        raise HTTPException(status_code=404, detail="Memo not found")

    # 내부 dict를 그대로 반환해도 response_model=MemoPublic이 응답 필드를 걸러 줍니다.
    return memos[memo_id]


# @app.get("/memos")는 전체 메모 목록 조회 API입니다.
# 응답은 항상 ApiResponse 구조로 감싸서 반환합니다.
@app.get("/memos", response_model=ApiResponse)
def list_memos() -> ApiResponse:
    """메모 목록을 표준 응답 구조로 반환합니다.

    프론트엔드에서는 success로 성공 여부를 확인하고, message를 화면 메시지로 쓰고,
    data에 들어 있는 실제 목록을 화면에 표시할 수 있습니다.
    """

    # 각 메모를 MemoPublic으로 변환해 internal_note 같은 내부 필드를 제거합니다.
    # 리스트 컴프리헨션은 여러 메모를 하나씩 변환해 새 목록을 만드는 Python 문법입니다.
    public_memos = [MemoPublic(**memo).model_dump() for memo in memos.values()]

    return ApiResponse(
        success=True,
        message="memos loaded",
        data=public_memos,
    )


# 이 API는 "데이터가 없어도 응답 모양은 유지한다"는 점을 보여 주는 예제입니다.
# 프론트엔드는 data가 None이어도 success/message 필드를 같은 방식으로 읽을 수 있습니다.
@app.get("/empty", response_model=ApiResponse)
def empty_response() -> ApiResponse:
    """데이터가 없어도 응답 구조를 일정하게 유지하는 예제입니다."""

    return ApiResponse(
        success=True,
        message="no data yet",
        data=None,
    )
