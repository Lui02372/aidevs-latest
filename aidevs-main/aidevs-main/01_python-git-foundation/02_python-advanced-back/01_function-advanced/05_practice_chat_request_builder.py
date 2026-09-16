"""함수 분리를 이용해 LLM 질문 요청 데이터를 만드는 미니 실습입니다."""


def normalize_question(question: str) -> str:
    """질문 앞뒤 공백을 제거합니다."""

    return question.strip()


def validate_question(question: str) -> bool:
    """질문이 비어 있지 않은지 확인합니다."""

    return question != ""


def build_chat_request(question: str, **options: str) -> dict[str, object]:
    """LLM API에 전달할 질문 요청 데이터를 만듭니다."""

    # 먼저 질문을 정리합니다.
    normalized_question = normalize_question(question)

    # 질문이 비어 있으면 오류 상태를 반환합니다.
    if not validate_question(normalized_question):
        return {
            "ok": False,
            "error": "질문은 비워둘 수 없습니다.",
        }

    # 질문이 정상이라면 API 요청에 사용할 dict를 만듭니다.
    return {
        "ok": True,
        "message": normalized_question,
        "options": options,
    }


request1 = build_chat_request("  FastAPI에서 Pydantic은 왜 사용하나요?  ", model="practice-chat-model")
request2 = build_chat_request("   ", model="practice-chat-model")

print("정상 요청:", request1)
print("잘못된 요청:", request2)
