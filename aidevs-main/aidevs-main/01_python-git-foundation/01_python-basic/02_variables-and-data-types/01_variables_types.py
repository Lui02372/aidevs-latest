"""변수와 자료형 예제입니다.

변수는 값을 담아 두는 이름입니다.
자료형은 값의 종류를 의미합니다.

이 예제에서는 문자열(str), 정수(int), 불(bool)을 확인합니다.
"""

# 변수는 값을 담는 이름입니다.
# 오른쪽 값을 왼쪽 변수 이름에 저장한다고 이해하면 됩니다.
user_name = "Jean"
user_name = 'kim'
user_age = 30
user_height = 180.5
is_beginner = True
user_height = "180.5cm"  # 문자열로 저장

# 변수 이름 뒤에 : str, : int, : bool처럼 적는 것을 타입 힌트라고 합니다.
# name: str = "kim"은 "name 변수는 문자열로 사용할 예정"이라는 뜻입니다.
# 지금은 힌트처럼 이해하고, FastAPI/Pydantic을 배울 때 더 자주 만나게 됩니다.
name: str = "kim"
age: int = 20
height: float = 180.5
# weight: double = 70.5
is_student: bool = True
name = 100
print(type(name), type(age), type(height), type(is_student))




# 문자열, 숫자, True/False 값을 각각 출력합니다.
print("이름:", user_name, "입니다.")
print("나이:", user_age)
print("초보자인가요?", is_beginner)
print("타입 힌트 예시:", name, age, is_student)

# type()은 값이나 변수의 자료형을 확인하는 함수입니다.
# str은 문자열, int는 정수, bool은 참/거짓 값을 뜻합니다.
print(type(user_name))
print(type(user_age))
print(type(is_beginner))

# input()으로 받은 값이나 따옴표로 감싼 숫자는 문자열입니다.
# 문자열 "1000"은 숫자 1000과 다르기 때문에 바로 계산할 수 없습니다.
price_text = "1000"

# print("가격 + 500 =", price_text / 500)  # 문자열 결합

# int()는 숫자 모양의 문자열을 정수로 변환합니다.
price = float(price_text)
print("가격 + 500 =", price + 500)

num1 = 10
num2 = 3
num3 = 100

result = num3 + num1 / num2
print("결과:", result)