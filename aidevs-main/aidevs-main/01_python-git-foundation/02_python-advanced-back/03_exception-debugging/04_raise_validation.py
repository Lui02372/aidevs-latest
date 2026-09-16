"""raise를 사용해 직접 검증 오류를 발생시키는 예제입니다."""


def validate_question(question: str) -> None:
    """사용자 질문이 비어 있지 않은지 확인합니다."""

    # strip은 문자열 앞뒤 공백을 제거합니다.
    if question.strip() == "":
        # 서비스 로직에서 허용할 수 없는 값이면 직접 오류를 발생시킵니다.
        raise ValueError("질문은 비워둘 수 없습니다.")


def create_chat_request(question: str) -> dict[str, str]:
    """질문을 검증한 뒤 요청 데이터 형태로 만듭니다."""

    # 검증에 실패하면 여기서 ValueError가 발생합니다.
    validate_question(question)

    # 검증을 통과하면 딕셔너리로 요청 데이터를 만듭니다.
    return {"question": question.strip()}


for text in ["FastAPI란 무엇인가요?", "   "]:
    try:
        request = create_chat_request(text)
        print("요청 생성 성공:", request)

    except ValueError as error:
        print("요청 생성 실패:", error)
