r"""직접 만든 모듈을 import하는 예제입니다.

실행 위치:
    C:\aidev\01_python-git-foundation

실행 명령:
    python .\02_python-advanced\01_function-and-import\03_import_my_module.py

이 예제의 목표:
    my_tools.py 파일에 있는 함수를 현재 파일에서 가져와 사용합니다.
    뒤 과정의 FastAPI 프로젝트도 여러 파일을 import해서 동작합니다.
"""

from my_tools import create_answer as ca, normalize_text as nt


def main() -> None:
    question = "  import는 왜 필요한가요?  "

    cleaned_question = nt(question)
    answer = ca(cleaned_question)

    print("정리된 질문:", cleaned_question)
    print("답변:", answer)


main()
