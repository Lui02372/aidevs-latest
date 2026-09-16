"""파일 경로 기초 예제입니다.

파일을 저장하거나 읽으려면 먼저 "어디에 저장할 것인지"를 정해야 합니다.
Python에서는 pathlib의 Path를 사용하면 파일과 폴더 경로를 쉽게 다룰 수 있습니다.

이 예제에서는 data 폴더를 만들고, 그 안에 파일 경로를 준비합니다.
"""

# pathlib은 Python이 기본으로 제공하는 표준 라이브러리입니다.
# Path는 파일 경로와 폴더 경로를 다룰 때 사용하는 도구입니다.
from pathlib import Path

# "data"라는 이름의 폴더 경로를 Path 객체로 만듭니다.
# 아직 실제 폴더가 만들어진 것은 아니고, 경로 정보만 준비한 상태입니다.
data_dir = Path("data")

# print()는 화면에 값을 출력합니다.
# 여기서는 Path 객체가 어떤 경로를 가리키는지 확인합니다.
print("data 폴더 경로:", data_dir)

# exists()는 해당 경로가 실제로 존재하는지 True 또는 False로 알려줍니다.
print("data 폴더가 이미 있나요?", data_dir.exists())

# mkdir()은 폴더를 만드는 함수입니다.
# exist_ok=True는 폴더가 이미 있어도 오류를 내지 말라는 뜻입니다.
data_dir.mkdir(exist_ok=True)

# 폴더를 만든 뒤 다시 exists()로 실제 생성 여부를 확인합니다.
print("data 폴더 생성 후:", data_dir.exists())

# / 연산자를 사용하면 폴더 경로와 파일 이름을 자연스럽게 연결할 수 있습니다.
# 아래 코드는 data 폴더 안의 memo.txt 파일 경로를 의미합니다.
memo_path = data_dir / "memo.txt"

# memo_path는 아직 파일을 만든 것은 아니고, 파일이 저장될 위치를 나타냅니다.
print("메모 파일 경로:", memo_path)

# name은 경로에서 파일 이름만 꺼냅니다.
print("메모 파일 이름:", memo_path.name)

# suffix는 파일 확장자만 꺼냅니다.
print("메모 파일 확장자:", memo_path.suffix)
