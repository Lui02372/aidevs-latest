"""URL과 HTTP 요청/응답만 담당하는 Notes API 라우터입니다."""

from fastapi import APIRouter, HTTPException, status

from app.core.config import SUPABASE_SERVICE_ROLE_KEY, SUPABASE_URL
from app.schemas.note_schema import NoteCreate, NotePublic, NoteUpdate
from app.services import notes_service


router = APIRouter(tags=["notes"])


@router.get("/health")
def health() -> dict[str, str | bool]:
    """서버와 Supabase 설정 상태를 확인합니다."""
    return {
        "status": "ok",
        "supabase_configured": bool(SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY),
    }


@router.get("/notes")
def list_notes() -> dict[str, int | list[NotePublic]]:
    notes = notes_service.list_notes()
    return {"count": len(notes), "data": notes}


@router.post("/notes", response_model=NotePublic, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate) -> NotePublic:
    return notes_service.create_note(note)


@router.get("/notes/{note_id}", response_model=NotePublic)
def get_note(note_id: str) -> NotePublic:
    note = notes_service.get_note(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/notes/{note_id}", response_model=NotePublic)
def update_note(note_id: str, note: NoteUpdate) -> NotePublic:
    updated_note = notes_service.update_note(note_id, note)
    if updated_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note


@router.delete("/notes/{note_id}")
def delete_note(note_id: str) -> dict[str, str]:
    deleted = notes_service.delete_note(note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "deleted"}
