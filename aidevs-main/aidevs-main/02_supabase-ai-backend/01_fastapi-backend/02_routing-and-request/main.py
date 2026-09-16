"""메모 관리 API로 라우팅과 요청 데이터를 연습하는 FastAPI 예제입니다.

이 파일은 실제 실행용입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\02_routing-and-request
    uvicorn main:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn main:app --reload

브라우저:
    http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field


# 이 파일은 01~04 개념 파일에서 배운 내용을 하나의 메모 API로 합친 통합 예제입니다.
# uvicorn 명령의 `main:app`은 "main.py 파일 안의 app 변수"라는 뜻입니다.
app = FastAPI(
    title="Memo Routing Practice",
    description="메모 API 하나로 GET, POST, PUT, DELETE, Path, Query, Body를 연습합니다.",
    version="1.0.0",
)


class MemoCreate(BaseModel):
    """POST /memos 요청에서 받을 메모 생성 데이터입니다."""

    # POST /memos로 들어오는 JSON은 title과 content를 가져야 합니다.
    # Field(min_length=1)는 빈 문자열을 막기 위한 검증 조건입니다.
    title: str = Field(min_length=1, examples=["오늘 배운 내용"])
    content: str = Field(min_length=1, examples=["GET과 POST의 차이를 배웠습니다."])


class MemoUpdate(BaseModel):
    """PUT /memos/{memo_id} 요청에서 받을 메모 수정 데이터입니다."""

    # PUT은 기존 메모를 수정하는 요청이므로 생성과 비슷하게 title, content를 받습니다.
    title: str = Field(min_length=1, examples=["수정된 제목"])
    content: str = Field(min_length=1, examples=["수정된 내용입니다."])


# 서버 메모리에만 저장되는 수업용 데이터입니다.
# 서버를 종료하거나 다시 시작하면 처음 상태로 돌아갑니다.
# 이후 Supabase 단원에서는 이 부분을 테이블 저장으로 바꾸게 됩니다.
memos: dict[int, dict[str, object]] = {
    1: {
        "id": 1,
        "title": "FastAPI 시작",
        "content": "Swagger UI에서 API를 확인했습니다.",
    },
    2: {
        "id": 2,
        "title": "요청 데이터",
        "content": "Path, Query, Body의 차이를 배웁니다.",
    },
}
# 다음에 생성될 메모 id입니다.
# 이미 1, 2번 메모가 있으므로 새 메모는 3번부터 시작합니다.
next_memo_id = 3


# 서버가 살아 있는지 가장 먼저 확인하는 API입니다.
# 프론트엔드나 배포 환경에서도 /health는 자주 사용합니다.
@app.get("/health")
def health_check() -> dict[str, str]:
    """서버가 실행 중인지 확인합니다."""

    return {"status": "ok"}


# GET /memos는 전체 목록을 조회합니다.
# GET 요청은 서버 상태를 바꾸지 않고 데이터를 읽는 데 사용합니다.
@app.get("/memos")
def list_memos() -> dict[str, list[dict[str, object]]]:
    """GET Method로 전체 메모 목록을 조회합니다."""

    # dict 형태의 저장소를 API 응답으로 보내기 위해 값 목록만 list로 변환합니다.
    return {"data": list(memos.values())}


# GET /memos/search는 Query Parameter를 사용하는 검색 API입니다.
# 예: /memos/search?keyword=FastAPI&limit=5
@app.get("/memos/search")
def search_memos(
    # keyword는 보내지 않아도 되며, 기본값은 빈 문자열입니다.
    keyword: str = Query(default="", description="메모 제목과 내용에서 찾을 검색어"),
    # limit은 최소 1, 최대 20까지만 허용합니다.
    limit: int = Query(default=10, ge=1, le=20, description="최대 반환 개수"),
) -> dict[str, object]:
    """Query Parameter로 메모를 검색합니다."""

    # 검색 전에는 모든 메모를 대상으로 시작합니다.
    result = list(memos.values())

    if keyword:
        # 제목 또는 본문에 keyword가 들어 있는 메모만 남깁니다.
        # str(...)을 사용한 이유는 dict 값이 object 타입으로 선언되어 있기 때문입니다.
        result = [
            memo
            for memo in result
            if keyword.lower() in str(memo["title"]).lower()
            or keyword.lower() in str(memo["content"]).lower()
        ]

    # count는 실제 응답에 포함되는 개수를 보여 줍니다.
    # data는 limit 개수만큼 잘라서 반환합니다.
    return {
        "keyword": keyword,
        "limit": limit,
        "count": len(result[:limit]),
        "data": result[:limit],
    }


# GET /memos/{memo_id}는 Path Parameter를 사용하는 단건 조회 API입니다.
# 예: /memos/1 요청 -> memo_id 값은 1
@app.get("/memos/{memo_id}")
def get_memo(memo_id: int) -> dict[str, object]:
    """Path Parameter로 메모 id를 받아 메모 한 건을 조회합니다."""

    # URL에는 문자열로 들어오지만, memo_id: int 때문에 FastAPI가 숫자로 변환합니다.
    # 숫자로 바꿀 수 없는 값이면 FastAPI가 자동으로 422 오류를 반환합니다.
    if memo_id not in memos:
        # 형식은 맞지만 해당 id의 데이터가 없으면 404가 자연스럽습니다.
        raise HTTPException(status_code=404, detail="Memo not found")

    return {"data": memos[memo_id]}


# POST /memos는 Request Body를 받아 새 메모를 만드는 API입니다.
# status_code=201은 생성 성공을 뜻합니다.
@app.post("/memos", status_code=201)
def create_memo(memo: MemoCreate) -> dict[str, object]:
    """POST Method와 Request Body로 새 메모를 생성합니다."""

    # next_memo_id 값을 함수 안에서 증가시키기 위해 global을 사용합니다.
    global next_memo_id

    # memo는 이미 MemoCreate 모델로 검증된 값입니다.
    # 잘못된 JSON이 들어오면 이 함수가 실행되기 전에 FastAPI가 422 오류를 반환합니다.
    new_memo = {
        "id": next_memo_id,
        "title": memo.title,
        "content": memo.content,
    }
    # 새 메모를 메모리 저장소에 추가합니다.
    memos[next_memo_id] = new_memo
    # 다음 생성 요청에서 사용할 id를 준비합니다.
    next_memo_id += 1

    return {"message": "memo created", "data": new_memo}


# PUT /memos/{memo_id}는 Path Parameter와 Request Body를 함께 사용합니다.
# 어느 메모를 수정할지는 URL로 받고, 어떤 내용으로 바꿀지는 JSON Body로 받습니다.
@app.put("/memos/{memo_id}")
def update_memo(memo_id: int, memo: MemoUpdate) -> dict[str, object]:
    """Path Parameter와 Request Body로 기존 메모를 수정합니다."""

    # 수정하려는 메모가 없으면 404 오류를 반환합니다.
    if memo_id not in memos:
        raise HTTPException(status_code=404, detail="Memo not found")

    # 기존 id는 유지하고 title, content를 요청 Body 값으로 교체합니다.
    memos[memo_id] = {
        "id": memo_id,
        "title": memo.title,
        "content": memo.content,
    }

    return {"message": "memo updated", "data": memos[memo_id]}


# DELETE /memos/{memo_id}는 Path Parameter로 받은 id의 메모를 삭제합니다.
@app.delete("/memos/{memo_id}")
def delete_memo(memo_id: int) -> dict[str, object]:
    """DELETE Method와 Path Parameter로 기존 메모를 삭제합니다."""

    # 없는 메모를 삭제하려고 하면 404 오류를 반환합니다.
    if memo_id not in memos:
        raise HTTPException(status_code=404, detail="Memo not found")

    # pop은 값을 꺼내면서 동시에 dict에서 삭제합니다.
    deleted = memos.pop(memo_id)
    return {"message": "memo deleted", "data": deleted}
