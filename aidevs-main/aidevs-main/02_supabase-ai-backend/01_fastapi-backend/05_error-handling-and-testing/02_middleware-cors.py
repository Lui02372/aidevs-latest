"""CORS 미들웨어 예제.

실행:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\05_error-handling-and-testing
    uvicorn 02_middleware-cors:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn 02_middleware-cors:app --reload

확인:
    http://127.0.0.1:8000/health

CORS는 브라우저에서 다른 주소의 API를 호출할 때 적용되는 보안 규칙입니다.
예를 들어 Streamlit 화면이 localhost:8501에서 실행되고,
FastAPI 서버가 localhost:8000에서 실행되면 출처(origin)가 다릅니다.

CORS는 Cross-Origin Resource Sharing의 줄임말입니다.
한국어로 풀면 "서로 다른 출처 사이의 리소스 공유" 정도로 이해할 수 있습니다.

여기서 출처(origin)는 보통 아래 3가지를 합친 개념입니다.

1. 프로토콜: http 또는 https
2. 도메인 또는 호스트: localhost, 127.0.0.1, example.com
3. 포트: 8000, 8501 같은 번호

즉, 사용자가 브라우저에서 Streamlit 화면인 http://localhost:8501 에 접속한 뒤,
그 화면에서 FastAPI 서버인 http://localhost:8000 으로 API 요청을 보내면
브라우저는 "서로 다른 출처로 요청을 보내는구나"라고 판단합니다.

FastAPI 서버가 이 요청을 허용한다는 CORS 응답 헤더를 보내지 않으면
브라우저는 보안상 응답을 막고 CORS 오류를 표시할 수 있습니다.

이 예제에서는 이후 Streamlit 프론트엔드가 FastAPI 백엔드를 호출하는 상황을 대비해
localhost:8501, 127.0.0.1:8501에서 오는 요청을 허용하는 설정을 연습합니다.
실제 Streamlit 연동은 `03_supabase-ai-frontend` 과정에서 다시 진행합니다.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# FastAPI 앱 객체입니다.
# uvicorn 실행 명령의 마지막 `:app`은 아래 변수 이름 `app`과 연결됩니다.
app = FastAPI(title="CORS Middleware Practice")


# 수업에서는 로컬 개발 주소만 허용합니다.
# 실제 운영에서는 "*"로 전체 허용하지 말고 필요한 도메인만 명시합니다.
# Streamlit 기본 포트는 보통 8501이므로 아래 두 주소를 허용합니다.
allowed_origins = [
    "http://localhost:8501",
    "http://127.0.0.1:8501",
]


# add_middleware는 모든 요청/응답 사이에 공통 기능을 끼워 넣는 설정입니다.
# 여기서는 브라우저가 허용된 프론트엔드 주소에서 FastAPI를 호출할 수 있게 합니다.
app.add_middleware(
    CORSMiddleware,
    # 어떤 출처(origin)의 브라우저 요청을 허용할지 정합니다.
    allow_origins=allowed_origins,
    # 쿠키나 인증 정보가 필요한 요청을 허용할지 정합니다.
    allow_credentials=True,
    # GET, POST, PUT, DELETE 등 어떤 HTTP Method를 허용할지 정합니다.
    allow_methods=["*"],
    # Authorization, Content-Type 같은 요청 헤더를 허용합니다.
    allow_headers=["*"],
)


# CORS 설정 자체는 브라우저에서 다른 origin으로 호출할 때 체감됩니다.
# /health는 서버가 정상 실행 중인지 빠르게 확인하는 API입니다.
@app.get("/health")
def health_check():
    """프론트엔드에서 백엔드 연결 상태를 확인할 때 사용할 수 있습니다."""

    return {"status": "ok", "cors": "enabled"}
