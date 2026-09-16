"""JSON dict 저장과 읽기 예제입니다.

JSON은 데이터를 저장하거나 API로 주고받을 때 자주 사용하는 형식입니다.
Python의 dict는 JSON 형식으로 바꾸어 파일에 저장할 수 있습니다.

이 예제는 학생 한 명의 정보를 JSON 파일에 저장합니다.
"""

# json은 Python 자료구조를 JSON 문자열로 바꾸거나,
# JSON 문자열을 Python 자료구조로 바꿀 때 사용하는 표준 라이브러리입니다.
import json

# 파일 경로를 다루기 위해 Path를 가져옵니다.
from pathlib import Path

# data 폴더 경로를 준비합니다.
data_dir = Path("data")

# data 폴더가 없으면 새로 만듭니다.
data_dir.mkdir(exist_ok=True)

# JSON으로 저장할 학생 정보를 dict로 만듭니다.
student = {
    "name": "Jean",
    "score": 95,
    "passed": True,
}

# student.json 파일 경로를 준비합니다.
file_path = data_dir / "student.json"

# json.dumps()는 Python dict를 JSON 문자열로 바꿉니다.
# ensure_ascii=False는 한글을 실제 글자로 저장하게 합니다.
# indent=2는 사람이 읽기 좋게 들여쓰기합니다.
json_text = json.dumps(student, ensure_ascii=False, indent=2)

# JSON 문자열을 파일에 저장합니다.
file_path.write_text(json_text, encoding="utf-8")

# 저장한 파일 경로를 출력합니다.
print("JSON 파일을 저장했습니다:", file_path)

# 파일에서 JSON 문자열을 다시 읽어옵니다.
loaded_text = file_path.read_text(encoding="utf-8")

# json.loads()는 JSON 문자열을 다시 Python dict로 바꿉니다.
loaded_student = json.loads(loaded_text)

# dict가 되었으므로 key를 사용해 값을 꺼낼 수 있습니다.
print("읽어온 이름:", loaded_student["name"])
print("읽어온 점수:", loaded_student["score"])
