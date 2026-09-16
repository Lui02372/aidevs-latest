"""JSON 저장과 읽기를 담당하는 파일입니다.

지금은 JSON 파일에 저장하지만, 뒤 과정에서는 이 역할이 Supabase 테이블 저장으로 확장됩니다.
"""

import json
from pathlib import Path

from app.models import ChatMessage


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"
DATA_FILE = DATA_DIR / "chat_messages.json"


def load_messages() -> list[dict]:
    """저장된 메시지 목록을 읽습니다.

    파일이 아직 없으면 빈 목록을 반환합니다.
    """

    if not DATA_FILE.exists():
        return []

    text = DATA_FILE.read_text(encoding="utf-8")
    return json.loads(text)


def save_message(message: ChatMessage) -> None:
    """새 메시지 하나를 JSON 파일에 추가 저장합니다."""

    DATA_DIR.mkdir(exist_ok=True)

    messages = load_messages()
    messages.append(message.to_dict())

    DATA_FILE.write_text(
        json.dumps(messages, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
