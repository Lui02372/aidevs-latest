from pathlib import Path
import os

from dotenv import load_dotenv


# backend_service 폴더 위치를 기준으로 .env 파일을 찾습니다.
BACKEND_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(BACKEND_ROOT / ".env")

# Swagger 제목과 서버 이름에 사용됩니다.
APP_NAME = os.getenv("APP_NAME", "99 Final Frontend Service Backend")

# Streamlit은 보통 8501 포트에서 실행되고 FastAPI는 8000 포트에서 실행됩니다.
# 포트가 다르면 브라우저 기준 origin이 다르므로 CORS 허용 목록이 필요합니다.
raw_origins = os.getenv(
    "CORS_ALLOW_ORIGINS",
    "http://localhost:8501,http://127.0.0.1:8501",
)
CORS_ALLOW_ORIGINS = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

# Supabase Auth와 DB 접근에 필요한 값입니다.
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

# Gemini API 호출에 필요한 값입니다.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

# Upstash Redis는 같은 질문에 대한 AI 응답을 캐시하는 선택 확장입니다.
UPSTASH_REDIS_REST_URL = os.getenv("UPSTASH_REDIS_REST_URL", "")
UPSTASH_REDIS_REST_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN", "")
