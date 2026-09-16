"""계산기 코드를 함수로 정리하는 예제입니다.

반복문 단원에서 계산기 프로그램을 만들었습니다.
이번에는 계산 로직을 함수로 분리합니다.

함수로 나누면 좋은 점:
1. 계산 코드만 따로 테스트하기 쉽습니다.
2. 프로그램 흐름과 계산 로직을 분리할 수 있습니다.
3. 나중에 기능을 추가하기 쉽습니다.
"""


def calculate(a:int, b:int, operator:str)->float:
    if operator == "+":
        return a + b
    if operator == "-":
        return a - b
    if operator == "*":
        return a * b
    if operator == "/":
        if b == 0:
            return None
        return a / b
    if operator == "%":
        return a % b
    return None

   


print("계산 함수 테스트")

print("10 + 5 =", calculate(10, 5, "+"))
print("10 - 5 =", calculate(10, 5, "-"))
print("10 * 5 =", calculate(10, 5, "*"))
print("10 / 5 =", calculate(10, 5, "/"))
print("10 / 0 =", calculate(10, 0, "/"))
print("10 % 5 =", calculate(10, 5, "%"))

print("\n함수로 분리하면 입력을 받지 않아도 계산 기능만 확인할 수 있습니다.")
