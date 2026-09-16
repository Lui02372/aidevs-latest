"""조건문과 함수를 함께 사용하는 예제입니다.

함수 안에서도 if, elif, else를 사용할 수 있습니다.
조건 판단 로직을 함수로 묶어 두면 같은 판단을 여러 곳에서 재사용할 수 있습니다.
"""


def get_grade(score)->str:
    if score >= 90:
        return "A"

    if score >= 80:
        return "B"

    if score >= 70:
        return "C"

    return "D"


def is_passed(score)-> bool:
    return score >= 60


scores = [95, 82, 73, 55]

for score in scores:
    grade = get_grade(score)
    passed = is_passed(score)

    print("점수:", score)
    print("등급:", grade)
    print("통과 여부:", passed)
    print("-" * 20)
