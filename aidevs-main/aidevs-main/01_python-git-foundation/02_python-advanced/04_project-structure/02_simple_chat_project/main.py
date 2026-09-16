r"""작은 채팅 기록 프로젝트의 실행 시작점입니다.

실행 위치:
    C:\aidev\01_python-git-foundation

실행 명령:
    python .\02_python-advanced\04_project-structure\02_simple_chat_project\main.py

이 파일의 역할:
    1. 사용자 질문을 준비합니다.
    2. services.py에 있는 함수로 응답 데이터를 만듭니다.
    3. storage.py에 있는 함수로 JSON 파일에 저장합니다.

중요:
    main.py에는 모든 기능을 직접 작성하지 않습니다.
    main.py는 여러 파일의 함수를 연결하는 시작점 역할만 합니다.
"""

from app.services import create_chat_message
from app.storage import load_messages, save_message


def main() -> None:
    question = "FastAPI 프로젝트 구조는 왜 나누나요?"

    message = create_chat_message(question)
    save_message(message)

    messages = load_messages()

    print("새 메시지를 저장했습니다.")
    print("저장된 메시지 수:", len(messages))
    print("마지막 메시지:")
    print(messages[-1])


main()
