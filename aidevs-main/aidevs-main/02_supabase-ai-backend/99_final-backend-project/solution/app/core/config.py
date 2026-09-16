"""환경 변수(.env)를 읽어 오는 설정 파일입니다.

이 solution은 두 가지 방식으로 동작할 수 있습니다.

1. Supabase 환경변수가 있으면 Supabase 테이블에 데이터를 저장합니다.
2. Supabase 환경변수가 없으면 메모리 리스트에 임시 저장합니다.

초보자에게 중요한 점:
    `.env` 파일에는 API Key, Supabase Key 같은 민감 정보가 들어갑니다.
    따라서 `.env`는 GitHub에 올리지 않고, 예시는 `.env.example`에만 작성합니다.
"""

from pathlib import Path

from dotenv import load_dotenv


# 현재 파일 위치:
#   solution/app/core/config.py
#
# parents[4]는 `C:\aidev\02_supabase-ai-backend` 폴더를 가리킵니다.
# 이 과정에서는 공통 `.env`를 02_supabase-ai-backend 바로 아래에 두는 방식을 기본으로 사용합니다.
COURSE_ROOT = Path(__file__).resolve().parents[4]

# `.env` 파일이 있으면 환경변수로 읽어 옵니다.
# 파일이 없어도 오류를 내지 않습니다. 대신 storage_service.py가 메모리 모드로 동작합니다.
load_dotenv(COURSE_ROOT / ".env")
