r"""Streamlit API 연동 실습용 FastAPI 샘플 백엔드입니다.

실행:
    cd C:\aidev\03_supabase-ai-frontend
    .\.venv\Scripts\Activate.ps1
    cd .\03_api-integration\00_sample_backend
    uvicorn main:app --reload --host 127.0.0.1 --port 8000

위 명령에서 uvicorn 실행이 막히거나 오류가 나면:
    python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

실행 확인:
    http://127.0.0.1:8000/health
    http://127.0.0.1:8000/docs

이 파일은 Streamlit 프론트엔드가 FastAPI 백엔드를 호출하는 기초 흐름을 연습하기 위한
작은 서버입니다. 챗봇 API, Supabase 저장, 로그인 인증, Gemini API 호출은 여기서 다루지 않습니다.

챗봇 전용 백엔드는 05_ai-chatbot-interface/00_sample_backend에서 다룹니다.
"""

from fastapi import FastAPI  # FastAPI 서버 객체와 API 경로를 만들기 위해 가져옵니다.
from fastapi.middleware.cors import CORSMiddleware  # Streamlit 화면에서 FastAPI를 호출할 수 있도록 CORS 설정을 추가합니다.
from pydantic import BaseModel, Field  # 요청 JSON의 구조와 검증 규칙을 정의하기 위해 가져옵니다.


# app은 FastAPI 서버 전체를 대표하는 객체입니다.
# uvicorn main:app 명령에서 main은 main.py 파일을 뜻하고, app은 아래 변수 이름을 뜻합니다.
app = FastAPI(title="Frontend Practice Backend")  # Streamlit 연동 실습용 최소 백엔드 앱을 만듭니다.

# CORS는 Cross-Origin Resource Sharing의 줄임말입니다.
# 브라우저는 보안상 "서로 다른 출처(origin)" 사이의 API 호출을 기본적으로 제한합니다.
# 예를 들어 Streamlit 화면은 보통 http://localhost:8501 에서 실행되고,
# FastAPI 백엔드는 http://127.0.0.1:8000 또는 http://localhost:8000 에서 실행됩니다.
# 포트 번호가 8501과 8000으로 다르기 때문에 브라우저는 두 주소를 다른 출처로 판단합니다.
# 아래 설정은 수업용 Streamlit 주소에서 이 FastAPI 서버를 호출할 수 있도록 허용합니다.
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:8501",
#         "http://127.0.0.1:8501",
        
#     ],  # Streamlit 기본 실행 주소만 허용합니다.
#     allow_credentials=True,  # 쿠키나 인증 정보를 함께 보내는 요청도 허용할 수 있게 합니다.
#     allow_methods=["*"],  # GET, POST 등 모든 HTTP Method를 허용합니다.
#     allow_headers=["*"],  # Content-Type 같은 요청 헤더를 허용합니다.
# )


class MessageRequest(BaseModel):  # /api/message 요청 본문 구조를 정의합니다.
    """프론트엔드에서 이름과 메시지를 보낼 때 사용하는 요청 모델입니다."""

    # Field(...)에서 ...은 이 값이 필수라는 뜻입니다.
    # min_length=1은 빈 문자열을 허용하지 않겠다는 검증 규칙입니다.
    name: str = Field(..., min_length=1, description="메시지를 보낸 사용자 이름")
    message: str = Field(..., min_length=1, description="프론트엔드에서 보낸 메시지")


class ScoreRequest(BaseModel):  # /api/score-feedback 요청 본문 구조를 정의합니다.
    """프론트엔드에서 이름과 점수를 보낼 때 사용하는 요청 모델입니다."""

    # ge=0은 0 이상, le=100은 100 이하라는 뜻입니다.
    # 사용자가 범위를 벗어난 값을 보내면 FastAPI가 자동으로 422 오류를 반환합니다.
    name: str = Field(..., min_length=1, description="점수를 입력한 사용자 이름")
    score: int = Field(..., ge=0, le=100, description="0부터 100 사이의 점수")


def print_api_running(method: str, path: str):
    """현재 실행된 API URL 정보를 FastAPI 터미널에 출력합니다."""

    # 이 함수는 API가 호출될 때마다 "어떤 주소가 실행되었는지"를 확인하기 위한 학습용 출력 함수입니다.
    # 수업에서는 FastAPI 서버를 보통 127.0.0.1:8000 주소로 실행하므로, 아래 base_url을 함께 보여 줍니다.
    base_url = "http://127.0.0.1:8000"
    print(f"[api running] {method} {base_url}{path}")


