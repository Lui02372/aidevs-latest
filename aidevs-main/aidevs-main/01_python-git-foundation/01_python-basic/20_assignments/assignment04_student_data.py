# 1. 학생 3명 이상의 정보를 list 안의 dict로 저장합니다.
# 2. 각 학생 dict에는 name, score, tags를 포함합니다.
# 3. tags는 list로 저장합니다.
students: list[dict] = [
    {"name": "Jean", "score": 95, "tags": ["python", "backend"]},
    {"name": "Mina", "score": 82, "tags": ["python", "ui"]},
    {"name": "Tom", "score": 58, "tags": ["python", "frontend"]},
]
# 4. 모든 학생의 이름과 점수를 출력합니다.
# 5. 평균 점수를 계산합니다.
sum_score = 0
for student in students:
    print(f"이름: {student['name']}, 점수: {student['score']}")
    sum_score += student["score"]
average_score = sum_score / len(students)
print(f"평균 점수: {average_score}")

# 6. 60점 이상인 학생만 출력합니다.
for student in students:
    if student["score"] >= 60:
        print(f"합격 학생: {student['name']}, 점수: {student['score']}")

# 7. 전체 tags를 set으로 변환해 중복을 제거합니다.
all_tags: set[str] = set()
for student in students:
    all_tags.update(student["tags"])
print(f"전체 tags: {all_tags}")