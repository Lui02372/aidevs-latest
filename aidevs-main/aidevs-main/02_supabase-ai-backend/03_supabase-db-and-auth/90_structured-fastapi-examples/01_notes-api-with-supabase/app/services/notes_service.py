"""Supabase의 ex90_notes 테이블을 읽고 쓰는 코드입니다."""

from __future__ import annotations

from app.core.config import supabase
from app.schemas.note_schema import (
    NoteCreate, 
    NotePublic, 
    NoteUpdate
)


TABLE_NAME = "ex90_notes"


def list_notes() -> list[NotePublic]:
    result = (
        supabase
        .table(TABLE_NAME)
        .select("*")
        .order("created_at", desc=True)
        .limit(20)
        .execute()
    )
    # [{},{},{}]
    return [NotePublic.model_validate(row) for row in result.data]


def create_note(note: NoteCreate) -> NotePublic:
    result = (
        supabase
        .table(TABLE_NAME)
        .insert({"title": note.title, "content": note.content})
        .execute()
    )
    return NotePublic.model_validate(result.data[0])


def get_note(note_id: str) -> NotePublic | None:
    result = (
        supabase
        .table(TABLE_NAME)
        .select("*")
        .eq("id", note_id)
        .limit(1)
        .execute()
    )
    if not result.data:
        return None
    return NotePublic.model_validate(result.data[0])


def update_note(note_id: str, note: NoteUpdate) -> NotePublic | None:
    result = (
        supabase
        .table(TABLE_NAME)
        .update({"title": note.title, "content": note.content})
        .eq("id", note_id)
        .execute()
    )
    if not result.data:
        return None
    return NotePublic.model_validate(result.data[0])


def delete_note(note_id: str) -> bool:
    result = (
        supabase
        .table(TABLE_NAME)
        .delete()
        .eq("id", note_id)
        .execute()
    )
    return bool(result.data)