def print_client_request(api_name: str, payload: BaseModel):
    """클라이언트가 보낸 요청 데이터를 FastAPI 터미널에 출력합니다."""

    # Streamlit 화면에서 버튼을 누르면 프론트엔드가 FastAPI로 JSON 데이터를 보냅니다.
    # 이 함수는 그 JSON 데이터가 백엔드에 어떤 값으로 도착했는지 확인하기 위한 학습용 출력 함수입니다.
    # 서버를 실행한 PowerShell 터미널에서 출력 내용을 확인할 수 있습니다.
    if hasattr(payload, "model_dump"):
        request_data = payload.model_dump()  # Pydantic v2에서 모델을 dict로 바꾸는 방법입니다.
    else:
        request_data = payload.dict()  # Pydantic v1을 사용하는 환경을 위한 예비 코드입니다.

    print("\n" + "=" * 60)
    print(f"[client request] {api_name}")
    print("클라이언트에서 전송한 데이터:")

    for key, value in request_data.items():
        print(f"- {key}: {value}")

    print("=" * 60)


@app.get("/")  # 브라우저에서 루트 주소를 열었을 때 확인할 기본 API입니다.
def read_root():
    """서버가 실행 중인지 가장 간단하게 확인하는 루트 API입니다."""

    print_api_running("GET", "/")

    # dict를 반환하면 FastAPI가 자동으로 JSON 응답으로 변환합니다.
    return {"message": "Frontend Practice Backend is running"}


@app.get("/health")  # 프론트엔드가 서버 실행 상태를 확인할 때 호출하는 API입니다.
def health_check():
    """Streamlit 화면에서 백엔드 연결 상태를 확인할 때 사용하는 API입니다."""

    print_api_running("GET", "/health")

    # 프론트엔드에서는 이 응답의 status 값이 ok인지 확인해 서버 연결 여부를 판단할 수 있습니다.
    return {"status": "ok", "service": "frontend-practice-backend"}


@app.get("/api/courses")  # 과정 목록처럼 서버에서 데이터를 조회하는 GET 예제입니다.
def get_courses():
    """서버에서 목록 데이터를 조회하는 GET API 예제입니다."""
    # GET 요청은 보통 데이터를 새로 만들지 않고, 서버에 있는 데이터를 조회할 때 사용합니다.
    # Streamlit에서는 requests.get(...)으로 이 API를 호출한 뒤 courses 값을 화면에 출력할 수 있습니다.
    return {
        "courses": ["Python", "Streamlit", "FastAPI", "Supabase"],
        "count": 4,
    }


@app.post("/api/message")  # 프론트엔드가 JSON 데이터를 보내는 POST 예제입니다.
def create_message(request: MessageRequest):
    """프론트엔드가 보낸 이름과 메시지를 받아 응답 문장을 만들어 반환합니다."""

    print_api_running("POST", "/api/message")

    # request에는 MessageRequest 모델을 통과한 값만 들어옵니다.
    # 예를 들어 name이 비어 있으면 이 함수까지 오기 전에 FastAPI가 검증 오류를 반환합니다.
    print_client_request("/api/message", request)

    return {
        "name": request.name,
        "message": request.message,
        "reply": f"{request.name}님, 메시지를 받았습니다: {request.message}",
    }


@app.post("/api/score-feedback")  # 점수를 받아 조건문으로 피드백을 만드는 POST 예제입니다.
def create_score_feedback(request: ScoreRequest):
    """사용자가 보낸 점수에 따라 다른 피드백 문장을 반환합니다."""

    print_api_running("POST", "/api/score-feedback")

    # 백엔드에서는 프론트엔드가 보낸 값을 기준으로 조건문, 계산, 저장, 외부 API 호출 등을 처리합니다.
    # 이 예제에서는 가장 단순하게 점수 범위에 따라 피드백 문장만 바꿉니다.
    print_client_request("/api/score-feedback", request)

    if request.score >= 80:
        feedback = "좋습니다. 다음 단계로 넘어갈 준비가 되어 있습니다."
    elif request.score >= 50:
        feedback = "기본 흐름은 이해했습니다. 예제를 한 번 더 수정해 보세요."
    else:
        feedback = "기초 예제를 다시 실행해 보세요."

    return {
        "name": request.name,
        "score": request.score,
        "feedback": feedback,
    }

