"""import 연습에 사용할 함수 모음입니다.

이 파일은 직접 실행하기보다 다른 파일에서 import해서 사용합니다.

뒤 과정에서는 services.py, storage.py 같은 파일에 함수를 만들고,
main.py 또는 router 파일에서 import해서 사용하게 됩니다.
"""


def normalize_text(text: str) -> str:
    """문자열 앞뒤 공백을 제거합니다."""

    return text.strip()


def create_answer(question: str) -> str:
    """연습용 답변 문자열을 만듭니다."""

    return f"'{question}'에 대한 import 연습 답변입니다."
