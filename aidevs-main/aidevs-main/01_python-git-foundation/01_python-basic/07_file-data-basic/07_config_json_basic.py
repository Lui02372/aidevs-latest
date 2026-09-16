"""설정 파일 JSON 예제입니다.

프로그램에서 자주 바뀌는 값은 코드 안에 직접 쓰기보다
설정 파일로 분리할 수 있습니다.

이 예제는 config.json 파일을 만들고,
프로그램에서 필요한 설정값을 읽어옵니다.
"""

# 설정값을 JSON으로 저장하고 읽기 위해 json 모듈을 가져옵니다.
import json

# 파일 경로를 다루기 위해 Path를 가져옵니다.
from pathlib import Path

# data 폴더 경로를 준비합니다.
data_dir = Path("data")

# data 폴더가 없으면 새로 만듭니다.
data_dir.mkdir(exist_ok=True)

# 프로그램 설정값을 dict로 준비합니다.
# 실제 서비스에서는 모델 이름, 디버그 여부, 제한 값 등을 설정 파일에 둘 수 있습니다.
config = {
    "app_name": "AI Backend Practice",
    "debug": True,
    "default_model": "gemini-2.5-flash-lite",
    "max_messages": 20,
}

# config.json 파일 경로를 준비합니다.
file_path = data_dir / "config.json"

# config dict를 JSON 문자열로 바꾸어 파일에 저장합니다.
file_path.write_text(
    json.dumps(config, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

# 저장된 설정 파일을 다시 읽고 Python dict로 바꿉니다.
loaded_config = json.loads(file_path.read_text(encoding="utf-8"))

# 설정값은 dict의 key로 꺼내 사용할 수 있습니다.
print("앱 이름:", loaded_config["app_name"])
print("디버그 모드:", loaded_config["debug"])
print("기본 모델:", loaded_config["default_model"])
print("최대 메시지 수:", loaded_config["max_messages"])
