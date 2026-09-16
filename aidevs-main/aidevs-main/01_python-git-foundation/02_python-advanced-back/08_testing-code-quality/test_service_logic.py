"""pytest로 서비스 함수를 검증하는 예제입니다.

실행:
    cd C:\aidev\01_python-git-foundation
    python -m pytest .\02_python-advanced\08_testing-code-quality

pytest는 파일 이름이 test_로 시작하는 파일을 찾고,
그 안에서 함수 이름이 test_로 시작하는 함수를 자동으로 실행합니다.

왜 print가 아니라 pytest를 사용할까요?
    print는 사람이 눈으로 결과를 확인해야 합니다.
    pytest는 예상 결과와 실제 결과를 자동으로 비교합니다.
    테스트가 실패하면 어느 함수가 어떤 이유로 실패했는지 알려 줍니다.
"""

import pytest

from service_logic import build_chat_response, normalize_question, validate_question


def test_normalize_question_removes_spaces() -> None:
    """질문 앞뒤 공백이 제거되는지 확인합니다.

    assert 왼쪽은 실제 함수 실행 결과입니다.
    assert 오른쪽은 우리가 기대하는 정답입니다.
    두 값이 다르면 이 테스트는 실패합니다.
    """

    assert normalize_question("  Supabase란?  ") == "Supabase란?"


def test_normalize_question_keeps_inner_spaces() -> None:
    """문장 중간의 공백은 유지되는지 확인합니다."""

    assert normalize_question("  FastAPI 기본 구조  ") == "FastAPI 기본 구조"


def test_validate_question_rejects_empty_text() -> None:
    """빈 질문이면 ValueError가 발생해야 합니다.

    오류가 발생해야 정상인 경우에는 pytest.raises를 사용합니다.
    """

    with pytest.raises(ValueError):
        validate_question("   ")


def test_validate_question_accepts_normal_text() -> None:
    """정상 질문은 오류 없이 지나가야 합니다."""

    validate_question("테스트는 왜 필요한가요?")


def test_build_chat_response_has_required_keys() -> None:
    """응답 dict에 question과 answer key가 있는지 확인합니다.

    이후 FastAPI 응답이나 Supabase 저장 데이터도 dict/JSON 구조를 사용합니다.
    그래서 필수 key가 빠지지 않았는지 테스트하는 습관이 중요합니다.
    """

    response = build_chat_response("FastAPI란?")

    assert response["question"] == "FastAPI란?"
    assert "answer" in response
    assert response["answer"] != ""


def test_build_chat_response_normalizes_question() -> None:
    """응답을 만들 때도 질문 앞뒤 공백이 정리되는지 확인합니다."""

    response = build_chat_response("  pytest란?  ")

    assert response["question"] == "pytest란?"


def test_build_chat_response_rejects_empty_question() -> None:
    """응답 생성 함수도 빈 질문을 거부해야 합니다."""

    with pytest.raises(ValueError):
        build_chat_response("")
