"""패키지 안의 모듈을 import해서 사용하는 예제입니다."""

# shop은 폴더 이름이고, order_calculator는 그 안의 파이썬 파일 이름입니다.
# calculate_total은 order_calculator.py 안에 정의된 함수입니다.
from shop.order_calculator import calculate_total

# shop 패키지의 formatter.py 안에 있는 format_order_message 함수를 가져옵니다.
from shop.formatter import format_order_message

# 여러 상품 가격을 리스트로 준비합니다.
prices = [12000, 8000, 5000]

# 패키지 안의 함수를 사용해 총 금액을 계산합니다.
total = calculate_total(prices)

# 패키지 안의 다른 함수를 사용해 출력 문장을 만듭니다.
message = format_order_message("Mina", total)

# 결과를 출력합니다.
print(message)
