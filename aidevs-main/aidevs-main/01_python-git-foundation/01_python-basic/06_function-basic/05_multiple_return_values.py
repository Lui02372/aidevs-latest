"""여러 값을 반환하는 함수 예제입니다.

Python 함수는 여러 값을 한 번에 반환할 수 있습니다.
실제로는 tuple 형태로 반환되고, 이를 여러 변수에 나누어 받을 수 있습니다.
"""


def calculate(a: float, b: float)-> tuple[float, float, float, float]:
    """"""
    add_result = a + b
    subtract_result = a - b
    multiply_result = a * b
    divide_result = a / b

    return add_result, subtract_result, multiply_result, divide_result

# aa = (1,2,3,4)
result: tuple[float, float, float, float] = calculate(10.0, 2.0)
for value in result:
    print(value)


# Tuple unpacking을 사용하면 tuple 안의 값을 여러 변수에 나누어 담을 수 있습니다.
plus, minus, multiply, divide = calculate(10, 2)

print("더하기:", plus)
print("빼기:", minus)
print("곱하기:", multiply)
print("나누기:", divide)


def get_min_max(numbers:list[int]) -> tuple[int, int]:
    smallest = min(numbers)
    largest = max(numbers)
    return smallest, largest


scores = [80, 95, 70, 88]
min_score, max_score = get_min_max(scores)

print("최저 점수:", min_score)
print("최고 점수:", max_score)


print("------------------------------------------------")

# 숫자로 되어 있는 List를 입력하면
# 최소값과 최대값 합계 평균을 반환하는 함수를 만들어 보세요.
# dict 형태로 반환하는 함수를 구현 하시오
# 함수명: total_datas 
datas = [10,30,40,10,20,50,60]
def total_datas(numbers:list[int]) -> dict[str, float]:
    smallest = min(numbers)
    largest = max(numbers)
    total = sum(numbers)
    average = total / len(numbers)
    return {
        "최소값": smallest, 
        "최대값": largest, 
        "합계": total, 
        "평균": average}


result: dict[str, float] = total_datas(datas)
print("최소값:", result["최소값"])
print("최대값:", result["최대값"])
print("합계:", result["합계"])
print("평균:", result["평균"])

