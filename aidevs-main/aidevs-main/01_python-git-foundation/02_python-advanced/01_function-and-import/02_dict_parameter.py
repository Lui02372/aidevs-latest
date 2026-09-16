r"""dict 데이터를 함수에 전달하는 예제입니다.

실행 위치:
    C:\aidev\01_python-git-foundation

실행 명령:
    python .\02_python-advanced\01_function-and-import\02_dict_parameter.py

이 예제의 목표:
    FastAPI, Supabase, LLM API에서는 dict 형태의 데이터를 자주 다룹니다.
    이 예제에서는 dict에서 필요한 값을 꺼내 함수 안에서 처리합니다.
"""

from myteam.llm import build_chat_response as chat_response


def main() -> None:

    msg = input("뭐가 궁금해 ? ")

    if msg == "":
        return

    request_data = {
        "user": "kim",
        "message": f"{msg}",
        "model": "GPT5.0",
    }

    response = chat_response(request_data)

    print("요청 dict:")
    print(request_data["message"])
    print()
    print("응답 dict:")
    print(response["answer"])


main()
