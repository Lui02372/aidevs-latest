"""for 반복문 예제입니다.

반복문은 같은 형태의 작업을 여러 번 실행할 때 사용합니다.
`for` 반복문은 리스트, 문자열, range 같은 값을 하나씩 꺼내며 실행합니다.
"""

# 여러 학생 이름을 리스트에 저장합니다.
students = ["지민", "서연", "민준"]
print(type(students))
print(len(students))

# for student in students는 students 리스트에서 값을 하나씩 꺼내
# student 변수에 넣고, 들여쓰기 된 코드를 반복 실행합니다.
for student in students:
    print(student, "님 출석했습니다.")

# total은 합계를 저장하기 위한 변수입니다.
# 처음에는 아무것도 더하지 않았으므로 0에서 시작합니다.
total = 0

# range(1, 6)은 1, 2, 3, 4, 5를 차례대로 만들어 줍니다.
# 끝 숫자 6은 포함되지 않는다는 점을 기억합니다.
for number in range(1, 6):
    # total += number는 total = total + number와 같은 뜻입니다.
    total += number

print("1부터 5까지의 합:", total)
