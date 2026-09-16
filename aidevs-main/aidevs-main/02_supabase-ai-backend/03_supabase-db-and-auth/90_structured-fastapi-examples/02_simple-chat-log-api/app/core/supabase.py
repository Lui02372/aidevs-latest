"""Supabase client를 만듭니다."""

import os

from fastapi import HTTPException

import app.core.config  # .env 파일을 읽습니다.


def get_supabase_client():
    """service role key를 사용하는 Supabase client를 만듭니다."""

    from supabase import create_client

    supabase_url = os.getenv("SUPABASE_URL")
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url:
        raise HTTPException(500, "SUPABASE_URL이 없습니다. .env 파일을 확인하세요.")

    if not service_role_key:
        raise HTTPException(
            500,
            "SUPABASE_SERVICE_ROLE_KEY가 없습니다. .env 파일을 확인하세요.",
        )

    return create_client(supabase_url, service_role_key)
