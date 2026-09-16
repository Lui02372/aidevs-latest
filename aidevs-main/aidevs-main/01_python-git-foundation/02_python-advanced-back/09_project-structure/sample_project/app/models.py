"""프로젝트에서 주고받는 데이터 모양을 정리하는 파일입니다.

아직 Pydantic을 본격적으로 사용하기 전이므로 dict 타입으로 단순하게 표현합니다.
이후 FastAPI에서는 이 역할을 Pydantic 모델이 담당합니다.
"""


def create_chat_reply(user_name: str, question: str, answer: str, model: str) -> dict:
    """챗봇 응답 데이터를 dict 형태로 만듭니다."""

    return {
        "user_name": user_name,
        "question": question,
        "answer": answer,
        "model": model,
    }
