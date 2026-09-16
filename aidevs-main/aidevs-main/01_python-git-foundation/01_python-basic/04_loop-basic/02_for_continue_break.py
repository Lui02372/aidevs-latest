"""for 반복문에서 continue와 break를 사용하는 예제입니다.

`continue`와 `break`는 반복문의 흐름을 바꾸는 문법입니다.

continue:
    이번 반복의 남은 코드를 건너뛰고 다음 반복으로 이동합니다.

break:
    반복문 전체를 즉시 종료합니다.

먼저 `for` 반복문에서 두 문법의 차이를 확인합니다.
"""

print("1부터 7까지 반복하면서 continue와 break를 확인합니다.")

for number in range(1, 8):
    print("현재 숫자:", number)

    # number가 3이면 아래 print를 실행하지 않고 다음 반복으로 넘어갑니다.
    if number == 3:
        print("3은 건너뜁니다. continue 실행")
        continue

    # number가 6이면 반복문 전체를 끝냅니다.
    if number == 6:
        print("6을 만나서 반복문을 종료합니다. break 실행")
        break

    print("처리한 숫자:", number)

print("for 반복문이 끝났습니다.")
