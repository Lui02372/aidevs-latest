"""반복문과 자료구조를 함께 사용하는 예제입니다.

자료구조는 데이터를 담는 그릇이고,
반복문은 그 데이터를 하나씩 꺼내 처리하는 방법입니다.

이 예제에서는 list 안에 dict를 넣어 여러 명의 학생 정보를 표현합니다.
백엔드 API 응답이나 데이터베이스 조회 결과도 이런 모양으로 자주 다룹니다.
"""
# JSON(JavaScript Object Notation)과 모양이 비슷합니다.
students = [
    {"name": "Jean", "score": 95, "passed": True},
    {"name": "Mina", "score": 72, "passed": True},
    {"name": "Jun", "score": 58, "passed": False},
]

print("[학생 목록]")

# list에서 학생 dict를 하나씩 꺼냅니다.
for student in students:
    print(student["name"], "-", student["score"], "점")

print("\n[통과한 학생만 출력]")

for student in students:
    # dict 안의 passed 값이 True인 학생만 출력합니다.
    if student["passed"]:
        print(student["name"], "통과")

print("\n[평균 점수 계산]")

total_score = 0

for student in students:
    total_score += student["score"]

average = total_score / len(students)
print("평균 점수:", average)

print("\n[학생별 상세 정보]")

for index, student in enumerate(students, start=1):
    print(f"\n학생 {index}")

    # dict의 key와 value를 함께 출력합니다.
    for key, value in student.items():
        print(key, "=", value)
