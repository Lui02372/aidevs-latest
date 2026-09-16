from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


bearer_scheme = HTTPBearer(
    auto_error=False,
    description="Supabase Auth 로그인 후 받은 access_token만 입력합니다. Swagger가 Bearer prefix를 자동으로 붙입니다.",
)


def get_bearer_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    """Authorization: Bearer <token> header에서 token 값만 꺼냅니다.

    backend_service에서는 이 token이 Supabase Auth에서 발급한 access_token입니다.
    이 함수는 header 형식만 확인하고, 실제 사용자가 유효한지는 auth_service에서
    Supabase Auth의 get_user로 검증합니다.
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
