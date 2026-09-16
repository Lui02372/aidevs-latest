r"""print 확인과 assert 확인의 차이를 보여 주는 예제입니다.

실행 위치:
    C:\aidev\01_python-git-foundation

실행 명령:
    python .\02_python-advanced\03_testing-basic\02_print_vs_assert.py
"""


def normalize_question(question: str) -> str:
    return question.strip()


def main() -> None:
    question = "  FastAPI란?  "
    result = normalize_question(question)

    print("print 확인:", result)
    print("print는 값을 보여 주지만, 맞는지 틀린지는 사람이 봐야 합니다.")

    assert result == "FastAPI란?"
    print("assert 확인 통과: 앞뒤 공백이 제거되었습니다.")


main()
