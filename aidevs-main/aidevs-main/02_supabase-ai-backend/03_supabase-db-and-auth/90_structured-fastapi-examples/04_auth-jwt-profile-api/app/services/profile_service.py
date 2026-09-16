"""RLS가 적용된 `ex90_profiles`를 REST API로 호출합니다."""

from __future__ import annotations

import os

import httpx
from fastapi import HTTPException

import app.core.config  # .env 파일을 읽습니다.
from app.schemas.profile_schema import ProfilePublic, ProfileUpdate


TABLE_NAME = "ex90_profiles"


def auth_headers(access_token: str | None) -> dict[str, str]:
    """Supabase REST API에 보낼 사용자 인증 헤더를 만듭니다.

    apikey에는 anon key를 넣고, Authorization에는 로그인한 사용자의 access token을 넣습니다.
    이 조합이어야 Supabase RLS가 "현재 사용자"를 판단할 수 있습니다.
    """

    anon_key = os.getenv("SUPABASE_ANON_KEY")
    if not anon_key:
        raise HTTPException(status_code=500, detail="SUPABASE_ANON_KEY가 없습니다. .env 파일을 확인하세요.")

    if not access_token:
        raise HTTPException(status_code=401, detail="Bearer token이 없습니다.")

    return {
        "apikey": anon_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def table_url() -> str:
    """ex90_profiles 테이블의 Supabase REST API URL을 만듭니다."""

    supabase_url = os.getenv("SUPABASE_URL")
    if not supabase_url:
        raise HTTPException(status_code=500, detail="SUPABASE_URL이 없습니다. .env 파일을 확인하세요.")
    return f"{supabase_url.rstrip('/')}/rest/v1/{TABLE_NAME}"


def to_profile(row: dict) -> ProfilePublic:
    """Supabase row를 ProfilePublic 응답 모델로 변환합니다."""

    return ProfilePublic(
        id=str(row["id"]),
        display_name=row["display_name"],
        created_at=row.get("created_at"),
        updated_at=row.get("updated_at"),
    )


def get_profile(access_token: str | None) -> ProfilePublic:
    """현재 token으로 접근 가능한 프로필 1개를 조회합니다."""

    try:
        # select=*로 요청하지만 RLS 때문에 현재 사용자 row만 응답됩니다.
        response = httpx.get(
            table_url(),
            headers=auth_headers(access_token),
            params={"select": "*"},
            timeout=10,
        )
        response.raise_for_status()
    except httpx.HTTPError as error:
        raise HTTPException(status_code=502, detail=f"profile 조회 실패: {error}") from error

    data = response.json()
    if not data:
        raise HTTPException(status_code=404, detail="profile이 없습니다. PUT /profile을 먼저 실행하세요.")
    return to_profile(data[0])


def upsert_profile(
    user_id: str,
    access_token: str | None,
    request: ProfileUpdate,
) -> ProfilePublic:
    """현재 사용자 id로 프로필을 생성하거나 업데이트합니다."""

    # id는 auth.users.id와 같은 값입니다.
    # RLS 정책은 이 id가 auth.uid()와 같은지 검사합니다.
    payload = {"id": user_id, "display_name": request.display_name}
    try:
        # on_conflict=id는 id가 이미 있으면 update처럼 동작하게 해 줍니다.
        # 그래서 학생은 POST/PUT 차이보다 "내 프로필 저장" 흐름에 집중할 수 있습니다.
        response = httpx.post(
            f"{table_url()}?on_conflict=id",
            headers=auth_headers(access_token),
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
    except httpx.HTTPError as error:
        raise HTTPException(status_code=502, detail=f"profile 저장 실패: {error}") from error

    return to_profile(response.json()[0])
