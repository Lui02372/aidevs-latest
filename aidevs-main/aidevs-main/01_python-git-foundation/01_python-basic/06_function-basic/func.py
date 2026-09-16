# func.py
def add_numbers(num1:int, num2:int) -> int:
    return num1 + num2


num1 = 1
num2 = 2
total = add_numbers(num1, num2)
avg = total / 2
print(f"합계: {total}, 평균: {avg}")

num3 = 3
num4 = 4
total = add_numbers(num3, num4)
avg = total / 2
print(f"합계: {total}, 평균: {avg}")


print("-------------------------")

def calculate_data(numbers:list[int]) -> tuple[int, float]:
    """주어진 숫자 리스트의 합계와 평균을 계산합니다."""
    total = sum(numbers)
    average = total / len(numbers)
    return total, average

# 각 데이터의 평균보다 큰 수를 리턴 하는 함수를 구현 하시오
# 함수 정의 -
def over_date(list_data:list)->tuple:
    # 평균을 구한다
    total, avg_number = calculate_data(list_data)
    # 평균 보다 큰수를 results 담는다
    results = list()
    for data in list_data:
        if data > avg_number:
            results.append(data)
    return tuple(results)




datas1 = [1, 2, 3, 4, 5]
datas1_total, datas1_average = calculate_data(datas1)
print(f"합계: {datas1_total}, 평균: {datas1_average}")
big_data:tuple = over_date(datas1)
print(big_data)

datas2 = [6, 7, 8, 9, 10]
datas2_total, datas2_average = calculate_data(datas2)
print(f"합계: {datas2_total}, 평균: {datas2_average}")
big_data:tuple = over_date(datas2)
print(big_data)

