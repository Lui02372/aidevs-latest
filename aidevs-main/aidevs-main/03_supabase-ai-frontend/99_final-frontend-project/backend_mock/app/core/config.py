import os


# 앱 이름은 Swagger UI 제목과 서버 식별에 사용됩니다.
APP_NAME = "99 Final Frontend Project Backend"

# mock token 앞에 붙일 문자열입니다. 실제 JWT가 아니라 수업용 문자열입니다.
MOCK_TOKEN_PREFIX = os.getenv("MOCK_TOKEN_PREFIX", "mock")

# 실제 만료 처리는 하지 않지만, token 만료 개념을 설명할 때 사용할 수 있는 설정입니다.
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# true로 바꾸면 mock AI 응답 전에 짧게 기다려 로딩 UI를 테스트할 수 있습니다.
ENABLE_FAKE_DELAY = os.getenv("ENABLE_FAKE_DELAY", "false").lower() == "true"

# Streamlit 프론트엔드가 다른 포트에서 API를 호출할 수 있도록 허용할 origin 목록입니다.
CORS_ALLOW_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")
