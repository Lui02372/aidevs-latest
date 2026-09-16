"""핵심 처리 로직을 모아두는 파일입니다.

FastAPI 프로젝트에서는 endpoint 함수 안에 모든 코드를 쓰지 않고,
이런 service 함수로 실제 처리 로직을 나누는 경우가 많습니다.
"""

from app.models import ChatMessage


def normalize_question(question: str) -> str:
    """질문 앞뒤 공백을 제거합니다."""

    return question.strip()


def validate_question(question: str) -> str:
    """질문이 비어 있으면 ValueError를 발생시킵니다."""

    cleaned = normalize_question(question)

    if cleaned == "":
        raise ValueError("질문은 비워둘 수 없습니다.")

    return cleaned


def create_mock_answer(question: str) -> str:
    """실제 AI API 대신 연습용 답변을 만듭니다."""

    return f"'{question}'에 대한 프로젝트 구조 연습 답변입니다."


def create_chat_message(question: str) -> ChatMessage:
    """질문을 받아 ChatMessage object를 만듭니다."""

    cleaned = validate_question(question)
    answer = create_mock_answer(cleaned)

    return ChatMessage(
        question=cleaned,
        answer=answer,
        model="practice-model",
    )
