r"""raise로 직접 오류를 만드는 예제입니다.

실행 위치:
    C:\aidev\01_python-git-foundation

실행 명령:
    python .\02_python-advanced\02_exception-debugging\02_raise_validation.py

이 예제의 목표:
    잘못된 입력을 발견했을 때 함수 안에서 ValueError를 발생시킵니다.
    뒤 과정에서는 FastAPI가 이런 검증 흐름을 HTTP 오류로 바꾸어 응답합니다.
"""


def validate_question(question: str) -> str:
    """질문이 비어 있으면 ValueError를 발생시킵니다."""
    cleaned = question.strip()
    if cleaned == "":
        raise ValueError("문제 생김")
    return cleaned


def main() -> None:
    questions = ["FastAPI란?", "   ", "Supabase란?"]

    for question in questions:
        try:
            cleaned_question = validate_question(question)
        except ValueError:
            print("비정상")
            break
        print("정상 질문:", cleaned_question)

main()
