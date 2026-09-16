"""pytest로 테스트할 서비스 함수 모음입니다.

이 파일은 직접 실행하는 파일이라기보다 test_service_logic.py에서 import해서 테스트합니다.
"""


def normalize_question(question: str) -> str:
    """질문 앞뒤 공백을 제거합니다."""

    return question.strip()


def validate_question(question: str) -> str:
    """질문이 비어 있으면 ValueError를 발생시킵니다."""

    cleaned = normalize_question(question)

    if cleaned == "":
        raise ValueError("질문은 비워둘 수 없습니다.")

    return cleaned


def build_response(question: str) -> dict:
    """연습용 응답 dict를 만듭니다."""

    cleaned = validate_question(question)

    return {
        "question": cleaned,
        "answer": f"'{cleaned}'에 대한 연습용 답변입니다.",
        "model": "practice-model",
    }
