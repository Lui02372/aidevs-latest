r"""04_state-session-and-data 전용 FastAPI 샘플 백엔드입니다.

이 파일은 Streamlit 화면에서 회원가입, 로그인, access token 저장,
Authorization header, 보호된 API 호출 흐름을 연습하기 위한 수업용 백엔드입니다.

실행 순서:
    1. PowerShell에서 03_supabase-ai-frontend 폴더로 이동합니다.

       cd C:\aidev\03_supabase-ai-frontend

    2. 03 과정 가상환경을 활성화합니다.

       .\.venv\Scripts\Activate.ps1

    3. 이 파일이 있는 샘플 백엔드 폴더로 이동합니다.

       cd .\04_state-session-and-data\00_sample_backend

    4. FastAPI 서버를 실행합니다.

       uvicorn main:app --reload --host 127.0.0.1 --port 8000

    5. 브라우저에서 API 문서를 확인합니다.

       http://127.0.0.1:8000/docs

Swagger에서 보호된 API를 테스트할 때:
    /api/me, /api/conversations, /api/service-logs는 Authorization header가 필요합니다.
    오른쪽 위 Authorize 버튼에 아래 token만 입력합니다.

       sample-access-token

주의:
    - 이 백엔드는 Supabase Auth를 사용하지 않는 mock 서버입니다.
    - 데이터는 Python 메모리에만 저장됩니다.
    - 서버를 재시작하면 수업 중 새로 가입한 계정과 로그는 초기화됩니다.
    - 실제 서비스의 회원가입, 로그인, JWT 검증, RLS는 백엔드 과정에서 다룹니다.
"""

from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field


app = FastAPI(title="State Session Sample API")


# Swagger Docs에서 오른쪽 위 Authorize 버튼으로 Bearer token을 넣기 위한 설정입니다.
# Authorize 버튼을 누른 뒤 아래 token 값만 입력합니다.
#
#     sample-access-token
#
# HTTPBearer가 요청을 보낼 때 "Bearer "를 자동으로 붙입니다.
# auto_error=False로 두면 인증 정보가 없을 때 아래 인증 함수에서
# 초보자가 이해하기 쉬운 한국어 오류를 반환할 수 있습니다.
authorization_scheme = HTTPBearer(
    auto_error=False,
    description="예: sample-access-token",
)


class SignupRequest(BaseModel):
    """회원가입 요청 데이터의 모양을 정의합니다."""

    username: str = Field(min_length=3, examples=["student"])
    password: str = Field(min_length=4, examples=["1234"])
    display_name: str = Field(min_length=1, examples=["수강생"])


class LoginRequest(BaseModel):
    """로그인 요청 데이터의 모양을 정의합니다."""

    username: str = Field(examples=["student"])
    password: str = Field(examples=["1234"])


class ConversationRequest(BaseModel):
    """새 대화 메시지를 저장할 때 받는 요청 데이터입니다."""

    message: str = Field(min_length=1, examples=["오늘 학습한 내용을 요약해 주세요."])


# 수업용 사용자 저장소입니다.
# 실제 서비스에서는 Supabase Auth 또는 users 테이블을 사용합니다.
USERS: dict[str, dict] = {
    "student": {
        "username": "student",
        "password": "1234",
        "display_name": "수강생",
        "role": "learner",
    }
}


# 수업용 고정 access token입니다.
# 이 샘플 백엔드는 실제 JWT를 발급하지 않고, 아래 문자열 하나만 token처럼 사용합니다.
# Swagger Docs의 Authorize 버튼에는 "sample-access-token"만 입력하면 됩니다.
SAMPLE_ACCESS_TOKEN = "sample-access-token"


# access token과 username의 관계를 저장합니다.
# 처음에는 student 계정에 연결되어 있고, 다른 사용자로 로그인하면 같은 token이 그 사용자에게 연결됩니다.
# 실제 서비스에서는 사용자마다 서로 다른 JWT를 발급하고 만료 시간과 서명을 검증해야 합니다.
TOKENS: dict[str, str] = {SAMPLE_ACCESS_TOKEN: "student"}


CONVERSATIONS = [
    {"id": 1, "role": "user", "content": "오늘 학습한 내용을 요약해 주세요."},
    {"id": 2, "role": "assistant", "content": "Streamlit 상태 관리와 인증 흐름을 학습했습니다."},
]


SERVICE_LOGS = [
    {
        "id": 1,
        "event": "sample_backend_started",
        "status": "ok",
        "message": "04_state-session-and-data 샘플 백엔드 준비",
        "created_at": "2026-06-15T09:00:00",
    },
    {
        "id": 2,
        "event": "login_success",
        "status": "ok",
        "message": "student 계정 로그인 성공 예시",
        "created_at": "2026-06-15T09:05:00",
    },
]


