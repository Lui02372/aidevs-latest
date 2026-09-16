"""assert 실패가 어떤 식으로 보이는지 안전하게 확인하는 예제입니다.

실행:
    cd C:\aidev\01_python-git-foundation
    python .\02_python-advanced\08_testing-code-quality\03_assert_failure_message.py

이 파일은 일부러 실패하는 조건을 try/except로 감싸서 보여 줍니다.
실제 테스트 파일에서는 실패를 숨기지 않고 pytest가 실패를 표시하게 둡니다.
"""


def normalize_question(question: str) -> str:
    """질문 앞뒤 공백을 제거합니다."""

    return question.strip()


expected = "FastAPI란?"
actual = normalize_question("  FastAPI란?  ")

# 성공하는 assert입니다.
assert actual == expected

wrong_expected = "Supabase란?"

try:
    # 일부러 틀린 예상값을 넣어 assert 실패를 만들어 봅니다.
    assert actual == wrong_expected
except AssertionError:
    print("assert 실패를 확인했습니다.")
    print("예상값:", wrong_expected)
    print("실제값:", actual)
    print("이런 차이를 자동으로 잡아내기 위해 assert와 pytest를 사용합니다.")
