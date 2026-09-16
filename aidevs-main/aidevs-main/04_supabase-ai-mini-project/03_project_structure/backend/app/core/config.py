"""최종 프로젝트 starter backend의 공통 환경 설정 파일입니다.

학생들은 이 파일을 기준으로 Supabase, Upstash Redis, CORS 설정이
backend 코드 안에서 어떻게 사용되는지 확인할 수 있습니다.
"""

from pathlib import Path
import os

from dotenv import load_dotenv


# BACKEND_ROOT는 현재 starter backend 폴더입니다.
# COURSE_ROOT는 04_supabase-ai-mini-project 과정 루트입니다.
BACKEND_ROOT = Path(__file__).resolve().parents[2]
COURSE_ROOT = Path(__file__).resolve().parents[4]

# 과정 루트 `.env`와 backend 폴더 `.env`를 함께 읽습니다.
# 수업에서는 과정 루트 `.env`를 기본 위치로 권장합니다.
load_dotenv(COURSE_ROOT / ".env")
load_dotenv(BACKEND_ROOT / ".env")

APP_NAME = "04 Mini Project Final Starter Backend"

# Supabase 연결 값입니다.
# service role key는 서버 전용 비밀키이므로 Streamlit frontend에 노출하지 않습니다.
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip().rstrip("/")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()

# Upstash Redis는 실시간 로그 스트리밍을 더 안정적으로 전달할 때 사용합니다.
# 값이 없으면 먼저 memory fallback으로 프로젝트 구조를 완성해도 됩니다.
REDIS_URL = os.getenv("REDIS_URL", "").strip()

raw_origins = os.getenv(
    "CORS_ALLOW_ORIGINS",
    "http://localhost:8501,http://127.0.0.1:8501",
)
CORS_ALLOW_ORIGINS = [item.strip() for item in raw_origins.split(",") if item.strip()]

REDIS_CHANNEL = "mini-project:service-logs"


def is_real_value(value: str) -> bool:
    """환경변수가 비어 있지 않고 `.env.example`의 예시 값도 아닌지 확인합니다."""

    return bool(value) and not value.startswith(("your-", "https://your-"))


def is_supabase_configured() -> bool:
    """Supabase URL과 service role key가 모두 실제 값인지 확인합니다."""

    return is_real_value(SUPABASE_URL) and is_real_value(SUPABASE_SERVICE_ROLE_KEY)


def is_redis_configured() -> bool:
    """Upstash Redis URL이 실제 값으로 설정되었는지 확인합니다."""

    return is_real_value(REDIS_URL)
