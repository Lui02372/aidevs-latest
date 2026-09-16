"""테스트 대상이 되는 간단한 서비스 로직입니다.

이 파일은 직접 실행하기보다 test_service_logic.py에서 import해서 테스트합니다.

테스트를 쉽게 하려면 함수가 너무 많은 일을 한 번에 하지 않는 것이 좋습니다.
아래 예제도 질문 정리, 질문 검증, 응답 생성 기능을 함수로 나누었습니다.
이렇게 나누면 각 함수를 따로 테스트할 수 있습니다.
"""


def normalize_question(question: str) -> str:
    """질문 앞뒤 공백을 제거합니다.

    사용자가 입력한 값에는 앞뒤 공백이 섞일 수 있습니다.
    API나 DB에 저장하기 전에 같은 형태로 정리하면 이후 처리가 쉬워집니다.
    """

    return question.strip()


def validate_question(question: str) -> None:
    """질문이 비어 있으면 오류를 발생시킵니다.

    잘못된 입력은 조용히 넘어가지 않고 명확한 오류로 처리합니다.
    테스트에서는 pytest.raises로 이 오류가 실제로 발생하는지 확인합니다.
    """

    if normalize_question(question) == "":
        raise ValueError("질문은 비워둘 수 없습니다.")


def build_chat_response(question: str) -> dict[str, str]:
    """질문을 받아 API 응답처럼 사용할 dict를 만듭니다.

    이후 FastAPI에서는 이런 dict가 JSON 응답으로 바뀝니다.
    그래서 테스트에서는 question, answer 같은 필수 key가 있는지 확인합니다.
    """

    # 먼저 질문이 유효한지 확인합니다.
    validate_question(question)

    # 실제 LLM 호출 대신, 테스트하기 쉬운 고정 응답을 만듭니다.
    normalized = normalize_question(question)

    return {
        "question": normalized,
        "answer": f"'{normalized}' 질문을 처리했습니다.",
    }
