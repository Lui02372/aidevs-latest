r"""FastAPI에서 Supabase Auth를 호출하는 최소 예제입니다.

이 예제는 Swagger UI에서 회원가입, 로그인, 현재 사용자 확인 흐름을 확인합니다.
수강생은 이 파일을 통해 아래 흐름을 한 번에 연결해서 볼 수 있습니다.

1. FastAPI가 요청을 받습니다.
2. FastAPI가 Supabase Auth API에 회원가입 또는 로그인 요청을 보냅니다.
3. 로그인에 성공하면 Supabase가 access_token을 발급합니다.
4. 클라이언트는 access_token을 Authorization 헤더에 담아 보호 API를 호출합니다.
5. FastAPI는 그 token을 Supabase에 확인시켜 현재 사용자를 알아냅니다.

이 예제의 핵심은 "비밀번호를 FastAPI가 직접 검사하지 않는다"는 점입니다.
비밀번호 확인, 사용자 생성, token 발급은 Supabase Auth가 담당합니다.
FastAPI는 Supabase Auth와 통신하는 API 서버 역할을 합니다.

실행 전 준비:
    C:\aidev\02_supabase-ai-backend\.env 파일에
    SUPABASE_URL, SUPABASE_ANON_KEY 값을 입력합니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\04_supabase-auth-and-rls
    ..\..\.venv\Scripts\Activate.ps1
    python -m uvicorn 01_fastapi_supabase_auth:app --reload --host 127.0.0.1 --port 8002

Swagger 확인:
    http://127.0.0.1:8002/docs
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
from supabase import create_client


# 이 파일 위치:
#   C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\04_supabase-auth-and-rls
#
# parents[0] -> 04_supabase-auth-and-rls
# parents[1] -> 03_supabase-db-and-auth
# parents[2] -> 02_supabase-ai-backend
#
# 따라서 PROJECT_ROOT는 .env 파일이 있는 02_supabase-ai-backend 폴더를 가리킵니다.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"

# HTTPBearer를 사용하면 Swagger UI 오른쪽 위에 Authorize 버튼이 생깁니다.
# 이 버튼은 Authorization 헤더를 쉽게 넣기 위한 Swagger의 보조 기능입니다.
#
# 수강생 흐름:
#   1. /auth/signin을 실행합니다.
#   2. 응답으로 받은 access_token을 복사합니다.
#   3. Swagger의 Authorize 버튼에 붙여 넣습니다.
#   4. /me를 실행하면 Swagger가 Authorization 헤더를 자동으로 보냅니다.
bearer_security = HTTPBearer(auto_error=False)

# FastAPI 애플리케이션 객체입니다.
# python -m uvicorn 명령의 "01_fastapi_supabase_auth:app"에서 app이 바로 이 변수입니다.
app = FastAPI(
    title="Supabase Auth FastAPI Example",
    description="Supabase Auth sign up/sign in과 Bearer token 확인 흐름을 Swagger에서 실습합니다.",
)


class AuthRequest(BaseModel):
    """회원가입과 로그인 요청 Body입니다.

    Swagger에서 /auth/signup, /auth/signin을 열면 이 모델이 요청 예시로 표시됩니다.
    email과 password를 JSON Body에 넣어 보내는 구조를 연습하기 위한 모델입니다.
    """

    email: str = Field(
        examples=["student-auth-test@example.com"],
        description="Supabase Auth에 사용할 테스트 이메일입니다.",
    )
    password: str = Field(
        min_length=6,
        examples=["test-password-123"],
        description="Supabase Auth에 사용할 테스트 비밀번호입니다.",
    )


class UserInfo(BaseModel):
    """응답에서 보여 줄 사용자 정보입니다.

    Supabase Auth의 user 객체에는 더 많은 정보가 들어 있지만,
    초반 실습에서는 현재 사용자 id와 email만 확인하면 충분합니다.
    이 id는 나중에 사용자별 데이터 접근을 구현할 때 기준이 됩니다.
    """

    id: str
    email: str | None = None


class SignUpResponse(BaseModel):
    """회원가입 요청 결과입니다.

    가입 요청이 성공했다고 해서 항상 바로 로그인 가능한 것은 아닙니다.
    Supabase의 Confirm email 설정이 켜져 있으면 이메일 인증 후 로그인해야 합니다.
    """

    message: str
    user: UserInfo | None = None


class SignInResponse(BaseModel):
    """로그인 성공 결과입니다.

    access_token은 Swagger에서 /me를 호출할 때 필요합니다.
    수업 중 화면 공유나 GitHub에는 실제 token 값을 노출하지 않습니다.
    """

    access_token: str
    token_type: str = "bearer"
    user: UserInfo


def read_required_env(name: str) -> str:
    """필수 환경 변수를 읽고, 비어 있거나 예시 값이면 HTTP 500 오류를 냅니다.

    .env.example에는 `your-supabase-anon-key` 같은 안내용 값이 들어 있습니다.
    이런 값은 실제 접속 정보가 아니므로 Supabase 요청 전에 막습니다.
    """

    value = os.getenv(name, "").strip()

    if not value:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{name} 환경변수를 C:\\aidev\\02_supabase-ai-backend\\.env에 설정하세요.",
        )

    if value.startswith(("your-", "https://your-")):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{name}에 실제 값을 입력하세요. Supabase Dashboard에서 복사한 값을 사용해야 합니다.",
        )

    return value


def get_supabase():
    """Supabase client를 만듭니다.

    Auth API는 사용자를 대신해 호출하는 흐름이므로 service role key가 아니라 anon key를 사용합니다.

    여기서 중요한 구분:
    - SUPABASE_ANON_KEY: 클라이언트/사용자 흐름에서 사용하는 공개 가능한 key입니다.
    - SUPABASE_SERVICE_ROLE_KEY: RLS를 우회할 수 있는 서버 전용 key입니다.

    회원가입, 로그인, 현재 사용자 확인 같은 Auth 흐름은 사용자를 대신하는 요청이므로
    SUPABASE_ANON_KEY로 진행합니다.
    """

    load_dotenv(ENV_PATH)

    supabase_url = read_required_env("SUPABASE_URL")
    anon_key = read_required_env("SUPABASE_ANON_KEY")

    return create_client(supabase_url, anon_key)


@app.get("/health")
def health_check() -> dict[str, str]:
    """서버가 실행 중인지 확인합니다.

    Supabase 연결이나 로그인 전에 FastAPI 서버 자체가 켜졌는지 먼저 확인합니다.
    Swagger에서 가장 먼저 실행해 보기 좋은 endpoint입니다.
    """

    return {"status": "ok"}


@app.post("/auth/signup", response_model=SignUpResponse)
def sign_up(request: AuthRequest) -> SignUpResponse:
    """Supabase Auth에 회원가입 요청을 보냅니다.

    Swagger에서 입력한 email/password를 Supabase Auth의 sign_up API로 전달합니다.
    FastAPI가 직접 사용자 테이블에 insert하지 않습니다.
    사용자 생성은 Supabase Auth가 처리합니다.
    """

    supabase = get_supabase()

    try:
        # Supabase Python client의 Auth 기능을 사용해 회원가입을 요청합니다.
        # 요청 Body는 {"email": "...", "password": "..."} 형태입니다.
        response = supabase.auth.sign_up(
            {
                "email": request.email,
                "password": request.password,
            }
        )
    except Exception as error:
        # 예: 이메일 형식 오류, email rate limit exceeded, provider 설정 문제 등이 여기로 올 수 있습니다.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Supabase sign up 실패: {error}",
        ) from error

    user = response.user
    # Confirm email이 켜져 있어도 user 객체는 생성되어 돌아올 수 있습니다.
    # 하지만 이메일 인증 전에는 /auth/signin이 실패할 수 있습니다.
    return SignUpResponse(
        message="sign up request sent",
        user=UserInfo(id=user.id, email=user.email) if user else None,
    )


@app.post("/auth/signin", response_model=SignInResponse)
def sign_in(request: AuthRequest) -> SignInResponse:
    """Supabase Auth에 로그인 요청을 보내고 access token을 반환합니다.

    로그인에 성공하면 Supabase는 session을 반환합니다.
    session 안의 access_token은 이후 /me 같은 보호 API를 호출할 때 사용합니다.
    """

    supabase = get_supabase()

    try:
        # 가입할 때 사용한 email/password와 동일한 값으로 로그인합니다.
        # Confirm email이 켜져 있으면 이메일 인증 전에는 Invalid login credentials가 나올 수 있습니다.
        response = supabase.auth.sign_in_with_password(
            {
                "email": request.email,
                "password": request.password,
            }
        )
    except Exception as error:
        # 비밀번호가 틀렸거나, 이메일 인증이 끝나지 않았거나, 사용자가 없을 때 주로 발생합니다.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Supabase sign in 실패: {error}",
        ) from error

    if response.user is None or response.session is None:
        # Supabase 설정에 따라 user/session이 비어 있을 수 있으므로 명확한 오류로 안내합니다.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인 응답에 user 또는 session이 없습니다. 이메일 인증 설정을 확인하세요.",
        )

    # 실제 서비스에서는 access_token을 응답으로 그대로 보여 주는 방식을 신중히 다뤄야 합니다.
    # 여기서는 Swagger에서 Bearer token 흐름을 학습하기 위해 그대로 반환합니다.
    return SignInResponse(
        access_token=response.session.access_token,
        user=UserInfo(id=response.user.id, email=response.user.email),
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_security),
) -> UserInfo:
    """Authorization 헤더의 Bearer token으로 현재 사용자를 확인합니다.

    이 함수는 /me endpoint가 실행되기 전에 먼저 실행되는 의존성 함수입니다.
    FastAPI의 Depends는 "이 endpoint를 실행하기 전에 필요한 값을 준비하라"는 뜻입니다.

    여기서는 Swagger Authorize에 넣은 access_token을 꺼내고,
    그 token이 정말 Supabase Auth에서 발급한 token인지 Supabase에 확인시킵니다.
    """

    if credentials is None or credentials.scheme.lower() != "bearer":
        # Swagger Authorize를 누르지 않았거나 Authorization 헤더가 빠진 경우입니다.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization 헤더가 필요합니다. 예: Bearer <access_token>",
        )

    supabase = get_supabase()

    try:
        # credentials.credentials에는 "Bearer "를 제외한 실제 access_token 값이 들어 있습니다.
        # Supabase Auth에 token을 보내면, 해당 token이 가리키는 사용자 정보를 돌려줍니다.
        response = supabase.auth.get_user(credentials.credentials)
    except Exception as error:
        # token이 만료되었거나, 잘못 복사되었거나, 다른 프로젝트의 token이면 실패할 수 있습니다.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"token 확인 실패: {error}",
        ) from error

    if response.user is None:
        # token 검증은 통과하지 못했지만 예외 형태로 오지 않은 경우를 한 번 더 방어합니다.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token에서 사용자를 확인할 수 없습니다.",
        )

    # 이 id는 나중에 사용자별 데이터 접근을 구현할 때 기준이 됩니다.
    return UserInfo(id=response.user.id, email=response.user.email)


@app.get("/me", response_model=UserInfo)
def read_me(current_user: UserInfo = Depends(get_current_user)) -> UserInfo:
    """현재 access token이 가리키는 사용자를 반환합니다.

    이 endpoint는 보호 API의 가장 작은 예제입니다.
    Authorization 헤더가 없거나 token이 틀리면 get_current_user에서 401 오류가 발생하고,
    token이 올바르면 현재 사용자 id/email을 반환합니다.
    """

    return current_user
