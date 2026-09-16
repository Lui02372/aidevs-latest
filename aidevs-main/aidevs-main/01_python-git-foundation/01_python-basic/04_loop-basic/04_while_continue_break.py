"""while 반복문에서 continue와 break를 사용하는 예제입니다.

이번에는 `while` 반복문 안에서 `continue`와 `break`를 사용합니다.

for 반복문과 문법의 의미는 같습니다.
다만 while 반복문에서는 continue 전에 반복 조건을 바꾸는 코드를
빠뜨리면 무한 루프가 될 수 있으므로 더 조심해야 합니다.
"""

count = 0

while count < 10:
    # 반복이 한 번 돌 때마다 count를 먼저 증가시킵니다.
    # 이 위치가 중요합니다. continue가 실행되어도 count는 이미 증가한 상태입니다.
    count += 1

    print("현재 count:", count)

    # 짝수는 처리하지 않고 다음 반복으로 넘어갑니다.
    if count % 2 == 0:
        print("짝수는 건너뜁니다. continue 실행")
        continue

    # count가 7이면 반복문 전체를 종료합니다.
    if count == 7:
        print("7을 만나서 반복문을 종료합니다. break 실행")
        break

    print("처리한 홀수:", count)

print("while 반복문이 끝났습니다.")
