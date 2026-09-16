"""데이터 저장 역할을 모아두는 파일입니다.

지금은 리스트에 데이터를 저장하는 방식으로 연습합니다.
이후 과정에서는 이 역할이 Supabase 테이블 저장 코드로 바뀝니다.
"""

# 프로그램이 실행되는 동안만 유지되는 임시 저장소입니다.
# 프로그램을 종료하면 이 리스트의 내용은 사라집니다.
CHAT_LOGS: list[dict] = []


def save_chat_log(reply: dict) -> dict:
    """챗봇 응답 데이터를 임시 저장소에 저장합니다."""

    CHAT_LOGS.append(reply)

    return {
        "status": "saved",
        "question": reply["question"],
        "answer": reply["answer"],
        "total_logs": len(CHAT_LOGS),
    }
