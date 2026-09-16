"""반복문을 사용한 간단한 계산기 예제입니다.

이 예제는 지금까지 배운 내용을 함께 사용합니다.

사용하는 문법:
1. while True
2. input()
3. if / elif / else
4. break
5. 숫자 형변환 float()

프로그램 흐름:
1. 첫 번째 숫자를 입력합니다.
2. 두 번째 숫자를 입력합니다.
3. 사칙연산 기호 중 하나를 입력합니다.
4. 계산 결과를 출력합니다.
5. q를 입력하면 프로그램을 종료합니다.
"""

print("반복 계산기 프로그램입니다.")
print("종료하려면 첫 번째 숫자 입력 위치에서 q를 입력하세요.")

while True:
    first_text = input("첫 번째 숫자를 입력하세요: ")

    # 첫 번째 입력값이 q이면 프로그램을 종료합니다.
    if first_text.strip().lower() == "q":
        print("계산기를 종료합니다.")
        break

    second_text = input("두 번째 숫자를 입력하세요: ")
    operator = input("연산자를 입력하세요(+, -, *, /): ")

    # input()으로 받은 값은 문자열입니다.
    # 계산하려면 숫자로 바꾸어야 합니다.
    # float()를 사용하면 정수와 소수 모두 계산할 수 있습니다.
    first_number = float(first_text)
    second_number = float(second_text)

    if operator == "+":
        result = first_number + second_number
        print("계산 결과:", result)

    elif operator == "-":
        result = first_number - second_number
        print("계산 결과:", result)

    elif operator == "*":
        result = first_number * second_number
        print("계산 결과:", result)

    elif operator == "/":
        # 0으로 나누면 오류가 발생합니다.
        # 그래서 나누기 전에 두 번째 숫자가 0인지 먼저 확인합니다.
        if second_number == 0:
            print("0으로 나눌 수 없습니다.")
        else:
            result = first_number / second_number
            print("계산 결과:", result)

    else:
        print("지원하지 않는 연산자입니다.")

    print("다음 계산을 계속합니다.")
    print()
