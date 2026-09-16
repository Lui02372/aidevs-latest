"""pathlib로 데이터 폴더와 파일 경로를 관리하는 예제입니다."""

from pathlib import Path

# 현재 파일을 실행하는 기준 폴더 아래에 data 폴더를 만들 예정입니다.
data_dir = Path("data")

# mkdir은 폴더를 만드는 메서드입니다.
# exist_ok=True를 넣으면 이미 폴더가 있어도 오류가 나지 않습니다.
data_dir.mkdir(exist_ok=True)

# / 연산자를 사용하면 경로를 안전하게 이어 붙일 수 있습니다.
memo_path = data_dir / "memo.txt"

# write_text는 문자열을 파일에 저장합니다.
memo_path.write_text("데이터 폴더와 파일 경로 예제입니다.", encoding="utf-8")

# read_text는 파일 내용을 문자열로 읽어옵니다.
content = memo_path.read_text(encoding="utf-8")

# 결과를 출력합니다.
print("데이터 폴더:", data_dir)
print("메모 파일:", memo_path)
print("메모 내용:", content)
