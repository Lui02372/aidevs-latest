"""샘플 프로젝트의 실행 시작점입니다.

이 파일은 실제 작업을 모두 직접 처리하지 않습니다.
대신 app 폴더에 나누어 둔 설정, 서비스 함수, 저장 함수를 불러와 실행합니다.
"""

from app.config import DEFAULT_USER_NAME
from app.services import build_chat_reply
from app.storage import save_chat_log


def main() -> None:
    """샘플 프로젝트를 실행합니다."""

    # 실제 서비스에서는 사용자가 화면에서 질문을 입력합니다.
    # 여기서는 프로젝트 구조를 이해하기 위해 예제 질문을 코드 안에 준비합니다.
    question = "FastAPI 프로젝트는 왜 파일을 나누나요?"

    # 서비스 함수는 질문을 받아 응답 데이터를 만들어 줍니다.
    # main.py는 세부 처리 방법을 몰라도 build_chat_reply 함수만 호출하면 됩니다.
    reply = build_chat_reply(user_name=DEFAULT_USER_NAME, question=question)

    # 저장 함수는 응답 데이터를 받아 저장소에 기록합니다.
    # 지금은 메모리 리스트에 저장하지만, 이후에는 Supabase 저장으로 연결됩니다.
    saved_log = save_chat_log(reply)

    # 최종 결과를 화면에 출력합니다.
    print("질문:", saved_log["question"])
    print("답변:", saved_log["answer"])
    print("저장 상태:", saved_log["status"])


# 이 파일을 직접 실행할 때만 main 함수를 호출합니다.
# 다른 파일에서 import할 때 자동 실행되는 것을 막기 위한 기본 구조입니다.
if __name__ == "__main__":
    main()
