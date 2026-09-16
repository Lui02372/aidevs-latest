"""StreamingResponse 기초 예제입니다.

이 파일은 스트리밍 응답 개념을 나누어 읽고 실행해 보기 위한 학습용 파일입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\04_async-and-external-api
    uvicorn 04_streaming-response:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn 04_streaming-response:app --reload

이 파일은 스트리밍 응답의 개념을 보여주는 아주 작은 예제입니다.
Server-Sent Events(SSE)를 이용한 실제 AI 응답 스트리밍 통합은
`04_supabase-ai-mini-project`에서 백엔드, 프론트엔드, Supabase 저장과 함께 다룹니다.
"""

# asyncio.sleep()으로 단어가 조금씩 늦게 도착하는 상황을 흉내 냅니다.
import asyncio

# AsyncGenerator[str, None]은 "문자열을 비동기로 하나씩 만들어 내는 함수"라는 타입 힌트입니다.
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse


# FastAPI 앱 객체입니다.
# uvicorn 실행 명령의 마지막 `:app`은 아래 변수 이름 `app`과 연결됩니다.
app = FastAPI(title="Streaming Response Practice")


async def generate_words() -> AsyncGenerator[str, None]:
    """단어를 하나씩 천천히 보내는 generator입니다."""

    # 한 번에 긴 문장을 보내지 않고 단어를 하나씩 보낼 예정입니다.
    words = ["FastAPI", "can", "send", "streaming", "responses."]

    for word in words:
        # 실제 AI 스트리밍에서는 모델이 다음 토큰을 만들 때까지 시간이 걸립니다.
        # 여기서는 그 상황을 0.5초 대기로 흉내 냅니다.
        await asyncio.sleep(0.5)
        # 일반 텍스트 스트리밍에서는 문자열 조각을 순서대로 yield합니다.
        # yield는 값을 하나 반환하고 함수 실행 상태를 잠시 멈춰 두는 동작입니다.
        yield word + " "


# GET /stream에 접속하면 응답을 한 번에 받는 대신 조금씩 받습니다.
@app.get("/stream")
async def stream_text():
    """텍스트를 한 번에 보내지 않고 조금씩 나누어 보냅니다."""

    # StreamingResponse는 generator가 yield하는 값을 클라이언트에 순서대로 전달합니다.
    # media_type="text/plain"은 일반 텍스트 응답이라는 뜻입니다.
    return StreamingResponse(generate_words(), media_type="text/plain")
