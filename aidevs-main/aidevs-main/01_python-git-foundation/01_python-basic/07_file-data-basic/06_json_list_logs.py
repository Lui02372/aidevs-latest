"""JSON list와 로그 데이터 저장 예제입니다.

실제 서비스에서는 데이터 한 개만 저장하지 않습니다.
사용자 목록, 대화 목록, 서비스 로그처럼 여러 개의 데이터를 저장합니다.

이 예제는 list 안에 dict를 넣어 여러 개의 로그를 JSON 파일로 저장합니다.
"""

# JSON 저장과 읽기를 위해 json 모듈을 가져옵니다.
import json

# 파일 경로를 다루기 위해 Path를 가져옵니다.
from pathlib import Path

# data 폴더 경로를 준비합니다.
data_dir = Path("data")

# data 폴더가 없으면 새로 만듭니다.
data_dir.mkdir(exist_ok=True)

# 여러 개의 로그를 list에 저장합니다.
# 각 로그는 dict 하나로 표현합니다.
logs = [
    {
        "level": "INFO",
        "message": "서비스 시작",
        "user": "Jean",
    },
    {
        "level": "INFO",
        "message": "질문 저장",
        "user": "Mina",
    },
    {
        "level": "WARNING",
        "message": "응답 시간이 길어짐",
        "user": "Jun",
    },
]

# service_logs.json 파일 경로를 준비합니다.
file_path = data_dir / "service_logs.json"

# list 안의 dict 구조를 JSON 문자열로 바꾸어 파일에 저장합니다.
file_path.write_text(
    json.dumps(logs, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

# 저장된 JSON 파일을 다시 읽고 Python list로 바꿉니다.
loaded_logs = json.loads(file_path.read_text(encoding="utf-8"))

# 읽어온 로그 목록을 출력합니다.
print("[서비스 로그]")

# enumerate()를 사용해 로그 번호를 1부터 붙입니다.
for index, log in enumerate(loaded_logs, start=1):
    print(index)

    # log는 dict이므로 key로 값을 꺼냅니다.
    print("레벨:", log["level"])
    print("메시지:", log["message"])
    print("사용자:", log["user"])

    # "-" 문자를 20번 반복해 구분선을 출력합니다.
    print("-" * 20)
