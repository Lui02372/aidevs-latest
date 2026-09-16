"""if, elif, else를 함께 사용하는 조건문 예제입니다.

조건문은 특정 조건이 참(True)인지 거짓(False)인지에 따라
실행할 코드를 선택하는 문법입니다.

`if`, `elif`, `else`는 위에서 아래로 조건을 검사합니다.
처음으로 참이 되는 조건의 코드만 실행됩니다.
"""

# 점수를 하나 정해 둡니다.
# 나중에는 input()으로 사용자에게 점수를 입력받을 수도 있습니다.
score = 85

# if는 "만약 ~라면"이라는 뜻으로 이해하면 됩니다.
# score가 90 이상이면 A 등급을 저장합니다.
if score >= 90:
    grade = "A"

# elif는 앞의 if 조건이 거짓일 때 다음 조건을 검사합니다.
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"

# else는 위 조건이 모두 거짓일 때 실행됩니다.
else:
    grade = "D"

print("점수:", score)
print("등급:", grade)

# 아래 코드는 조건문에서 and를 사용하는 예시입니다.
# 지금은 주석 처리되어 있어 실행되지 않습니다.
# 주석을 해제하면 나이와 티켓 보유 여부를 함께 검사할 수 있습니다.
# age = 20
# has_ticket = True

# if age >= 18 and has_ticket:
#     print("입장할 수 있습니다.")
# else:
#     print("입장할 수 없습니다.")
