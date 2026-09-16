"""텍스트 파일 저장과 읽기 예제입니다.

프로그램이 종료되어도 데이터를 남기고 싶을 때 파일을 사용합니다.
이 예제는 문자열을 텍스트 파일에 저장한 뒤 다시 읽어옵니다.
"""

# Path를 사용하기 위해 pathlib에서 가져옵니다.
from pathlib import Path

# data 폴더 경로를 준비합니다.
data_dir = Path("data")

# data 폴더가 없으면 만들고, 이미 있으면 그대로 사용합니다.
data_dir.mkdir(exist_ok=True)

# data 폴더 안에 memo.txt라는 파일 경로를 만듭니다.
file_path = data_dir / "memo.txt"

# write_text()는 문자열을 텍스트 파일에 저장합니다.
# 같은 파일에 다시 저장하면 기존 내용은 새 내용으로 바뀝니다.
# encoding="utf-8"은 한글이 깨지지 않도록 UTF-8 방식으로 저장한다는 뜻입니다.
file_path.write_text("Python 파일 저장 연습입니다.", encoding="utf-8")

# read_text()는 텍스트 파일의 내용을 문자열로 읽어옵니다.
# 저장할 때와 같은 encoding="utf-8"로 읽는 것이 좋습니다.
content = file_path.read_text(encoding="utf-8")

# 파일이 저장된 경로를 출력합니다.
print("파일 경로:", file_path)

# 파일에서 읽어온 내용을 출력합니다.
print("파일 내용:", content)
