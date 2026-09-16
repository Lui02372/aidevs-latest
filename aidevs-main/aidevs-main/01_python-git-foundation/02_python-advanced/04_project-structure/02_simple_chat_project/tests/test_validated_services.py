r"""02_simple_chat_project의 검증 포함 서비스 함수 테스트입니다.

실행 위치:
    C:\aidev\01_python-git-foundation

실행 명령:
    python -m pytest .\02_python-advanced\04_project-structure\02_simple_chat_project
"""

import pytest
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

# 여러 예제 프로젝트를 한 번에 테스트할 때 이전에 불러온 app 패키지와 섞이지 않게 합니다.
for module_name in list(sys.modules):
    if module_name == "app" or module_name.startswith("app."):
        del sys.modules[module_name]

from app.services import create_chat_message, normalize_question, validate_question


def test_normalize_question_removes_spaces() -> None:
    assert normalize_question("  FastAPI  ") == "FastAPI"


def test_validate_question_raises_error_when_empty() -> None:
    with pytest.raises(ValueError):
        validate_question("   ")


def test_create_chat_message_returns_object() -> None:
    message = create_chat_message("프로젝트 구조란?")

    assert message.question == "프로젝트 구조란?"
    assert message.model == "practice-model"
    assert "연습 답변" in message.answer
