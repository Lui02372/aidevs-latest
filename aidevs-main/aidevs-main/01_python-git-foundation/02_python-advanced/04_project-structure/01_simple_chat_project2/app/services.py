"""핵심 처리 로직을 모아두는 파일입니다.

이 예제에서는 질문을 받아 연습용 답변을 만드는 함수만 둡니다.

아직 하지 않는 것:
    - 질문 앞뒤 공백 제거
    - 빈 질문인지 검사
    - JSON 파일 저장
    - 예외 처리

이렇게 단순하게 시작하면 main.py와 services.py의 역할 차이를 먼저 익힐 수 있습니다.
"""

from app.models import RequestChatMessage as RequestMsg,ResponseChatMessage as ResponseMsg


def create_mock_answer(question: RequestMsg) -> str:
    """실제 AI API 대신 연습용 답변 문장을 만듭니다."""

    return f"'{question.prompt} {question.method}'에 대한 첫 번째 프로젝트 구조 연습 답변입니다."


def create_chat_message(question: RequestMsg) -> ResponseMsg:
    """질문을 받아 ChatMessage object를 만듭니다."""
    print("------------------------------------------")
    print(f"{question.user}질문 저장 {question.prompt}")
    print("------------------------------------------")

    answer = create_mock_answer(question)
    print("------------------------------------------")
    print(f"{answer}응답 저장")
    print("------------------------------------------")

    return ResponseMsg(
        answer=answer,
        model="practice-model",
    )
