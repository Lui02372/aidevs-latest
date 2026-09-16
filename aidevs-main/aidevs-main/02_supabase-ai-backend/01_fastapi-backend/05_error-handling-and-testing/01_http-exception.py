"""HTTPException 예외 처리 예제.

실행:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\05_error-handling-and-testing
    uvicorn 01_http-exception:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn 01_http-exception:app --reload

확인:
    http://127.0.0.1:8000/items/1
    http://127.0.0.1:8000/items/999
    http://127.0.0.1:8000/items/2/buy

API에서는 문제가 생겼을 때 단순히 Python 오류를 보여주면 안 됩니다.
클라이언트가 이해할 수 있는 HTTP 상태 코드와 메시지를 반환해야 합니다.
"""

from fastapi import FastAPI, HTTPException


# FastAPI 앱 객체입니다.
# uvicorn 실행 명령의 마지막 `:app`은 아래 변수 이름 `app`과 연결됩니다.
app = FastAPI(title="HTTPException Practice")


# 데이터베이스를 배우기 전이므로 dict를 임시 저장소로 사용합니다.
# key는 상품 id이고, value는 상품 정보입니다.
items = {
    1: {"id": 1, "name": "Python 교재", "price": 18000},
    2: {"id": 2, "name": "FastAPI 실습 노트", "price": 0},
}


# Path Parameter로 item_id를 받아 상품 하나를 조회합니다.
# 예: /items/1 요청 -> item_id 값은 1
@app.get("/items/{item_id}")
def get_item(item_id: int):
    """상품 id로 데이터를 조회합니다."""

    if item_id not in items:
        # 404는 요청한 리소스를 찾을 수 없다는 뜻입니다.
        # raise HTTPException을 사용하면 FastAPI가 JSON 오류 응답을 만들어 줍니다.
        raise HTTPException(status_code=404, detail="Item not found")

    return {"data": items[item_id]}


# 같은 상품 데이터를 사용하지만, 이번에는 "구매 가능 여부"라는 서비스 규칙을 확인합니다.
@app.get("/items/{item_id}/buy")
def buy_item(item_id: int):
    """구매 가능 여부를 확인하는 예제입니다."""

    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    item = items[item_id]

    if item["price"] <= 0:
        # 400은 클라이언트 요청 조건이 잘못되었을 때 사용할 수 있습니다.
        # 여기서는 무료 상품을 구매하려는 요청을 잘못된 요청으로 처리합니다.
        raise HTTPException(status_code=400, detail="Free item cannot be purchased")

    return {"message": "purchase ready", "data": item}
