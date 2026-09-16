"""파이썬 표준 라이브러리를 import해서 사용하는 예제입니다."""

# math는 수학 계산에 필요한 기능을 제공하는 표준 라이브러리입니다.
# 표준 라이브러리는 파이썬을 설치하면 함께 사용할 수 있습니다.
import math

# datetime은 날짜와 시간을 다룰 때 사용하는 표준 라이브러리입니다.
import datetime

# math.sqrt()는 제곱근을 계산합니다.
square_root = math.sqrt(16)

# math.ceil()은 소수점이 있는 숫자를 올림합니다.
rounded_up = math.ceil(3.2)

# datetime.datetime.now()는 현재 날짜와 시간을 가져옵니다.
now = datetime.datetime.now()

# 계산 결과를 출력합니다.
print("16의 제곱근:", square_root)
print("3.2를 올림:", rounded_up)
print("현재 날짜와 시간:", now)
