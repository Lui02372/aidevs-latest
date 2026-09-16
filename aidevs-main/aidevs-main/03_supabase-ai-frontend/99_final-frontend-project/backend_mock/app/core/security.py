from uuid import uuid4

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import MOCK_TOKEN_PREFIX


bearer_scheme = HTTPBearer(
    auto_error=False,
    description="로그인 후 받은 access_token만 입력합니다. Swagger가 Bearer prefix를 자동으로 붙입니다.",
)


def create_access_token() -> str:
    """수업용 mock access token을 만듭니다.

    실제 서비스에서는 Supabase Auth 또는 인증 서버가 JWT를 발급합니다.
    이 mock backend는 프론트엔드 실습을 위해 UUID 기반 문자열을 token처럼 사용합니다.
    """

    return f"{MOCK_TOKEN_PREFIX}_{uuid4().hex}"


def get_bearer_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    """Authorization: Bearer <token> header에서 token 값만 꺼냅니다.

    Streamlit 프론트엔드는 보호된 API를 호출할 때 아래 형태의 header를 보냅니다.

        Authorization: Bearer 로그인_후_받은_access_token

    HTTPBearer를 사용하면 Swagger UI 오른쪽 위 Authorize 버튼에서도 같은 방식으로
    token을 입력하고 보호된 API를 테스트할 수 있습니다.
    """

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header가 없습니다. Bearer token을 보내야 합니다.",
        )

    if credentials.scheme.lower() != "bearer" or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header는 Bearer token 형식이어야 합니다.",
        )

    return credentials.credentials
