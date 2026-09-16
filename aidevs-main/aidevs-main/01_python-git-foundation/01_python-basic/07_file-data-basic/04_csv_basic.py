"""CSV 파일 저장과 읽기 예제입니다.

CSV는 표 형태 데이터를 저장할 때 자주 사용하는 파일 형식입니다.
엑셀, 구글 스프레드시트, 데이터 분석 도구에서 쉽게 열 수 있습니다.

CSV는 Comma Separated Values의 줄임말이며,
값을 쉼표로 구분해 저장하는 방식입니다.
"""

# csv는 Python이 기본으로 제공하는 CSV 처리 도구입니다.
import csv

# 파일 경로를 다루기 위해 Path를 가져옵니다.
from pathlib import Path

# data 폴더 경로를 준비합니다.
data_dir = Path("data")

# data 폴더가 없으면 새로 만듭니다.
data_dir.mkdir(exist_ok=True)

# students.csv 파일 경로를 준비합니다.
file_path = data_dir / "students.csv"

# CSV로 저장할 표 데이터를 list 안의 list 형태로 준비합니다.
# 첫 번째 줄은 컬럼 이름입니다.
students = [
    ["name", "score", "passed"],
    ["Jean", 95, True],
    ["Mina", 82, True],
    ["Jun", 58, False],
]

# 파일을 쓰기 모드("w")로 엽니다.
# newline=""은 Windows에서 빈 줄이 추가로 생기는 문제를 줄이기 위해 사용합니다.
with file_path.open("w", encoding="utf-8", newline="") as file:
    # csv.writer는 CSV 파일에 데이터를 쓰는 도구입니다.
    writer = csv.writer(file)

    # writerows()는 여러 줄을 한 번에 저장합니다.
    writer.writerows(students)

# 저장이 끝난 파일 경로를 출력합니다.
print("CSV 파일을 저장했습니다:", file_path)

# 이제 저장한 CSV 파일을 다시 읽어 봅니다.
print("\n[CSV 파일 읽기]")

# 파일을 읽기 모드("r")로 엽니다.
with file_path.open("r", encoding="utf-8", newline="") as file:
    # csv.reader는 CSV 파일을 한 줄씩 읽는 도구입니다.
    reader = csv.reader(file)

    # reader에서 row를 하나씩 꺼내면 각 줄이 list 형태로 나옵니다.
    for row in reader:
        print(row)