def now_iso() -> str:
    """현재 시각을 로그에 저장하기 좋은 문자열로 변환합니다."""

    return datetime.now().isoformat(timespec="seconds")


def add_service_log(event: str, status_text: str, message: str) -> None:
    """서비스 로그 목록에 새 로그를 추가합니다."""

    SERVICE_LOGS.append(
        {
            "id": len(SERVICE_LOGS) + 1,
            "event": event,
            "status": status_text,
            "message": message,
            "created_at": now_iso(),
        }
    )


def get_username_from_credentials(
    credentials: HTTPAuthorizationCredentials | None,
) -> str:
    """HTTPBearer가 분리한 인증 정보에서 사용자 이름을 찾습니다."""

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header가 없습니다. Bearer token을 보내야 합니다.",
        )

    token = credentials.credentials
    username = TOKENS.get(token)

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 token입니다. sample-access-token을 사용하세요.",
        )

    return username


@app.get("/")
def root() -> dict:
    """백엔드 서버가 실행 중인지 간단히 확인하는 기본 API입니다."""

    return {
        "message": "04_state-session-and-data sample backend is running",
        "docs": "http://127.0.0.1:8000/docs",
        "swagger_authorization_value": "sample-access-token",
    }


@app.get("/health")
def health() -> dict:
    """헬스 체크 API입니다."""

    return {"status": "ok"}


@app.post("/api/signup", status_code=status.HTTP_201_CREATED)
def signup(request: SignupRequest) -> dict:
    """회원가입 API입니다."""

    if request.username in USERS:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 가입된 사용자 이름입니다.",
        )

    USERS[request.username] = {
        "username": request.username,
        "password": request.password,
        "display_name": request.display_name,
        "role": "learner",
    }
    add_service_log("signup_success", "ok", f"{request.username} 회원가입")

    return {
        "message": "회원가입이 완료되었습니다. 이제 로그인할 수 있습니다.",
        "username": request.username,
        "display_name": request.display_name,
    }


@app.post("/api/login")
def login(request: LoginRequest) -> dict:
    """로그인 API입니다.

    username과 password가 맞으면 수업용 access_token을 반환합니다.
    이 예제에서는 초보자가 Swagger 테스트에서 헷갈리지 않도록 token 값을 하나로 고정합니다.
    Swagger의 Authorize 버튼에는 아래 token 값만 입력합니다.

        sample-access-token
    """

    user = USERS.get(request.username)
    if user is None or user["password"] != request.password:
        add_service_log("login_failed", "warning", f"{request.username} 로그인 실패")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자 이름 또는 비밀번호가 올바르지 않습니다.",
        )

    token = SAMPLE_ACCESS_TOKEN
    TOKENS[token] = request.username
    add_service_log("login_success", "ok", f"{request.username} 로그인 성공")

    return {
        "access_token": token,
        "token_type": "bearer",
        "username": request.username,
        "display_name": user["display_name"],
        "swagger_authorization_value": token,
    }


@app.get("/api/me")
def get_me(
    credentials: HTTPAuthorizationCredentials | None = Depends(authorization_scheme),
) -> dict:
    """로그인한 사용자 정보를 반환하는 보호된 API입니다."""

    username = get_username_from_credentials(credentials)
    user = USERS[username]

    return {
        "username": user["username"],
        "display_name": user["display_name"],
        "role": user["role"],
    }


@app.get("/api/conversations")
def get_conversations(
    credentials: HTTPAuthorizationCredentials | None = Depends(authorization_scheme),
) -> dict:
    """대화 이력 목록을 반환하는 보호된 API입니다."""

    username = get_username_from_credentials(credentials)
    add_service_log("conversation_fetch", "ok", f"{username} 대화 이력 조회")

    return {"items": CONVERSATIONS}


@app.post("/api/conversations")
def create_conversation(
    request: ConversationRequest,
    credentials: HTTPAuthorizationCredentials | None = Depends(authorization_scheme),
) -> dict:
    """새 대화 메시지를 저장하는 보호된 API입니다."""

    username = get_username_from_credentials(credentials)

    item = {
        "id": len(CONVERSATIONS) + 1,
        "role": "user",
        "content": request.message,
    }
    CONVERSATIONS.append(item)
    add_service_log("conversation_create", "ok", f"{username} 대화 메시지 저장")

    return item


@app.get("/api/service-logs")
def get_service_logs(
    credentials: HTTPAuthorizationCredentials | None = Depends(authorization_scheme),
) -> dict:
    """서비스 로그 목록을 반환하는 보호된 API입니다."""

    get_username_from_credentials(credentials)
    return {"items": SERVICE_LOGS}
