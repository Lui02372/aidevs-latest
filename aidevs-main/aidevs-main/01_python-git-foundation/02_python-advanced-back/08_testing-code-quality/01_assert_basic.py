"""assert로 함수 결과를 직접 확인하는 기본 예제입니다.

실행:
    cd C:\aidev\01_python-git-foundation
    python .\02_python-advanced\08_testing-code-quality\01_assert_basic.py

왜 assert를 사용할까요?
    print는 값을 화면에 보여 주기만 합니다.
    값이 맞는지 틀린지는 사람이 직접 눈으로 확인해야 합니다.

    assert는 "이 조건은 반드시 True여야 한다"라고 코드에 적는 방법입니다.
    조건이 틀리면 프로그램이 바로 실패하므로, 실수를 빨리 찾을 수 있습니다.
"""


def normalize_question(question: str) -> str:
    """질문 앞뒤 공백을 제거합니다."""

    return question.strip()


# 아래 코드는 "normalize_question 함수의 결과가 반드시 FastAPI란? 이어야 한다"는 뜻입니다.
# 조건이 True이면 아무 일 없이 다음 줄로 넘어갑니다.
assert normalize_question("  FastAPI란?  ") == "FastAPI란?"

# 빈 문자열에 strip을 적용하면 빈 문자열이 됩니다.
# 이 조건도 True여야 정상입니다.
assert normalize_question("   ") == ""

print("assert 검사 통과")
