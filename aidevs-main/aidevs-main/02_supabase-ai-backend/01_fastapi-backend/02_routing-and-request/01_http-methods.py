"""HTTP Method(GET/POST/PUT/DELETE) 예제.

이 파일은 HTTP Method 개념을 나누어 읽고 실행해 보기 위한 학습용 파일입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\02_routing-and-request
    uvicorn 01_http-methods:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn 01_http-methods:app --reload

HTTP Method는 API 요청의 의도를 표현합니다.

GET    -> 데이터 조회
POST   -> 새 데이터 생성
PUT    -> 기존 데이터 전체 수정
DELETE -> 기존 데이터 삭제
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


# FastAPI 객체를 만듭니다.
# uvicorn 실행 명령의 마지막 `:app`은 아래 변수 이름 `app`과 연결됩니다.
app = FastAPI(title="HTTP Method Practice")




class MemoCreate(BaseModel):
    """POST 요청에서 받을 메모 데이터 형식입니다."""

    # Field는 문자열 길이, 숫자 범위 같은 검증 조건을 붙일 때 사용합니다.
    # title과 content는 둘 다 최소 1글자 이상이어야 합니다.
    title: str = Field(min_length=1, examples=["오늘 배운 내용"])
    content: str = Field(min_length=1, examples=["GET과 POST의 차이를 배웠습니다."])


class MemoUpdate(BaseModel):
    """PUT 요청에서 받을 수정 데이터 형식입니다."""

    # 수정 요청에서도 제목과 본문이 비어 있지 않도록 같은 검증 조건을 둡니다.
    id: int = Field(min = 1)
    title: str = Field(min_length=1, examples=["수정된 제목"])
    content: str = Field(min_length=1, examples=["수정된 내용입니다."])


# 수업용 메모리 저장소입니다.
# 서버를 재시작하면 데이터가 사라집니다.
# 실제 서비스에서는 Supabase 같은 DB에 저장합니다.
memos = {
    1: {"id": 1, "title": "FastAPI 시작", "content": "Swagger UI를 확인했습니다."},
}
# 새 메모를 만들 때 사용할 다음 id 값입니다.
# 현재 1번 메모가 이미 있으므로 다음 id는 2부터 시작합니다.
next_memo_id = 2


# @app.get은 GET 요청을 처리하는 API 주소를 만듭니다.
# GET은 서버에 있는 데이터를 조회할 때 사용합니다.
@app.get("/memos/list")
def list_memos():
    """전체 메모 목록을 조회합니다."""

    # dict.values()는 memos 안에 저장된 메모 값만 꺼냅니다.
    # JSON 응답으로 보내기 쉽게 list로 바꿔 반환합니다.
    return {"data": list(memos.values())}


# @app.post는 POST 요청을 처리합니다.
# POST는 새 데이터를 만들 때 사용합니다.
# status_code=201은 "새 리소스를 만들었다"는 의미의 HTTP 상태 코드입니다.
@app.post("/memos/create", status_code=201)
def create_memo(memo: MemoCreate):
    """새 메모를 생성합니다."""
    print(memo.content)
    print(memo.title)
    # 함수 안에서 바깥쪽 next_memo_id 값을 수정하려면 global이 필요합니다.
    global next_memo_id # 2

    # FastAPI는 요청 JSON을 MemoCreate 모델로 검증한 뒤 memo 인자에 넣어 줍니다.
    # memo.title, memo.content처럼 객체 속성으로 값을 꺼낼 수 있습니다.
    new_memo = {
        "id": next_memo_id,
        "title": memo.title,
        "content": memo.content,
    }
    # 새 메모를 메모리 저장소에 저장합니다.
    memos[next_memo_id] = new_memo
    # 다음 생성 요청에서 겹치지 않는 id를 쓰기 위해 1 증가시킵니다.
    next_memo_id += 1

    return {"message": "memo created"}


# @app.put은 PUT 요청을 처리합니다.
# PUT은 기존 데이터를 새 내용으로 수정할 때 사용합니다.
# {memo_id}는 URL 경로에서 값을 받아오는 Path Parameter입니다.
@app.put("/memos")
def update_memo(memo: MemoUpdate):
    """기존 메모를 수정합니다."""

    # 요청한 id가 저장소에 없으면 404 오류를 직접 발생시킵니다.
    if memo.id not in memos:
        raise HTTPException(status_code=404, detail="Memo not found")

    # 기존 메모를 같은 id의 새 데이터로 덮어씁니다.
    memos[memo.id] = {
        "id": memo.id,
        "title": memo.title,
        "content": memo.content,
    }

    return {"message": "memo updated", "data": memos[memo.id]}


# @app.delete는 DELETE 요청을 처리합니다.
# DELETE는 기존 데이터를 삭제할 때 사용합니다.
@app.delete("/memos/{memo_id}")
def delete_memo(memo_id: int):
    """기존 메모를 삭제합니다."""

    # 없는 메모를 삭제하려고 하면 404로 알려줍니다.
    if memo_id not in memos:
        print(f"{memo_id}는 없습니다 ........")
        # return {"message":f"{memo_id}는 없습니다 ........"}
        raise HTTPException(status_code=404, detail="Memo not found")

    # pop은 dict에서 값을 꺼내면서 동시에 삭제합니다.
    # 삭제한 데이터를 응답에 포함하면 무엇이 삭제됐는지 확인하기 쉽습니다.
    deleted = memos.pop(memo_id)
    return {"message": "memo deleted", "data": deleted}
