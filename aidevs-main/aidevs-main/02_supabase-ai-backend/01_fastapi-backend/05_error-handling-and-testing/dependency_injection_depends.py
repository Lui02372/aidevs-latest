"""FastAPI Depends 의존성 주입 예제.

실행:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\05_error-handling-and-testing
    uvicorn dependency_injection_depends:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn dependency_injection_depends:app --reload

확인:
    http://127.0.0.1:8000/me?token=student-token
    http://127.0.0.1:8000/me?token=wrong-token
    http://127.0.0.1:8000/admin?token=student-token

의존성 주입(Dependency Injection)은 여러 API에서 반복되는 공통 작업을
별도의 함수로 분리하고, FastAPI가 필요한 순간에 자동으로 실행하게 하는 방식입니다.

초보자는 `Depends`를 처음 보면 어렵게 느낄 수 있습니다.
하지만 핵심은 단순합니다.

1. 공통으로 필요한 작업을 함수로 만든다.
2. 엔드포인트 함수의 매개변수에 `Depends(함수명)`을 적는다.
3. FastAPI가 요청을 처리하기 전에 그 함수를 먼저 실행한다.
"""

from fastapi import Depends, FastAPI, HTTPException, Query


# FastAPI 앱 객체입니다.
# `uvicorn dependency_injection_depends:app --reload`에서 마지막 `app`이 이 변수입니다.
app = FastAPI(title="Dependency Injection Practice")


# get_current_user는 인증 확인을 담당하는 공통 함수입니다.
# 여러 API에서 토큰 확인 코드가 반복되지 않도록 Depends로 재사용합니다.
def get_current_user(token: str = Query(..., description="수업용 인증 토큰")):
    """토큰을 확인하고 현재 사용자 정보를 반환합니다.

    실제 서비스에서는 Supabase Auth, JWT, 세션 저장소 등을 확인합니다.
    여기서는 초보자 실습을 위해 간단한 문자열 토큰만 사용합니다.
    """

    # Query(...)는 URL query string에 token 값이 반드시 있어야 한다는 뜻입니다.
    # 예: /me?token=student-token
    # token 값이 아예 없으면 FastAPI가 자동으로 422 오류를 반환합니다.
    if token != "student-token":
        # 401은 "인증되지 않았다"는 의미입니다.
        raise HTTPException(status_code=401, detail="Invalid token")

    # 인증에 성공하면 이후 API에서 사용할 사용자 정보를 반환합니다.
    return {
        "id": "user-001",
        "name": "Student",
        "role": "student",
}


# require_admin은 get_current_user 결과를 한 번 더 검사합니다.
# Depends 안에서 또 다른 Depends를 사용할 수 있습니다.
def require_admin(current_user: dict = Depends(get_current_user)):
    """관리자 권한이 있는지 확인하는 의존성 함수입니다.

    이 함수는 먼저 `get_current_user`를 실행한 뒤,
    반환된 사용자 정보에서 role 값을 확인합니다.
    """

    if current_user["role"] != "admin":
        # 403은 "인증은 되었지만 권한이 없다"는 의미입니다.
        raise HTTPException(status_code=403, detail="Admin permission required")

    return current_user


# read_me 함수가 실행되기 전에 FastAPI가 get_current_user를 먼저 실행합니다.
# get_current_user가 반환한 dict가 current_user 인자에 들어옵니다.
@app.get("/me")
def read_me(current_user: dict = Depends(get_current_user)):
    """현재 로그인한 사용자 정보를 반환합니다.

    엔드포인트 안에서 토큰 검증 코드를 다시 쓰지 않습니다.
    공통 인증 로직은 `get_current_user`가 담당합니다.
    """

    return {
        "message": "authenticated",
        "user": current_user,
}


# /admin은 require_admin 의존성을 통과해야 실행됩니다.
# 현재 get_current_user는 role이 student인 사용자만 반환하므로 이 예제는 403을 확인하기 좋습니다.
@app.get("/admin")
def read_admin_page(admin_user: dict = Depends(require_admin)):
    """관리자만 접근할 수 있는 API 예시입니다."""

    return {
        "message": "admin page",
        "user": admin_user,
    }
