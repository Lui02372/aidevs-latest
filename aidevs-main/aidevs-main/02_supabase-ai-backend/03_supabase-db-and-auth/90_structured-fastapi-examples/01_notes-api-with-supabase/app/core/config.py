""".env 파일을 읽어 Supabase 설정을 준비합니다."""

import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

# .env가 없는 상태에서도 /health와 테스트 앱은 시작할 수 있게 둡니다.
# 실제 /notes 요청 전에는 .env를 설정해야 합니다.
supabase = (
    create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY
    else None
)
