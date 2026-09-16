"""자료구조를 처리하는 함수 예제입니다.

함수는 숫자나 문자열뿐 아니라 list, dict 같은 자료구조도 받을 수 있습니다.

백엔드 개발에서는 사용자 목록, 메시지 목록, API 응답 데이터를
함수로 나누어 처리하는 일이 많습니다.
"""


def calculate_average(scores:list[int]) -> float:
    total = sum(scores)
    return total / len(scores)


def print_user(user: dict[str, object]) -> None:
    print("이름:", user["name"])
    print("역할:", user["role"])
    print("활성 상태:", user["active"])


score_list = [90, 85, 77, 92]
average = calculate_average(score_list)
print("평균 점수:", average)
average = calculate_average(score_list)
print("평균 점수:", average)

user = {
    "name": "Jean",
    "role": "admin",
    "active": True,
}

print_user(user)


def filter_passed_students(students:list)->tuple:
    passed_students = list()

    for student in students:
        if student["score"] >= 60:
            passed_students.append(student)

    return tuple(passed_students)


students = [
    {"name": "Jean", "score": 95},
    {"name": "Mina", "score": 72},
    {"name": "Jun", "score": 58},
]

passed = filter_passed_students(students)
print("통과 학생:", passed)
