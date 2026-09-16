"""외부 API 호출 구조 예제입니다.

이 파일은 외부 API 호출 개념을 나누어 읽고 실행해 보기 위한 학습용 파일입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\04_async-and-external-api
    uvicorn 02_external-api-structure:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn 02_external-api-structure:app --reload

실제 외부 API를 호출할 때는 httpx.AsyncClient를 자주 사용합니다.
이 예제는 네트워크가 가능한 공개 테스트 API를 호출합니다.
"""

# httpx는 Python에서 HTTP 요청을 보낼 때 사용하는 라이브러리입니다.
# AsyncClient는 async def 함수 안에서 await와 함께 사용할 수 있는 비동기 HTTP 클라이언트입니다.
import httpx
from fastapi import FastAPI, HTTPException


# FastAPI 앱 객체입니다.
# uvicorn 실행 명령의 마지막 `:app`은 아래 변수 이름 `app`과 연결됩니다.
app = FastAPI(title="External API Structure Practice")


# 이 API는 우리 서버가 직접 데이터를 만드는 대신,
# 외부 테스트 API에서 데이터를 가져와 가공한 뒤 응답합니다.
@app.get("/external/posts/{post_id}")
async def get_external_post(post_id: int):
    """외부 API에서 게시글 하나를 가져와 우리 API 응답으로 반환합니다."""

    # f-string을 사용해 요청할 외부 API 주소를 만듭니다.
    # 예: post_id가 1이면 https://jsonplaceholder.typicode.com/posts/1
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"

    try:
        # AsyncClient는 async 함수 안에서 외부 HTTP 요청을 보낼 때 사용합니다.
        # timeout=5는 외부 API가 너무 오래 응답하지 않을 때 5초 뒤 중단하기 위한 설정입니다.
        async with httpx.AsyncClient(timeout=5) as client:
            # await client.get(url)은 외부 서버 응답을 기다립니다.
            response = await client.get(url)
            # 상태 코드가 4xx 또는 5xx이면 HTTPStatusError를 발생시킵니다.
            response.raise_for_status()
    except httpx.HTTPStatusError as error:
        # 외부 API가 404, 500 같은 오류 상태 코드를 반환한 경우입니다.
        # 우리 API도 그 상태 코드를 사용자에게 전달합니다.
        raise HTTPException(
            status_code=error.response.status_code,
            detail="External API returned an error",
        ) from error
    except httpx.RequestError as error:
        # 네트워크 연결 실패, DNS 문제, timeout 같은 요청 자체의 실패입니다.
        # 이때는 우리 서버가 외부 서비스에 닿지 못한 것이므로 503으로 응답합니다.
        raise HTTPException(
            status_code=503,
            detail="External API is not reachable",
        ) from error

    # response.json()은 외부 API 응답 JSON을 Python dict로 바꿉니다.
    external_data = response.json()

    return {
        "source": "jsonplaceholder",
        # raw 데이터 전체를 바로 넘기기보다, 우리 서비스에서 필요한 값만 골라 응답합니다.
        "data": {
            "id": external_data["id"],
            "title": external_data["title"],
            "body_preview": external_data["body"][:60],
        },
    }
