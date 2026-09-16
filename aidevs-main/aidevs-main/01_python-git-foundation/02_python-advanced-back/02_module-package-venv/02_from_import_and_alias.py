"""from import와 별칭 import를 사용하는 예제입니다."""

# pathlib 모듈에서 Path 클래스만 가져옵니다.
# 이렇게 가져오면 pathlib.Path가 아니라 Path라고 바로 사용할 수 있습니다.
from pathlib import Path

# datetime 모듈은 dt라는 짧은 별칭으로 가져옵니다.
# 모듈 이름이 길거나 자주 사용할 때 별칭을 붙이면 코드가 짧아집니다.
import datetime as dt

# 현재 작업 폴더를 Path 객체로 가져옵니다.
current_folder = Path.cwd()

# 현재 날짜만 가져옵니다.
today = dt.date.today()

# 결과를 출력합니다.
print("현재 작업 폴더:", current_folder)
print("오늘 날짜:", today)

# Path 객체는 경로를 조립할 때 편리합니다.
example_path = current_folder / "example.txt"

# 조립된 경로를 출력합니다.
print("예시 파일 경로:", example_path)
