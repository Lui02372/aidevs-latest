"""여러 줄 텍스트 저장과 추가 저장 예제입니다.

텍스트 파일에는 한 줄만 저장할 수도 있고, 여러 줄을 저장할 수도 있습니다.
로그 파일처럼 뒤에 계속 내용을 추가해야 할 때는 append 모드를 사용합니다.
"""

# 파일과 폴더 경로를 다루기 위해 Path를 가져옵니다.
from pathlib import Path

# data 폴더 경로를 준비합니다.
data_dir = Path("data")

# data 폴더가 없으면 새로 만듭니다.
data_dir.mkdir(exist_ok=True)

# daily_log.txt 파일 경로를 준비합니다.
file_path = data_dir / "daily_log.txt"

# 여러 줄로 저장할 내용을 list에 담습니다.
# list의 각 값이 파일의 한 줄이 됩니다.
lines = [
    "Python 기초 학습 시작",
    "조건문과 반복문 복습",
    "파일 저장 예제 실행",
]

# "\n".join(lines)는 리스트 안의 문자열을 줄바꿈 문자로 연결합니다.
# 결과는 "첫 줄\n둘째 줄\n셋째 줄" 같은 하나의 긴 문자열이 됩니다.
text = "\n".join(lines)

# 여러 줄 문자열을 파일에 저장합니다.
file_path.write_text(text, encoding="utf-8")

# open(..., "a")에서 "a"는 append의 뜻입니다.
# append 모드는 기존 파일 내용 뒤에 새로운 내용을 추가합니다.
# with를 사용하면 파일 사용이 끝난 뒤 자동으로 닫힙니다.
with file_path.open("a", encoding="utf-8") as file:
    # 앞에 "\n"을 붙여 새 줄에 내용이 추가되도록 합니다.
    file.write("\nJSON 예제 준비")

# 파일 전체 내용을 다시 읽어옵니다.
content = file_path.read_text(encoding="utf-8")

# 전체 내용을 그대로 출력합니다.
print("[전체 파일 내용]")
print(content)

# 줄 단위로 나누어 출력합니다.
print("\n[줄 단위로 읽기]")

# splitlines()는 문자열을 줄 단위 list로 나눕니다.
# enumerate(..., start=1)는 번호를 1부터 붙여 줍니다.
for index, line in enumerate(content.splitlines(), start=1):
    print(index, line)
