r"""backend 전체에서 함께 사용하는 환경 설정 파일입니다.

이 파일은 `.env`에 적어 둔 Supabase, Upstash Redis, CORS 값을 읽어서
다른 Python 파일에서 쉽게 사용할 수 있도록 변수로 정리합니다.

중요:
    실제 비밀키는 코드에 직접 쓰지 않습니다.
    `C:\aidev\04_supabase-ai-mini-project\.env` 또는
    이 backend 폴더의 `.env`에만 저장합니다.
"""

from pathlib import Path
import os

from dotenv import load_dotenv


# BACKEND_ROOT:
#   C:\aidev\04_supabase-ai-mini-project\01_realtime-log-dashboard-practice\backend
# COURSE_ROOT:
#   C:\aidev\04_supabase-ai-mini-project
#
# 이 예제는 과정 루트의 `.env`와 backend 폴더의 `.env`를 모두 읽습니다.
# 수업에서는 보통 과정 루트의 `.env` 하나만 만들어도 됩니다.
BACKEND_ROOT = Path(__file__).resolve().parents[2]
COURSE_ROOT = Path(__file__).resolve().parents[4]

# 먼저 과정 루트의 `.env`를 읽고, 그 다음 backend 폴더의 `.env`를 읽습니다.
# 같은 이름의 값이 있으면 나중에 읽은 값이 우선 적용될 수 있습니다.
load_dotenv(COURSE_ROOT / ".env")
load_dotenv(BACKEND_ROOT / ".env")

# FastAPI 문서 화면의 제목으로 표시됩니다.
APP_NAME = "04 Mini Project Realtime Log Backend"

# Supabase에 로그를 저장할 때 사용하는 값입니다.
# 이 예제는 서버 코드에서 DB에 직접 저장하므로 service role key를 사용합니다.
# service role key는 강한 권한을 가지므로 frontend 코드에 절대 넣으면 안 됩니다.
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip().rstrip("/")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()

# Upstash Redis는 실시간 이벤트 전달에 사용합니다.
# 값이 없으면 수업 안정성을 위해 memory fallback으로 동작합니다.
REDIS_URL = os.getenv("REDIS_URL", "").strip()

raw_origins = os.getenv(
    "CORS_ALLOW_ORIGINS",
    "http://localhost:8501,http://127.0.0.1:8501",
)
# Streamlit frontend가 8501 포트에서 실행되고 FastAPI backend가 8000 포트에서 실행되면
# 브라우저 기준으로 서로 다른 origin입니다. 그래서 CORS 허용 목록이 필요합니다.
CORS_ALLOW_ORIGINS = [item.strip() for item in raw_origins.split(",") if item.strip()]

# Upstash Redis pub/sub에서 사용할 채널 이름입니다.
REDIS_CHANNEL = "mini-project:service-logs"


def is_real_value(value: str) -> bool:
    """환경변수가 비어 있지 않고 `.env.example`의 예시 값도 아닌지 확인합니다.

    예를 들어 `https://your-project-id.supabase.co`나
    `your-supabase-service-role-key`는 안내용 값이므로 실제 설정으로 보지 않습니다.
    """

    return bool(value) and not value.startswith(("your-", "https://your-"))


def is_supabase_configured() -> bool:
    """Supabase 접속에 필요한 URL과 service role key가 모두 실제 값인지 확인합니다."""

    return is_real_value(SUPABASE_URL) and is_real_value(SUPABASE_SERVICE_ROLE_KEY)


def is_redis_configured() -> bool:
    """Upstash Redis URL이 실제 값으로 설정되었는지 확인합니다.

    Upstash Redis URL을 비워 두면 수업용 memory fallback으로 SSE 흐름을 확인합니다.
    """

    return is_real_value(REDIS_URL)
