"""함수를 인자로 전달해 서비스 처리 흐름을 바꾸는 예제입니다."""


def validate_not_empty(text: str) -> bool:
    """문자열이 비어 있지 않은지 확인합니다."""

    # strip은 앞뒤 공백을 제거합니다.
    return text.strip() != ""


def validate_min_length(text: str) -> bool:
    """문자열 길이가 5자 이상인지 확인합니다."""

    return len(text.strip()) >= 5


def process_question(question: str, validator) -> dict[str, str]:
    """질문과 검증 함수를 받아 요청 처리 결과를 만듭니다."""

    # validator에는 validate_not_empty 또는 validate_min_length 같은 함수가 들어올 수 있습니다.
    is_valid = validator(question)

    # 검증에 실패하면 실패 결과를 반환합니다.
    if not is_valid:
        return {"status": "error", "message": "질문 형식이 올바르지 않습니다."}

    # 검증에 성공하면 성공 결과를 반환합니다.
    return {"status": "ok", "message": question.strip()}


print("빈 값 검증:", process_question("FastAPI란?", validate_not_empty))
print("길이 검증:", process_question("AI", validate_min_length))
