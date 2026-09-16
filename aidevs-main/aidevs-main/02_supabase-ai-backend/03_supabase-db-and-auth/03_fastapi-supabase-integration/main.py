from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from supabase import Client, create_client


# 이 파일은 다음 위치에 있습니다.
# 02_supabase-ai-backend/03_supabase-db-and-auth/03_fastapi-supabase-integration/main.py
# parents[2]는 02_supabase-ai-backend 폴더입니다.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"


def read_required_env(name: str) -> str:
    """필수 환경 변수를 읽고, 비어 있거나 예시 값이면 HTTP 500 오류를 냅니다.

    FastAPI 예제에서는 환경변수 오류도 API 응답으로 보여 주는 편이 이해하기 쉽습니다.
    그래서 RuntimeError 대신 HTTPException을 사용합니다.
    """

    value = os.getenv(name, "").strip()

    if not value:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{name} 환경변수를 C:\\aidev\\02_supabase-ai-backend\\.env에 설정하세요.",
        )

    if value.startswith(("your-", "https://your-")):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{name}에 실제 값을 입력하세요. Supabase Dashboard에서 복사한 값을 사용해야 합니다.",
        )

    return value


def is_configured_env(name: str) -> bool:
    """health check에서 환경변수가 실제 값으로 설정되었는지 True/False로 확인합니다."""

    value = os.getenv(name, "").strip()
    return bool(value) and not value.startswith(("your-", "https://your-"))


# FastAPI가 실행될 때 .env 값을 미리 읽습니다.
# 실행 위치가 03_fastapi-supabase-integration 폴더여도 최상위 .env를 안정적으로 찾습니다.
load_dotenv(ENV_PATH)

app = FastAPI(title="FastAPI Supabase Integration Practice")


class NoteCreate(BaseModel):
    """새 학습 메모를 만들 때 사용하는 요청 모델입니다."""

    title: str = Field(..., min_length=1, max_length=100, description="학습 메모 제목")
    content: str = Field(..., min_length=1, max_length=1000, description="학습 메모 내용")


class NoteUpdate(BaseModel):
    """기존 학습 메모를 수정할 때 사용하는 요청 모델입니다.

    title과 content는 둘 다 선택 값입니다.
    단, 둘 다 비어 있으면 실제로 수정할 내용이 없으므로 400 오류를 반환합니다.
    """

    title: str | None = Field(default=None, min_length=1, max_length=100, description="수정할 제목")
    content: str | None = Field(default=None, min_length=1, max_length=1000, description="수정할 내용")


class NoteResponse(BaseModel):
    """프론트엔드가 받기 좋은 학습 메모 응답 구조입니다."""

    id: str
    title: str
    content: str
    created_at: str


class NoteItemResponse(BaseModel):
    """메모 1개를 반환할 때 사용하는 응답 구조입니다."""

    item: NoteResponse


class NoteListResponse(BaseModel):
    """메모 목록을 반환할 때 사용하는 응답 구조입니다."""

    items: list[NoteResponse]


def get_supabase() -> Client:
    """FastAPI endpoint에서 사용할 Supabase client를 생성합니다.

    이 예제는 백엔드 서버에서 실행되므로 service role key를 사용합니다.
    service role key는 강한 권한을 가진 key이므로 화면 코드나 GitHub에 노출하면 안 됩니다.
    """

    url = read_required_env("SUPABASE_URL")
    service_role_key = read_required_env("SUPABASE_SERVICE_ROLE_KEY")
    return create_client(url, service_role_key)


@app.get("/health")
def health() -> dict[str, bool | str]:
    """서버와 Supabase 환경 변수 설정 상태를 확인합니다."""

    return {
        "status": "ok",
        "database": "supabase",
        "supabase_url_configured": is_configured_env("SUPABASE_URL"),
        "service_role_key_configured": is_configured_env("SUPABASE_SERVICE_ROLE_KEY"),
    }


@app.get("/notes", response_model=NoteListResponse)
def list_notes() -> dict[str, list[dict]]:
    """최근 학습 메모 목록을 조회합니다."""

    supabase = get_supabase()

    # select("*")는 모든 컬럼을 조회한다는 뜻입니다.
    # created_at 기준 내림차순으로 정렬해서 최근 메모가 먼저 오게 합니다.
    result = (
        supabase.table("learning_notes_main")
        .select("*")
        .order("created_at", desc=True)
        .limit(20)
        .execute()
    )

    return {"items": result.data}


@app.get("/notes/{note_id}", response_model=NoteItemResponse)
def get_note(note_id: str) -> dict[str, dict]:
    """id로 학습 메모 1개를 조회합니다."""

    supabase = get_supabase()

    # eq("id", note_id)는 id가 note_id와 같은 행만 가져오라는 조건입니다.
    result = (
        supabase.table("learning_notes_main")
        .select("*")
        .eq("id", note_id)
        .limit(1)
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found.")

    return {"item": result.data[0]}


@app.post("/notes", response_model=NoteItemResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate) -> dict[str, dict]:
    """학습 메모를 새로 저장합니다."""

    supabase = get_supabase()

    # note.model_dump()는 Pydantic 모델을 딕셔너리로 바꿉니다.
    # Supabase insert에는 딕셔너리 형태의 데이터가 필요합니다.
    result = supabase.table("learning_notes_main").insert(note.model_dump()).execute()

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create note.",
        )

    return {"item": result.data[0]}


@app.put("/notes/{note_id}", response_model=NoteItemResponse)
def update_note(note_id: str, note: NoteUpdate) -> dict[str, dict]:
    """학습 메모를 수정합니다."""

    # exclude_none=True를 사용하면 None인 필드는 수정 데이터에서 제외됩니다.
    update_data = note.model_dump(exclude_none=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update.")

    supabase = get_supabase()

    # update/delete에는 조건이 중요합니다.
    # eq("id", note_id)가 있어야 특정 메모 1개만 수정합니다.
    result = (
        supabase.table("learning_notes_main")
        .update(update_data)
        .eq("id", note_id)
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found.")

    return {"item": result.data[0]}


@app.delete("/notes/{note_id}")
def delete_note(note_id: str) -> dict[str, str]:
    """학습 메모를 삭제합니다."""

    supabase = get_supabase()

    # 삭제 전에 존재 여부를 먼저 확인합니다.
    # 이렇게 하면 없는 id를 삭제하려고 할 때도 명확하게 404를 반환할 수 있습니다.
    existing = (
        supabase.table("learning_notes_main")
        .select("id")
        .eq("id", note_id)
        .limit(1)
        .execute()
    )
    if not existing.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found.")

    supabase.table("learning_notes_main").delete().eq("id", note_id).execute()
    return {"deleted_id": note_id}
