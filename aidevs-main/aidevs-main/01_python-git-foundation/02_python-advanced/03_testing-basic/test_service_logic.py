r"""service_logic.py 테스트 예제입니다.

실행 위치:
    C:\aidev\01_python-git-foundation

실행 명령:
    python -m pytest .\02_python-advanced\03_testing-basic
"""

import pytest

from service_logic import build_response, normalize_question, validate_question


def test_normalize_question_removes_spaces() -> None:
    result = normalize_question("  FastAPI란?  ")

    assert result == "FastAPI란?"


def test_validate_question_raises_error_when_empty() -> None:
    with pytest.raises(ValueError):
        validate_question("   ")


def test_build_response_has_required_keys() -> None:
    response = build_response("Supabase란?")

    assert response["question"] == "Supabase란?"
    assert "answer" in response
    assert response["model"] == "practice-model"
