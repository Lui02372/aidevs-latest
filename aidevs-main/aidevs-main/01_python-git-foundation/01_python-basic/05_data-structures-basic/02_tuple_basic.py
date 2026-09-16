"""tuple 기초 예제입니다.

tuple은 여러 값을 순서대로 저장하는 자료구조입니다.

list와 비슷하지만 중요한 차이가 있습니다.
tuple은 한 번 만들면 값을 수정할 수 없습니다.

값이 바뀌면 안 되는 데이터, 예를 들어 좌표, 고정 설정값,
함수에서 여러 값을 한 번에 반환할 때 자주 사용합니다.
"""

# 소괄호 ( )를 사용해 tuple을 만듭니다.
# []
point = (10, 20)

print("좌표:", point)
print("자료형:", type(point))

# tuple도 순서가 있으므로 index로 값을 꺼낼 수 있습니다.
x = point[0]
y = point[1]

print("x 좌표:", x)
print("y 좌표:", y)

# tuple은 반복문으로 하나씩 꺼낼 수 있습니다.
print("\n[좌표 값 출력]")
for value in point:
    print(value)

# tuple unpacking은 tuple 안의 값을 여러 변수에 나누어 담는 문법입니다.
name_and_score = ("Jean", 95)
name, score = name_and_score

name, score = ("Jean", 95)  # tuple unpacking


print("\n이름:", name)
print("점수:", score)

# 아래 코드는 오류가 납니다.
# tuple은 값을 수정할 수 없기 때문입니다.
# 직접 확인해 보고 싶다면 주석을 해제해 보세요.
# point[0] = 100

print("\ntuple은 만든 뒤 값을 바꿀 수 없습니다.")
