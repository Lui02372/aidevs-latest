"""Supabase/Auth/Redis 오류를 분석하기 위한 의도적 문제 예제입니다.

실행:
    python -m uvicorn broken_external_service_api:app --reload --host 127.0.0.1 --port 8093

실제 외부 서비스 값이 없으면 일부 endpoint는 500/502를 반환합니다.
이 파일의 목적은 오류를 없애는 것이 아니라, 오류를 분류해서 좋은 질문을 만드는 것입니다.
"""

from pathlib import Path
import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, status


ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_PATH)

app = FastAPI(title="Lab 03 External Service Debugging")


def read_env(name: str) -> str:
    """필수 환경변수를 읽고 없으면 오류를 발생시킵니다."""

    value = os.getenv(name, "").strip()
    if not value or value.startswith(("your-", "https://your-")):
        raise HTTPException(status_code=500, detail=f"{name} 환경변수를 확인하세요.")
    return value


@app.get("/health")
def health() -> dict[str, str]:
    """서버 실행 여부를 확인합니다."""

    return {"status": "ok"}


@app.get("/debug/supabase-table")
def debug_supabase_table() -> dict:
    """일부러 잘못된 테이블명을 조회해 Supabase 오류를 재현합니다."""

    supabase_url = read_env("SUPABASE_URL")
    service_role_key = read_env("SUPABASE_SERVICE_ROLE_KEY")

    # 의도된 문제: schema.sql에는 lab03_debug_logs가 있지만 여기서는 다른 테이블명을 사용합니다.
    wrong_table_url = f"{supabase_url}/rest/v1/lab03_missing_logs"
    headers = {
        "apikey": service_role_key,
        "Authorization": f"Bearer {service_role_key}",
    }
    response = httpx.get(wrong_table_url, headers=headers, params={"select": "*"}, timeout=10)
    response.raise_for_status()
    return {"data": response.json()}


@app.get("/debug/me")
def debug_me(authorization: str | None = Header(default=None)) -> dict[str, str]:
    """Bearer token 누락 오류를 확인합니다."""

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization: Bearer <access_token> 헤더가 필요합니다.",
        )
    return {"token_preview": authorization[:20] + "..."}


@app.get("/debug/redis")
def debug_redis() -> dict:
    """Redis REST API 설정 오류와 TTL 확인 흐름을 재현합니다."""

    redis_url = read_env("UPSTASH_REDIS_REST_URL").rstrip("/")
    redis_token = read_env("UPSTASH_REDIS_REST_TOKEN")
    headers = {"Authorization": f"Bearer {redis_token}"}

    key = "lab03:debug"
    set_response = httpx.get(f"{redis_url}/set/{key}/hello/ex/30", headers=headers, timeout=10)
    set_response.raise_for_status()
    ttl_response = httpx.get(f"{redis_url}/ttl/{key}", headers=headers, timeout=10)
    ttl_response.raise_for_status()

    return {"set": set_response.json(), "ttl": ttl_response.json()}
