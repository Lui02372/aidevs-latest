"""JSON으로 설정값과 API 응답 형태의 데이터를 저장하는 예제입니다."""

import json
from pathlib import Path

# data 폴더를 준비합니다.
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# API 호출이나 LLM 요청에 사용할 설정값을 dict로 준비합니다.
config = {
    "model": "practice-chat-model",
    "temperature": 0.3,
    "max_tokens": 512,
}

# API 응답을 흉내 낸 dict입니다.
response = {
    "question": "FastAPI에서 JSON은 왜 사용하나요?",
    "answer": "JSON은 API가 데이터를 주고받을 때 자주 사용하는 형식입니다.",
}

# 설정값과 응답을 하나의 dict로 묶습니다.
record = {
    "config": config,
    "response": response,
}

# JSON 파일 경로를 만듭니다.
json_path = data_dir / "chat_response.json"

# json.dumps는 dict/list를 JSON 문자열로 바꿉니다.
# ensure_ascii=False는 한글이 깨지지 않게 합니다.
# indent=2는 사람이 읽기 좋게 들여쓰기를 추가합니다.
json_text = json.dumps(record, ensure_ascii=False, indent=2)

# JSON 문자열을 파일에 저장합니다.
json_path.write_text(json_text, encoding="utf-8")

# 다시 파일을 읽고 json.loads로 dict로 복원합니다.
loaded_record = json.loads(json_path.read_text(encoding="utf-8"))

print("JSON 저장 파일:", json_path)
print("복원된 질문:", loaded_record["response"]["question"])
print("사용 모델:", loaded_record["config"]["model"])
