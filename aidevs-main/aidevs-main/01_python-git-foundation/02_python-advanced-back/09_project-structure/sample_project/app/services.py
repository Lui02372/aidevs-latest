"""서비스 로직을 모아두는 파일입니다.

서비스 로직은 프로그램의 핵심 처리 과정입니다.
FastAPI 프로젝트에서는 라우터가 요청을 받고, 실제 처리는 services.py로 분리하는 경우가 많습니다.
"""

from app.config import DEFAULT_LLM_MODEL
from app.models import create_chat_reply


def normalize_question(question: str) -> str:
    """질문 앞뒤 공백을 제거합니다."""

    return question.strip()


def build_chat_reply(user_name: str, question: str) -> dict:
    """사용자 질문을 받아 챗봇 응답 데이터를 만듭니다."""

    clean_question = normalize_question(question)

    if clean_question == "":
        raise ValueError("질문은 비워둘 수 없습니다.")

    # 이후 LLM API 단원에서는 이 부분이 실제 AI 모델 호출 코드로 바뀝니다.
    # 지금은 프로젝트 구조를 이해하기 위해 고정 응답을 사용합니다.
    answer = "파일을 역할별로 나누면 코드를 찾고 수정하기 쉬워집니다."

    return create_chat_reply(
        user_name=user_name,
        question=clean_question,
        answer=answer,
        model=DEFAULT_LLM_MODEL,
    )
